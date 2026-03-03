# Financial Fraud Detection Using FinBERT and Logistic Regression

## Project Overview

This project presents a financial fraud detection system built using Natural Language Processing (NLP) and machine learning techniques.

The objective is to classify financial filing text into two categories:

- **0 → Non-Fraud**
- **1 → Fraud**

The proposed solution integrates:

- **FinBERT** (financial-domain transformer for contextual embeddings)
- **Logistic Regression** (regularized linear classifier)
- **Streamlit** (interactive deployment interface)

The system focuses on identifying fraud-related textual patterns in financial filings.

---

## Dataset

The model was developed using the **AmitKedia dataset**, which contains **170 labeled financial text samples** derived primarily from SEC filing-style documents.

Due to the relatively small dataset size, full transformer fine-tuning was avoided to reduce the risk of overfitting. Instead, a pretrained financial-domain transformer was used as a fixed feature extractor to generate contextual embeddings.

---

## Model Selection: Why `yiyanghkust/finbert-tone`?

The embedding model **`yiyanghkust/finbert-tone`** was selected because:

- It is pretrained on financial corpora.
- It captures domain-specific terminology and contextual nuances common in financial disclosures.
- It encodes subtle tone, uncertainty, and risk-related linguistic signals often associated with fraud-labeled filings.

Although originally fine-tuned for financial sentiment analysis, its contextual embeddings proved highly effective for fraud-related classification tasks.

During experimentation, this model outperformed alternative financial-domain transformers (including `ProsusAI/finbert`), achieving:

- Higher ROC-AUC
- Higher test F1-score
- More stable cross-validation results

Based on empirical evaluation, `yiyanghkust/finbert-tone` was selected as the final embedding model.

---

## Methodology

The modeling pipeline followed these steps:

1. Data cleaning and preprocessing  
2. Feature engineering using FinBERT embeddings  
   - CLS token representation (768-dimensional vectors)  
3. Logistic Regression training  
   - `class_weight="balanced"`  
   - Regularization (`C=0.5`) to reduce overfitting  
4. Stratified 5-fold cross-validation  
5. Model evaluation using Accuracy, F1-score, and ROC-AUC  
6. Deployment via Streamlit  

This approach combines deep contextual embeddings with a classical, interpretable classifier suitable for small datasets.

---

## Results

### Test Set Performance

- **Accuracy:** 82%
- **F1-score:** 0.82
- **ROC-AUC:** 0.93

The ROC-AUC score of 0.93 indicates strong separability between fraud and non-fraud classes. Balanced precision and recall demonstrate consistent predictive behavior across both categories.

---

### 5-Fold Stratified Cross-Validation

- **F1 Scores:** [0.76, 0.76, 0.81, 0.71, 0.44]
- **Mean F1-score:** 0.70

Most folds achieved strong F1 performance (0.71–0.81), confirming stable predictive capability across different subsets of the data.

One fold produced a lower score (0.44). This variability is expected given the small dataset size (170 samples). In 5-fold cross-validation, each validation fold contains approximately 34 samples. When a small number of more complex or borderline examples are concentrated within a single fold, performance may temporarily decrease.

Such variance is common in small-sample NLP classification tasks, particularly when working with high-dimensional embeddings (768 features).

Importantly:

- The majority of folds remain strong.
- The overall mean F1-score of 0.70 indicates reasonable robustness.
- The test performance remains consistent with cross-validation trends.

---

## Overfitting Analysis

The model achieves perfect training performance (F1 = 1.00). This is expected in high-dimensional embedding spaces where training samples can become linearly separable.

However, the model maintains strong performance on unseen test data (F1 ≈ 0.82) and stable cross-validation results (mean F1 ≈ 0.70), indicating controlled and acceptable generalization behavior.

Regularization was applied to mitigate excessive model complexity.

---

## Limitations

- Small dataset size (170 samples)
- No transformer fine-tuning to prevent overfitting
- Model trained exclusively on AmitKedia SEC filing-style disclosures
- Performance depends on the distribution of labeled training data
- May not generalize to:
  - Audit commentary
  - Investigative reports
  - Forensic accounting narratives
  - Structured financial ratio analysis

### Interpretation of Demo Behavior

Some manually created financial examples produced unexpected predictions. This occurs because the model learns statistical textual patterns present in the labeled dataset rather than performing true forensic accounting analysis.

The AmitKedia dataset contains specific structural and stylistic filing patterns. The model associates these patterns with the fraud label. As a result, inputs that fall outside the original distribution may be misclassified.

---

## Future Improvements

- Training on a larger and more diverse financial corpus
- Incorporating structured financial indicators (e.g., ratios, anomaly detection)
- Combining NLP embeddings with quantitative financial features
- Exploring probability calibration techniques

---

## Deployment

The model is deployed using **Streamlit** on **HuggingFace Spaces**.

Users can input SEC filing-style financial text and receive:

- Fraud probability score
- Risk level classification
- Real-time prediction output

---

## Author

**Student:** Lamia Rahmani  
**Bootcamp Coach & Project Supervisor:** Sara Latreche  
**Program:** Data Science Bootcamp – Code213