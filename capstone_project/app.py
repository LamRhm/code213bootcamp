import streamlit as st
import pickle
import joblib
import torch
import numpy as np
import re
import os
from transformers import AutoTokenizer, AutoModel
from datetime import datetime

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SEC Fraud Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset */
[data-testid="stAppViewContainer"] { background: #0a0e17; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0d1220; border-right: 1px solid #1e2a3a; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Page shell */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── NAV BAR ── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 48px;
    border-bottom: 1px solid #1e2a3a;
    background: #0a0e17;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #f1f5f9;
    letter-spacing: -0.3px;
}
.nav-logo-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3b82f6;
    box-shadow: 0 0 8px #3b82f680;
}
.nav-badge {
    font-size: 11px;
    font-weight: 500;
    color: #64748b;
    background: #1e2a3a;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}

/* ── HERO ── */
.hero {
    padding: 64px 48px 48px;
    max-width: 1100px;
    margin: 0 auto;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 42px;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.15;
    letter-spacing: -1.2px;
    margin-bottom: 16px;
}
.hero-title span {
    color: #3b82f6;
}
.hero-desc {
    font-size: 15px;
    color: #64748b;
    line-height: 1.7;
    max-width: 560px;
    margin-bottom: 40px;
}

/* ── STAT STRIP ── */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #1e2a3a;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 48px;
}
.stat-cell {
    background: #0d1220;
    padding: 20px 24px;
}
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    color: #f1f5f9;
    letter-spacing: -0.5px;
}
.stat-lbl {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* ── MAIN GRID ── */
.main-grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 20px;
    padding: 0 48px 48px;
    max-width: 1100px;
    margin: 0 auto;
}

/* ── CARD ── */
.card {
    background: #0d1220;
    border: 1px solid #1e2a3a;
    border-radius: 14px;
    padding: 28px;
}
.card-title {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 20px;
}

