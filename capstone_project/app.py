import streamlit as st
import pickle
import torch
import numpy as np
import re
from transformers import AutoTokenizer, AutoModel
from datetime import datetime

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Fraud Risk Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Corporate Styling
# -------------------------------------------------
st.markdown("""
<style>
.top-banner {
    background-color: #0f172a;
    padding: 28px;
    border-radius: 10px;
    margin-bottom: 25px;
}
.top-title {
    font-size: 38px;
    font-weight: 700;
    color: white;
}
.top-subtitle {
    font-size: 15px;
    color: #cbd5e1;
}
.footer {
    text-align: center;
    font-size: 12px;
    color: #9ca3af;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("Audit Risk Platform")
st.sidebar.markdown("### Modules")
st.sidebar.write("• Fraud Risk Assessment")
st.sidebar.write("• Filing Review")
st.sidebar.write("• Compliance Monitoring")
st.sidebar.markdown("---")
st.sidebar.caption("Internal Use | SEC Filing Classification Model")

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div class="top-banner">
    <div class="top-title">Financial Fraud Risk Analytics Dashboard</div>
    <div class="top-subtitle">
        NLP-based classification of SEC filing-style financial statements
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Model
# -------------------------------------------------
@st.cache_resource
def load_model():
    with open("fraud_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

@st.cache_resource
def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    finbert_model = AutoModel.from_pretrained("yiyanghkust/finbert-tone")
    return tokenizer, finbert_model

tokenizer, finbert_model = load_finbert()

# -------------------------------------------------
# Utilities
# -------------------------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

def get_embedding(text):
    text = clean_text(text)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    with torch.no_grad():
        outputs = finbert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

# -------------------------------------------------
# Layout
# -------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("SEC Filing Text Input")
    user_input = st.text_area(
        "Enter SEC filing excerpt (Form 10-K / 8-K section):",
        height=220
    )
    analyze = st.button("Run Risk Assessment")

with col_right:
    st.subheader("Model Overview")
    st.info("""
    • Embeddings: FinBERT (financial-domain transformer)  
    • Classifier: Logistic Regression (regularized)  
    • Dataset: AmitKedia SEC Filings (170 samples)  
    • ROC-AUC: 0.93  
    • Evaluation: Stratified 5-fold CV  
    """)

# -------------------------------------------------
# Risk Assessment
# -------------------------------------------------
if analyze:
    if user_input.strip() == "":
        st.warning("Please provide SEC filing text for analysis.")
    else:
        embedding = get_embedding(user_input)
        probability = model.predict_proba(embedding)[0][1]

        # Conservative Fraud Trigger
        fraud_threshold = 0.70
        prediction = 1 if probability >= fraud_threshold else 0

        # Professional Risk Tiers
        if probability < 0.40:
            risk_level = "Low"
        elif probability < 0.75:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        st.markdown("## Risk Assessment Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Fraud Probability", f"{probability:.2%}")

        with col2:
            st.metric("Risk Level", risk_level)

        with col3:
            classification = (
                "Fraudulent Pattern Detected"
                if prediction == 1
                else "No Fraud Pattern Detected"
            )
            st.metric("Classification", classification)

        st.markdown("### Risk Confidence Indicator")
        st.progress(float(probability))

        # Contextual Explanation
        if risk_level == "Low":
            st.success("Low textual fraud risk based on learned SEC filing patterns.")
        elif risk_level == "Moderate":
            st.warning("Moderate textual risk signals detected. Further review recommended.")
        else:
            st.error("High textual fraud indicators detected. Escalation recommended.")

        st.caption(
        f"Assessment generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        st.markdown("---")
        st.markdown("""
        **Model Scope Notice:**  
        This system classifies financial filing text based on patterns learned from the AmitKedia SEC filings dataset.  
        It does not perform forensic accounting analysis or structured financial ratio evaluation.
        """)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="footer">Confidential | Internal SEC Filing Risk Classification System</div>',
    unsafe_allow_html=True
)