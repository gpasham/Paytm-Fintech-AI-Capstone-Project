# Paytm Fintech AI Capstone Project

> **An end-to-end fintech analytics and AI capstone covering investment advisory, credit risk, transaction analytics, and fraud detection.**

This repository brings together three complementary fintech workstreams built around a Paytm-oriented use case. Each branch focuses on a different decision layer in a digital financial ecosystem: **investment intelligence**, **credit underwriting**, and **payments/fraud analytics**.

The project combines Python, SQL, machine learning, financial modelling, anomaly detection, data analytics, and responsible-AI governance into a single capstone portfolio.

---

## 🧭 Project Navigation

| Workstream | Branch | Primary Focus | Key Techniques |
|---|---|---|---|
| 📈 **AI Advisory & Blockchain Risk** | [`ai_advisory_blockchain`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/ai_advisory_blockchain) | Investment advisory, disclosure analysis & crypto/blockchain risk | CAPM, portfolio risk/return, DCF, rule-based NLP, multi-agent reasoning, risk escalation |
| 💳 **Credit Risk & Lending ML** | [`credit-risk-lending-ml`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/credit-risk-lending-ml) | Paytm Postpaid-style credit underwriting & transaction anomaly detection | Logistic Regression, Decision Tree, Isolation Forest, risk-based pricing, responsible AI |
| 📊 **Payments & Fraud Analytics** | [`payments-fraud-analytics`](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/payments-fraud-analytics) | Payments performance, merchant analytics & reconciliation | SQL, SQLite, pandas, KPI dashboards, payment-method/category analysis, reconciliation |

### Quick Links

- **[📈 AI Advisory & Blockchain Risk →](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/ai_advisory_blockchain)**
- **[💳 Credit Risk & Lending ML →](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/credit-risk-lending-ml)**
- **[📊 Payments & Fraud Analytics →](https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/payments-fraud-analytics)**

---

# 1. 📈 AI Advisory & Blockchain Risk

**Branch:** `ai_advisory_blockchain`

This workstream explores how AI-assisted decision systems can support **investment advisory and financial risk analysis**.

The branch uses deterministic/mock logic for its recorded baseline runs, allowing the workflows to be reproduced without requiring external LLM/API credentials.

### What it covers

- **Investor profiling & portfolio construction**
  - Maps investor risk profiles to prescribed portfolios.
  - Uses a local stock universe as the market-data input.

- **Portfolio analytics**
  - Calculates CAPM expected returns.
  - Calculates portfolio expected return and volatility.
  - Escalates portfolios when risk exceeds the defined threshold.

- **Disclosure intelligence**
  - Extracts financial risk signals from disclosure text.
  - Identifies litigation, regulatory exposure and customer-concentration signals.
  - Detects hedging language.
  - Classifies narrative sentiment as confident, cautious or neutral.

- **Multi-agent investment debate**
  - Bull agent
  - Bear agent
  - Synthesizer agent

- **DCF valuation**
  - Produces deterministic discounted-cash-flow outputs.

- **Blockchain / crypto risk**
  - Fiat-collateralized vs. algorithmic stablecoins
  - Tokenomics and DAO governance
  - Portfolio/CAPM considerations
  - Survivorship bias and transaction costs
  - Social-engineering/T.A.N.G. risks
  - Bank-side defensive controls

### Key files

```text
stock_universe.py
investor_profiles.py
disclosure_snippets.py
advisory_agent.py
extract_disclosure.py
debate.py
dcf_calculator.py
blockchain_risk_note.md
```

### Design principle

The advisory workflow follows:

**Think → Act → Observe → Decide**

This separates portfolio selection, data retrieval, quantitative analysis and the final escalation/decision layer.

---

# 2. 💳 Credit Risk & Lending ML

**Branch:** `credit-risk-lending-ml`

This workstream develops a compact **credit-risk and transaction-anomaly detection pipeline** for a Paytm Postpaid-style lending scenario.

It combines supervised learning for default prediction with unsupervised anomaly detection for transaction behaviour.

### Data

- **400 synthetic credit applicants**
- **20% thin-file applicants** with missing credit-bureau scores
- **265 transaction-behaviour records**
- **15 deliberately seeded transaction anomalies**

### Credit-risk pipeline

The applicant model includes:

- Monthly income
- Existing loan count
- Credit-utilization ratio
- UPI monthly inflow
- Bounced payments
- Credit-bureau score
- Employment type
- Thin-file indicator

The preprocessing workflow uses:

1. Stratified 75/25 train-test split
2. Training-only median imputation for missing bureau scores
3. One-hot encoding for employment type
4. Training-only feature scaling
5. Logistic Regression
6. Decision Tree classification

### Model comparison

