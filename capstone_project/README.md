---
title: SEC Fraud Detector
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# SEC Fraud Detector

NLP-based fraud detection on SEC financial filings.  
Built as a data science bootcamp capstone project.

## What it does

Paste any financial statement excerpt (10-K, 8-K, MD&A section) and get an instant fraud risk assessment. The model classifies the text as **Low**, **Moderate**, or **High** risk based on linguistic patterns learned from confirmed fraud cases.

## Model

| Component | Details |
|---|---|
| **Architecture** | Logistic Regression |
| **Embedding** | Hybrid TF-IDF (500 features) + SEC-BERT (768 dims) |
| **SEC-BERT model** | `nlpaueb/sec-bert-base` — frozen, no fine-tuning |
| **Dataset** | AmitKedia SEC Filings — 170 samples (85 fraud / 85 non-fraud) |
| **Validation** | Stratified 5-fold cross-validation |
| **Test F1** | 0.895 |
| **Recall (fraud)** | 1.000 — zero missed fraud cases on test set |
| **ROC-AUC** | 0.983 |
| **CV F1** | 0.856 ± 0.056 |

## Project pipeline

```
NB01 — EDA
  └─ Class distribution, text length, vocabulary analysis, word clouds

NB02 — Embedding Comparison
  └─ TF-IDF vs Frozen FinBERT vs Frozen SEC-BERT
      vs Hybrid TF-IDF + SEC-BERT vs Isolation Forest (unsupervised)
  └─ Winner: Hybrid TF-IDF + SEC-BERT (CV F1 = 0.845, Recall = 0.929)

NB03 — Classifier Comparison on Hybrid features
  └─ Logistic Regression vs Linear SVM vs Random Forest
      vs Gradient Boosting vs Naive Bayes
  └─ Winner: Logistic Regression (Recall = 1.0, gap = 0.0004)
```

## Why Hybrid TF-IDF + SEC-BERT

- **TF-IDF** captures fraud-specific lexical patterns: *restatement, going concern, material weakness, irregularities*
- **SEC-BERT** (`nlpaueb/sec-bert-base`) was pre-trained on actual SEC 10-K and 10-Q filings — the exact document type being classified
- Combining both gives the model lexical and semantic signals simultaneously
- At 170 samples, neither embedding alone generalises as well as their combination

## Dataset

[AmitKedia Financial Statement Fraud Dataset](https://www.kaggle.com/datasets/amitkedia/financial-statement-fraud-data) — 170 SEC filings, balanced 85 fraud / 85 non-fraud, sourced from SEC-EDGAR and AAER enforcement releases.

## Scope & limitations

> ⚠️ This tool classifies filing **text** based on linguistic patterns learned from 170 SEC filings. It does not perform forensic accounting analysis or evaluate structured financial ratios. Results are probabilistic and should not replace professional audit judgment. Built for research and educational purposes only.

## Tech stack

`Python` · `Streamlit` · `scikit-learn` · `HuggingFace Transformers` · `PyTorch` · `SEC-BERT`

## Author

**Lamia Rahmani** — Data Science Bootcamp Capstone, 2026  
**Bootcamp Coach:** Sara Latreche
