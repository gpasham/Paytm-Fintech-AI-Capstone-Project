# Paytm Fintech AI Capstone — Payments & Fraud Analytics

A fintech analytics capstone project focused on **payments performance, reconciliation, transaction risk, and fraud analytics** using a synthetic Paytm-style transaction environment.

The project combines Python-based data generation and reconciliation with SQL analytics and a four-layer dashboard covering headline KPIs, trends, payment-method/category breakdowns, and merchant-level details.

> **Note:** This is an educational/synthetic analytics project. The data and findings should not be interpreted as actual Paytm internal data or production fraud metrics.

## Project Objectives

The `payments-fraud-analytics` branch is designed to answer four broad questions:

1. **How is the payments business performing?**
   - GMV
   - transaction success rate
   - payment-method contribution
   - merchant/category contribution

2. **Where are operational and fraud risks appearing?**
   - chargebacks
   - newly created/burner accounts
   - transaction velocity
   - merchant concentration
   - transaction-level risk scores

3. **Do payment records reconcile correctly?**
   - Compare gateway and ledger records
   - Identify missing or mismatched transactions
   - Compare transaction amounts and statuses

4. **How can the analysis be communicated to decision-makers?**
   - Executive KPI scorecards
   - Daily trend analysis
   - GMV breakdowns
   - Top-merchant detail
   - Risk-oriented SQL queries

## Repository Structure

```text
payments-fraud-analytics/
│
├── README.md
├── analytics_queries.sql
├── dashboard_interpretation.md
│
├── generate_data.py
├── reconcile.py
│
├── gateway.csv
├── ledger.csv
├── merchant_master.csv
├── users.csv
├── paytm_payments.db
│
├── 01_headline_scorecards.png
├── 02_daily_trends.png
├── 03a_gmv_by_payment_method.png
├── 03b_gmv_by_category.png
└── 04_top10_merchants_detail.png
```

The branch currently contains the analytics SQL, Python utilities, synthetic datasets/database, dashboard outputs, and dashboard interpretation. citeturn0view0

## Data Model

The project works with four principal business entities:

### 1. Transactions

The transaction-level data contains fields used for payment performance, reconciliation, and fraud analytics, including:

- transaction ID
- user ID
- merchant ID
- payment method
- transaction timestamp
- transaction amount
- transaction status
- risk score

### 2. Users

User-level information supports customer and account-age analysis, including signup dates used to identify potentially suspicious activity shortly after account creation.

### 3. Merchants

Merchant master data provides merchant identifiers and names, enabling transaction coverage, GMV, and merchant-level analysis.

### 4. Gateway / Ledger Records

The gateway and ledger datasets provide two sides of the payment flow and are used by the reconciliation workflow to identify:

- records present in one system but absent in another
- amount mismatches
- status mismatches
- records that fully match

## Analytics Layer

`analytics_queries.sql` contains six core SQL analyses.

### Q1 — Chargeback Payment Methods

Identifies the payment methods associated with chargeback transactions.

### Q2 — Chargeback Impact

Calculates:

- number of chargeback transactions
- unique users affected
- total chargeback amount

### Q3 — Burner Accounts

Identifies chargeback transactions occurring within the first 30 days of account creation.

This query joins transactions to users and explicitly prevents negative account ages from being treated as valid.

### Q4 — Merchant Coverage

Uses a `LEFT JOIN` to retain merchants even when they have no matching transactions, then ranks merchants by transaction count and amount.

### Q5 — 10-Minute Bucketed Velocity

Groups transactions into floored 10-minute buckets and flags users with at least three transactions in a bucket.

### Q6 — Explicit Rolling 10-Minute Velocity

Uses a self-join to calculate transactions occurring within a rolling 10-minute window from each transaction timestamp.

These queries are implemented in `analytics_queries.sql`. citeturn1view1

## Dashboard

The dashboard is structured as a four-layer decision-support view.

### Layer 1 — Headline Scorecards

Executive-level KPIs include:

- Total GMV
- Overall transaction success rate
- reconciliation match rate
- chargeback ratio

The current dashboard interpretation reports total GMV of **₹382,603**, an overall success rate of **85.6%**, a strict reconciliation match rate of **90.5%**, and a count-based chargeback ratio of **5.1%**. citeturn1view2

### Layer 2 — Daily Trends

Daily GMV and chargeback movement are used to identify unusual periods and potential operational/risk signals.

The current interpretation identifies **2026-01-11** as the highest daily GMV date at **₹28,284**. citeturn1view2

### Layer 3 — GMV Breakdown

The dashboard examines GMV by:

- payment method
- merchant category

The current analysis identifies **UPI** as the largest GMV-contributing payment method and **ecommerce** as the largest merchant category by GMV. citeturn1view2

### Layer 4 — Merchant Detail

The detailed layer focuses on individual merchants and transaction-level patterns so that aggregate signals can be investigated at a more granular level.

## Reconciliation Workflow

`reconcile.py` provides the payment reconciliation component.

The intended workflow is:

```text
Gateway Records ─────┐
                     ├──> Reconciliation ──> Match / Mismatch Analysis
Ledger Records ──────┘
```