| Metric | Logistic Regression | Decision Tree |
|---|---:|---:|
| Accuracy | **76.00%** | 67.00% |
| Precision | **38.89%** | 24.00% |
| Recall | **35.00%** | 30.00% |
| F1 | **36.84%** | 26.67% |
| ROC AUC | **0.71875** | 0.53125 |

**Result:** Logistic Regression provides stronger overall predictive performance and materially better discrimination on the test set.

### Risk-based pricing

Applicants are bucketed into four risk tiers using predicted default probabilities, with illustrative interest-rate ranges increasing with observed risk.

The observed default rate across the four tiers was monotonic:

**8% → 12% → 20% → 40%**

This provides a basic sanity check that the model's risk ranking aligns with realized default frequency in the synthetic test data.

### Transaction anomaly detection

Isolation Forest is applied to standardized behavioural features:

- `txn_hour`
- `is_new_device`
- `txn_amount_inr`

Using contamination equal to the seeded anomaly proportion:

**15 / 265 = 5.66%**

the model detected:

**11 / 15 seeded anomalies = 73.33% recall**

### Responsible AI

The branch also considers proxy discrimination: variables such as employment type, income and credit-bureau score could correlate with protected attributes in a real deployment even when those attributes are not explicitly included.

A recommended governance control is **maker-checker human review for declined thin-file applicants**, alongside fairness testing, feature/proxy-risk assessment, monitoring and an appeal pathway.

### Key files

```text
generate_data.py
credit_applicants.csv
txn_behaviour.csv
model_comparison.csv
risk_pricing_table.csv
roc_comparison.png
isolation_forest_results.csv
```

---

# 3. 📊 Payments & Fraud Analytics

**Branch:** `payments-fraud-analytics`

This workstream focuses on **transaction-level payments analytics, merchant performance and reconciliation** using a relational SQLite dataset.

### Core datasets

```text
users.csv
merchant_master.csv
ledger.csv
gateway.csv
paytm_payments.db
```

The branch also contains the SQL queries, reconciliation script and exported dashboard visuals.

### Analytics covered

The SQL analytics workflow examines:

- Payment and transaction KPIs
- Daily payment trends
- GMV by payment method
- GMV by transaction category
- Merchant-level performance
- Top merchants
- Gateway vs. ledger reconciliation

### Dashboard outputs

The branch includes visual outputs for:

- Headline scorecards
- Daily trends
- GMV by payment method
- GMV by category
- Top-10 merchant analysis

### Reconciliation

`reconcile.py` compares payment records across the relevant payment/gateway and ledger datasets to identify discrepancies and support operational controls.

### Key files

```text
analytics_queries.sql
reconcile.py
generate_data.py
dashboard_interpretation.md
paytm_payments.db
gateway.csv
ledger.csv
merchant_master.csv
users.csv
```

---

# 🔗 How the Three Workstreams Fit Together

The three branches can be viewed as different layers of a fintech decision system:

```text
                         PAYTM FINTECH AI
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      INVESTMENT          CREDIT & LENDING   PAYMENTS & FRAUD
       ADVISORY               RISK               ANALYTICS
             │                 │                 │
             ▼                 ▼                 ▼
      Portfolio risk       Default risk      Transaction KPIs
      CAPM / DCF           Risk pricing      Merchant analytics
      Disclosures          Thin-file ML      Reconciliation
      AI debate            Anomaly ML        Payment trends
      Blockchain risk                         Fraud signals
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    RESPONSIBLE FINTECH AI
                 ─────────────────────────────
                 • Explainability
                 • Human escalation
                 • Risk monitoring
                 • Fairness / proxy checks
                 • Data quality & controls
```

Together, the branches demonstrate how analytics and AI can support multiple financial workflows while keeping **risk controls, human oversight and reproducibility** in the design.

---

# 🛠️ Technology Stack

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

# 📂 Repository Structure

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

---

# ▶️ Getting Started

Because each workstream is maintained as its own branch, switch to the relevant branch before running its scripts.

```bash
git clone https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project.git
cd Paytm-Fintech-AI-Capstone-Project

git checkout ai_advisory_blockchain
# or
git checkout credit-risk-lending-ml
# or
git checkout payments-fraud-analytics
```

Then follow the branch-specific `README.md` for execution instructions and expected outputs.

---

# ⚠️ Disclaimer

This capstone uses **synthetic/mock data and deterministic baseline logic** for demonstration and academic purposes. Model metrics, investment outputs, risk tiers and anomaly-detection results should not be interpreted as production credit, investment, fraud or financial advice.

A real deployment would require validated production data, regulatory review, robust model validation, fairness testing, security controls, monitoring, explainability, human oversight and appropriate governance.

---

## 👤 Project

**Paytm Fintech AI Capstone Project**

Three workstreams. One fintech ecosystem.

**Investment Intelligence · Credit Risk · Payments Analytics**
