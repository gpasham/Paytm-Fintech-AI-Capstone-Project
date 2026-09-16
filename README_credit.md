# Credit Risk & Lending ML

This branch builds a small credit-risk and transaction-anomaly detection pipeline for a Paytm Postpaid-style lending use case. The project includes synthetic applicant data with thin-file customers, supervised default prediction, risk-based pricing, and Isolation Forest anomaly detection.

## Task 6 — Transaction Anomaly Detection

`txn_behaviour.csv` contains 265 transactions, including 15 deliberately seeded anomalies (`txn_id` beginning with `BTXNA`). The behavioural features `txn_hour`, `is_new_device`, and `txn_amount_inr` were standardized using `StandardScaler` and passed to scikit-learn's `IsolationForest(random_state=42)`.

The contamination rate was set to **15 / 265 = 0.0566 (5.66%)**, matching the injected anomaly proportion. Isolation Forest flagged **15 transactions** as anomalous in total, of which **11 of the 15 seeded anomalies were detected**, giving a seeded-anomaly recall of **73.33%**. This is a simple ground-truth recall check because the anomalies were deliberately injected for this exercise.

## Final Model Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC AUC / Anomaly Recall |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 76.00% | 38.89% | 35.00% | 36.84% | ROC AUC: 0.71875 |
| Decision Tree | 67.00% | 24.00% | 30.00% | 26.67% | ROC AUC: 0.53125 |
| Isolation Forest | — | — | — | — | Seeded anomaly recall: 73.33% (11/15) |

### Deployment Recommendation

I would deploy **Logistic Regression** as the primary classifier for Paytm Postpaid, subject to the governance controls above. It achieves higher accuracy (76.00%), precision (38.89%), recall (35.00%), F1 (36.84%), and ROC AUC (0.71875) than the Decision Tree, whose AUC is only 0.53125. The logistic model therefore provides materially better and more interpretable discrimination for default-risk ranking, which is useful for risk-based pricing and credit decisions. Isolation Forest should complement, rather than replace, the classifier by screening transaction behaviour for anomalies, with a 73.33% recall on the seeded anomalies in this exercise.

## Key Output Files

- `generate_data.py` — generates the synthetic applicant and transaction datasets.
- `credit_applicants.csv` — 400 applicant records with an explicit thin-file population.
- `txn_behaviour.csv` — 265 transaction-behaviour records, including 15 seeded anomalies.
- `model_comparison.csv` — Logistic Regression vs Decision Tree metrics.
- `risk_pricing_table.csv` — logistic-probability risk tiers and illustrative pricing bands.
- `roc_comparison.png` — ROC curves for the two classifiers.
- `isolation_forest_results.csv` — transaction-level anomaly flags.
- `isolation_forest_summary.csv` — Isolation Forest recall summary.