A **strict match** requires the transaction to exist in both datasets and have matching amount and status.

This distinction is important because a transaction existing in both systems is not sufficient to conclude that the records are fully reconciled.

## Synthetic Data Generation

`generate_data.py` is used to generate the project's synthetic payment data and database artifacts.

The repository includes:

```text
gateway.csv
ledger.csv
merchant_master.csv
users.csv
paytm_payments.db
```

The generated data supports repeatable experimentation without relying on confidential or proprietary payment records. citeturn0view0turn1view3

## Getting Started

### Prerequisites

- Python 3.9+ recommended
- SQLite
- A SQL client capable of executing SQLite-compatible SQL
- Git

No production Paytm credentials are required for the analytics workflow.

### Clone the repository

```bash
git clone https://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project.git
cd Paytm-Fintech-AI-Capstone-Project
git checkout payments-fraud-analytics
```

### Generate / refresh synthetic data

```bash
python generate_data.py
```

Review the generated CSV files and SQLite database before running downstream analysis.

### Run reconciliation

```bash
python reconcile.py
```

### Run SQL analytics

Using SQLite:

```bash
sqlite3 paytm_payments.db
```

Then:

```sql
.read analytics_queries.sql
```

Alternatively, open `analytics_queries.sql` in any SQLite-compatible database tool.

## Outputs

The branch contains the following visual outputs:

| Output | Purpose |
|---|---|
| `01_headline_scorecards.png` | Executive KPI overview |
| `02_daily_trends.png` | Daily GMV / risk trends |
| `03a_gmv_by_payment_method.png` | GMV contribution by payment method |
| `03b_gmv_by_category.png` | GMV contribution by merchant category |
| `04_top10_merchants_detail.png` | Merchant-level transaction/GMV detail |

The corresponding business interpretation is documented separately in `dashboard_interpretation.md`. citeturn0view0turn1view2

## Key Risk Analytics

The project goes beyond descriptive payment reporting by introducing several practical fraud/risk indicators.

### Chargebacks

Chargebacks are treated as a direct payment-risk signal and analyzed by:

- payment method
- user impact
- total amount
- time trends

### Burner Accounts

A chargeback occurring shortly after account creation can be used as an investigation signal. The project uses a 30-day threshold for this analytical screen.

### Transaction Velocity

Multiple transactions from the same user within a short time window can indicate unusual activity.

Two approaches are implemented:

- fixed 10-minute buckets
- rolling 10-minute windows

The rolling-window approach is more flexible because it evaluates activity relative to each transaction rather than only to fixed clock buckets.

### Merchant Concentration

GMV and transaction counts by merchant help identify where payment activity is concentrated and where operational monitoring may have the greatest impact.

## Decision-Making Framework

The project is designed around a simple analytics-to-action flow:

```text
Raw Payment Data
       ↓
Data Generation / Ingestion
       ↓
Reconciliation
       ↓
SQL Analytics
       ↓
Fraud & Risk Signals
       ↓
Dashboard / Visualization
       ↓
Business Investigation & Action
```

This separates **measurement** from **interpretation**, allowing analysts and decision-makers to trace high-level KPIs back to transaction-level evidence.

## Business Takeaways

Based on the current synthetic dashboard:

- Payment activity is concentrated in a small number of payment methods/categories, creating clear areas for monitoring.
- Chargebacks represent a relatively small share of transaction volume but remain an important risk indicator.
- Reconciliation should be evaluated using both record existence and field-level agreement.
- Daily spikes should be investigated together with merchant, user, and transaction-level data rather than interpreted in isolation.
- Velocity and newly created-account signals can provide useful prioritization features for fraud investigation.

These conclusions are based on the synthetic dataset included in the repository and should not be generalized to real Paytm operations. citeturn1view2

## Technical Skills Demonstrated

- **Python** — synthetic data generation and reconciliation
- **SQL / SQLite** — joins, aggregations, CTEs, date/time calculations, rolling windows
- **Data Analytics** — KPI construction and fraud-risk indicators
- **Data Visualization** — executive dashboards and drill-down analysis
- **Fintech Analytics** — payments, chargebacks, reconciliation, merchant analysis
- **Fraud Analytics** — velocity monitoring and burner-account screening
- **Business Communication** — converting analytical results into actionable interpretations

## Limitations & Future Enhancements

This project is intended as a capstone analytics implementation rather than a production fraud-detection platform.

Potential extensions include:

- machine-learning-based fraud scoring
- anomaly detection
- user behavioral profiling
- merchant risk scoring
- graph-based fraud-ring detection
- real-time transaction streaming
- automated fraud-alert prioritization
- model explainability
- monitoring dashboards with automated alerts
- production-grade data-quality checks
- authentication and access controls

## Repository

The project is available on the `payments-fraud-analytics` branch of the Paytm Fintech AI Capstone repository:

urlPaytm Fintech AI Capstone — payments-fraud-analyticshttps://github.com/gpasham/Paytm-Fintech-AI-Capstone-Project/tree/payments-fraud-analytics

## Disclaimer

This repository is an educational capstone project using synthetic/simulated payment data. It does not represent Paytm's proprietary systems, internal datasets, production fraud models, or actual operational performance.