/* ── TEXTAREA OVERRIDE ── */
textarea {
    background: #070b12 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    resize: none !important;
}
textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px #3b82f620 !important;
}
textarea::placeholder { color: #334155 !important; }

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: #3b82f6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 28px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
    margin-top: 12px !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
[data-testid="stButton"] > button:hover {
    background: #2563eb !important;
}

/* ── RESULT PANEL ── */
.result-risk-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 24px;
}
.badge-low    { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-mod    { background: #431407; color: #fb923c; border: 1px solid #9a3412; }
.badge-high   { background: #3b0764; color: #e879f9; border: 1px solid #7e22ce; }

.prob-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 56px;
    font-weight: 500;
    line-height: 1;
    letter-spacing: -2px;
    margin-bottom: 8px;
}
.prob-low  { color: #4ade80; }
.prob-mod  { color: #fb923c; }
.prob-high { color: #e879f9; }

.prob-bar-track {
    height: 4px;
    background: #1e2a3a;
    border-radius: 4px;
    margin: 20px 0 28px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e2a3a;
}
.metric-row:last-child { border-bottom: none; }
.metric-key {
    font-size: 12px;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
}
.metric-val {
    font-size: 12px;
    color: #94a3b8;
    font-weight: 500;
}
.metric-val-accent {
    font-size: 12px;
    color: #3b82f6;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* ── KEYWORD PANEL ── */
.kw-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.kw-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 6px;
    background: #0a1628;
    border: 1px solid #1e3a5f;
    color: #60a5fa;
}
.kw-chip.hit {
    background: #1e1245;
    border-color: #7c3aed;
    color: #c084fc;
}

/* ── MODEL INFO ── */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 10px 0;
    border-bottom: 1px solid #1e2a3a;
    gap: 16px;
}
.info-row:last-child { border-bottom: none; }
.info-key {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    white-space: nowrap;
    padding-top: 1px;
}
.info-val {
    font-size: 12px;
    color: #94a3b8;
    text-align: right;
    line-height: 1.5;
}

/* ── NOTICE ── */
.notice {
    margin: 0 48px 32px;
    max-width: 1060px;
    background: #0d1628;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 14px 20px;
    font-size: 12px;
    color: #475569;
    line-height: 1.6;
}
.notice span { color: #3b82f6; font-weight: 500; }

/* Alert overrides */
[data-testid="stAlert"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Spinner */
[data-testid="stSpinner"] p { color: #475569 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load model
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    model   = joblib.load("fraud_detection_final_model.pkl")
    tfidf   = joblib.load("tfidf_vectorizer.pkl")
    sec_tok = AutoTokenizer.from_pretrained("nlpaueb/sec-bert-base")
    sec_mdl = AutoModel.from_pretrained("nlpaueb/sec-bert-base")
    sec_mdl.eval()
    for p in sec_mdl.parameters():
        p.requires_grad = False
    return model, tfidf, sec_tok, sec_mdl

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
FRAUD_KEYWORDS = [
    "restatement", "going concern", "material weakness",
    "internal control", "misstatement", "irregularities",
    "investigation", "SEC inquiry", "revenue recognition",
    "write-off", "impairment", "earnings manipulation",
    "off-balance sheet", "undisclosed", "overstated"
]

def clean_text(text):
    text = str(text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return re.sub(r"\s+", " ", text).lower().strip()

def get_sec_bert_embedding(text, tokenizer, model, device="cpu"):
    inputs = tokenizer(
        [text], padding=True, truncation=True,
        max_length=512, return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        out = model(**inputs)
    return out.last_hidden_state[:, 0, :].cpu().numpy()

def build_hybrid(text, tfidf_vec, sec_tok, sec_mdl):
    cleaned = clean_text(text)
    tfidf_feat = tfidf_vec.transform([cleaned]).toarray()
    norm_tfidf  = tfidf_feat / (np.linalg.norm(tfidf_feat) + 1e-9)
    sec_emb     = get_sec_bert_embedding(cleaned, sec_tok, sec_mdl)
    norm_sec    = sec_emb / (np.linalg.norm(sec_emb) + 1e-9)
    return np.hstack([norm_tfidf, norm_sec])

def detect_keywords(text):
    text_lower = text.lower()
    return [kw for kw in FRAUD_KEYWORDS if kw in text_lower]

def risk_tier(prob):
    if prob < 0.40:
        return "Low Risk", "low", "badge-low", "prob-low", "#4ade80"
    elif prob < 0.75:
        return "Moderate Risk", "mod", "badge-mod", "prob-mod", "#fb923c"
    else:
        return "High Risk", "high", "badge-high", "prob-high", "#e879f9"

# ─────────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">
        <div class="nav-logo-dot"></div>
        SEC Fraud Detector
    </div>
    <div class="nav-badge">RESEARCH · BOOTCAMP PROJECT</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">NLP · Financial Statement Analysis</div>
    <div class="hero-title">Detect fraud signals<br>in <span>SEC filings</span>.</div>
    <div class="hero-desc">
        Paste any financial statement excerpt — 10-K, 8-K, MD&A section —
        and get an instant risk assessment powered by a hybrid
        TF-IDF + SEC-BERT model trained on confirmed fraud cases.
    </div>
    <div class="stat-strip">
        <div class="stat-cell">
            <div class="stat-val">0.895</div>
            <div class="stat-lbl">Test F1 Score</div>
        </div>
        <div class="stat-cell">
            <div class="stat-val">1.000</div>
            <div class="stat-lbl">Recall (fraud)</div>
        </div>
        <div class="stat-cell">
            <div class="stat-val">0.983</div>
            <div class="stat-lbl">ROC-AUC</div>
        </div>
        <div class="stat-cell">
            <div class="stat-val">170</div>
            <div class="stat-lbl">Training samples</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN LAYOUT — use st.columns to keep streamlit widgets working
# ─────────────────────────────────────────────
pad_l, col_input, gap, col_result, pad_r = st.columns([0.05, 1.2, 0.04, 0.85, 0.05])

# ─── INPUT COLUMN ───────────────────────────
with col_input:
    st.markdown('<div class="card-title">FILING TEXT INPUT</div>', unsafe_allow_html=True)

    sample_texts = {
        "— paste your own text —": "",
        "Sample: Fraud (going concern + restatement)":
            "The Company has identified material weaknesses in its internal control over financial reporting. "
            "Management has concluded that the previously issued financial statements contained misstatements "
            "and will require restatement. There is substantial doubt about the Company's ability to continue "
            "as a going concern. An SEC inquiry into revenue recognition practices is currently ongoing.",
        "Sample: Non-fraud (clean filing)":
            "Net revenues for the fiscal year ended December 31 were 4.2 billion dollars, "
            "representing an increase of 8 percent compared to the prior year. "
            "The increase was primarily driven by strong performance in our core product segments. "
            "Operating income improved to 890 million dollars. "
            "The Board of Directors approved a quarterly dividend of 0.42 dollars per share."
    }

    selected = st.selectbox("Load a sample or paste your own:", list(sample_texts.keys()),
                            label_visibility="collapsed")
    default_text = sample_texts[selected]

    user_input = st.text_area(
        "Filing text",
        value=default_text,
        height=240,
        placeholder="Paste SEC filing text here — MD&A, 10-K, 8-K, footnotes...",
        label_visibility="collapsed"
    )

    analyze = st.button("Run Fraud Assessment →")

    # Keyword scanner (always visible)
    if user_input.strip():
        hits = detect_keywords(user_input)
        st.markdown('<div style="margin-top:20px">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-bottom:10px">KEYWORD SCAN</div>',
                    unsafe_allow_html=True)
        chips = ""
        for kw in FRAUD_KEYWORDS:
            cls = "kw-chip hit" if kw in hits else "kw-chip"
            chips += f'<span class="{cls}">{kw}</span>'
        st.markdown(f'<div class="kw-list">{chips}</div>', unsafe_allow_html=True)
        if hits:
            st.markdown(
                f'<div style="margin-top:10px;font-size:12px;color:#c084fc">'
                f'⚠ {len(hits)} fraud-associated term{"s" if len(hits)>1 else ""} detected</div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── RESULT COLUMN ──────────────────────────
with col_result:
    st.markdown('<div class="card-title">RISK ASSESSMENT</div>', unsafe_allow_html=True)

    if not analyze and not user_input.strip():
        st.markdown("""
        <div style="padding:40px 0;text-align:center;color:#1e3a5f">
            <div style="font-size:40px;margin-bottom:12px">🔍</div>
            <div style="font-size:13px;color:#334155;line-height:1.7">
                Enter filing text and click<br><strong style="color:#3b82f6">Run Fraud Assessment</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif analyze:
        if not user_input.strip():
            st.markdown('<div style="color:#fb923c;font-size:13px;padding:12px 0">⚠ Please enter some filing text first.</div>',
                        unsafe_allow_html=True)
        else:
            with st.spinner("Running hybrid model inference..."):
                try:
                    clf, tfidf_vec, sec_tok, sec_mdl = load_artifacts()
                    X = build_hybrid(user_input, tfidf_vec, sec_tok, sec_mdl)
                    prob = float(clf.predict_proba(X)[0][1])
                    label, tier, badge_cls, prob_cls, bar_color = risk_tier(prob)
                    hits = detect_keywords(user_input)
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    st.markdown(f'<div class="result-risk-badge {badge_cls}">{label}</div>',
                                unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="prob-number {prob_cls}">{prob:.1%}</div>'
                        f'<div style="font-size:12px;color:#475569">fraud probability</div>',
                        unsafe_allow_html=True
                    )

                    fill_w = int(prob * 100)
                    st.markdown(
                        f'<div class="prob-bar-track">'
                        f'<div class="prob-bar-fill" style="width:{fill_w}%;background:{bar_color}"></div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # Metrics
                    verdict = "Fraudulent pattern detected" if prob >= 0.70 else "No fraud pattern detected"
                    st.markdown(f"""
                    <div class="metric-row">
                        <span class="metric-key">verdict</span>
                        <span class="metric-val">{verdict}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">fraud_prob</span>
                        <span class="metric-val-accent">{prob:.4f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">keywords_hit</span>
                        <span class="metric-val">{len(hits)} / {len(FRAUD_KEYWORDS)}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">threshold</span>
                        <span class="metric-val">0.70</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">timestamp</span>
                        <span class="metric-val">{ts}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Contextual guidance
                    guidance = {
                        "low":  ("✓", "#4ade80", "Low lexical fraud risk. Filing language is consistent with non-fraudulent SEC disclosures."),
                        "mod":  ("!", "#fb923c", "Moderate risk signals detected. One or more linguistic patterns align with fraud-adjacent language. Manual review recommended."),
                        "high": ("⚠", "#e879f9", "High-confidence fraud indicators detected. Filing language strongly matches confirmed fraud cases in the training corpus. Escalate for review."),
                    }
                    icon, color, msg = guidance[tier]
                    st.markdown(
                        f'<div style="margin-top:20px;padding:14px 16px;border-radius:8px;'
                        f'background:{color}10;border:1px solid {color}30;'
                        f'font-size:12px;color:{color};line-height:1.6">'
                        f'<strong>{icon} {label}:</strong> {msg}</div>',
                        unsafe_allow_html=True
                    )

                except FileNotFoundError as e:
                    st.markdown(f"""
                    <div style="padding:20px;background:#1a0a0a;border:1px solid #7f1d1d;
                         border-radius:10px;font-size:13px;color:#fca5a5;line-height:1.7">
                        <strong>Model files not found.</strong><br>
                        Make sure these files are in the same directory as app.py:<br>
                        <code style="color:#f87171">fraud_detection_final_model.pkl</code><br>
                        <code style="color:#f87171">tfidf_vectorizer.pkl</code>
                    </div>
                    """, unsafe_allow_html=True)

    # Model info card — always shown
    st.markdown("""
    <div style="margin-top:28px">
    <div class="card-title">MODEL DETAILS</div>
    <div class="info-row">
        <span class="info-key">Architecture</span>
        <span class="info-val">Logistic Regression</span>
    </div>
    <div class="info-row">
        <span class="info-key">Embedding</span>
        <span class="info-val">Hybrid TF-IDF (500) + SEC-BERT (768)</span>
    </div>
    <div class="info-row">
        <span class="info-key">SEC-BERT</span>
        <span class="info-val">nlpaueb/sec-bert-base · frozen</span>
    </div>
    <div class="info-row">
        <span class="info-key">Dataset</span>
        <span class="info-val">AmitKedia · 170 SEC filings<br>85 fraud / 85 non-fraud</span>
    </div>
    <div class="info-row">
        <span class="info-key">Validation</span>
        <span class="info-val">Stratified 5-fold CV</span>
    </div>
    <div class="info-row">
        <span class="info-key">CV F1</span>
        <span class="info-val">0.856 ± 0.056</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NOTICE
# ─────────────────────────────────────────────
st.markdown("""
<div class="notice">
    <span>⚠ Research scope:</span>
    This tool classifies filing text based on linguistic patterns learned from 170 SEC filings.
    It does not perform forensic accounting analysis or evaluate structured financial data.
    Results are probabilistic and should not replace professional audit judgment.
    Built as a data science bootcamp capstone project.
</div>
""", unsafe_allow_html=True)
