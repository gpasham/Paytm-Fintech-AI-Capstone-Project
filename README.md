# Paytm Fintech AI Capstone Project

Details of the student:
Name: Greeshma Pasham
ID: bitsom_ftai_2601078
email id: greeshmapasham@gmail.com

This repository brings together three complementary fintech workstreams built around a Paytm-oriented use case. Each branch focuses on a different decision layer in a digital financial ecosystem: **investment intelligence**, **credit underwriting**, and **payments/fraud analytics**.

The project combines Python, SQL, machine learning, financial modelling, anomaly detection, data analytics, and responsible-AI governance into a single capstone portfolio.

---

## Project Navigation

| Workstream | Branch | Primary Focus | Key Techniques |
|---|---|---|---|
| **AI Advisory & Blockchain Risk** | [`ai_advisory_blockchain`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/ai_advisory_blockchain) | Investment advisory, disclosure analysis & crypto/blockchain risk | CAPM, portfolio risk/return, DCF, rule-based NLP, multi-agent reasoning, risk escalation |
| **Credit Risk & Lending ML** | [`credit-risk-lending-ml`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/credit-risk-lending-ml) | Paytm Postpaid-style credit underwriting & transaction anomaly detection | Logistic Regression, Decision Tree, Isolation Forest, risk-based pricing, responsible AI |
| **Payments & Fraud Analytics** | [`payments-fraud-analytics`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/payments-fraud-analytics) | Payments performance, merchant analytics & reconciliation | SQL, SQLite, pandas, KPI dashboards, payment-method/category analysis, reconciliation |

Follow the branch-specific `README.md` for execution instructions and expected outputs.

# 1. AI Advisory & Blockchain Risk

**Branch:** `ai_advisory_blockchain`

This workstream explores how AI-assisted decision systems can support **investment advisory and financial risk analysis**.

The branch uses deterministic/mock logic for its recorded baseline runs, allowing the workflows to be reproduced without requiring external LLM/API credentials.

# 2. Credit Risk & Lending ML

**Branch:** `credit-risk-lending-ml`

This workstream develops a compact **credit-risk and transaction-anomaly detection pipeline** for a Paytm Postpaid-style lending scenario.

It combines supervised learning for default prediction with unsupervised anomaly detection for transaction behaviour.

# 3. Payments & Fraud Analytics

**Branch:** `payments-fraud-analytics`

This workstream focuses on **transaction-level payments analytics, merchant performance and reconciliation** using a relational SQLite dataset.

# Technology Stack

### Programming & Analytics
- Python
- pandas
- NumPy
- scikit-learn
- SQLite
- SQL

### Machine Learning
- Logistic Regression
- Decision Tree
- Isolation Forest
- StandardScaler
- Stratified train/test evaluation
- ROC/AUC analysis

### Financial Modelling
- CAPM
- Portfolio expected return
- Portfolio volatility
- DCF valuation
- Risk-based pricing

### AI / Decision Systems
- Rule-based disclosure extraction
- Mock LLM advisory workflow
- Multi-agent Bull/Bear/Synthesizer architecture
- Human-in-the-loop escalation

### Visualization
- Matplotlib-generated analytical outputs
- KPI scorecards
- Trend charts
- Category/payment-method analysis
- ROC curves

---

# Repository Structure

The repository is intentionally organized around independent branches rather than forcing all three workflows into one implementation.

```text
Paytm-Fintech-AI-Capstone-Project/
│
├── ai_advisory_blockchain
│   ├── Investment advisory
│   ├── Disclosure intelligence
│   ├── DCF
│   ├── Multi-agent debate
│   └── Blockchain risk analysis
│
├── credit-risk-lending-ml
│   ├── Credit-risk modelling
│   ├── Risk-based pricing
│   ├── Isolation Forest
│   └── Responsible AI governance
│
└── payments-fraud-analytics
    ├── SQL analytics
    ├── Payment KPIs
    ├── Merchant analytics
    ├── Dashboard outputs
    └── Reconciliation
```
