# Paytm Fintech AI Capstone — Payments & Fraud Analytics

The project combines Python-based data generation and reconciliation with SQL analytics and a four-layer dashboard covering headline KPIs, trends, payment-method/category breakdowns, and merchant-level details.

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

## Getting Started

### Prerequisites

- Python 3.9+ recommended
- SQLite
- A SQL client capable of executing SQLite-compatible SQL
- Git

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
