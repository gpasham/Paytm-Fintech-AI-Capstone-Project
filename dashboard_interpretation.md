# Four-Layer Payments Fraud Analytics Dashboard

## Headline layer
Total GMV is **₹382,603**, with an overall success rate of **85.6%**. The strict reconciliation match rate is **90.5%**, where a transaction only matches if it exists in both files and both amount and status are identical. The platform-wide count-based chargeback ratio is **5.1%** (chargeback transactions divided by all ledger transactions).

## Trends layer
The highest daily GMV occurs on **2026-01-11**, at **₹28,284**. Chargebacks are relatively infrequent compared with transaction volume, so their daily movement is better treated as a risk signal than a primary GMV driver. Daily spikes should be investigated alongside merchant and transaction-level details.

## Breakdown layer
**UPI** is the largest GMV-contributing payment method in the dataset. **ecommerce** is the largest merchant category by GMV. These views identify where transaction value is concentrated and therefore where operational monitoring and reconciliation attention may have the greatest impact.

## Details layer
The detail table ranks the top 10 merchants by transaction count and calculates each merchant's count-based chargeback ratio. **6 of the top 10 merchants** exceed the 1% threshold and are conditionally highlighted. These merchants merit closer review because their observed chargeback incidence crosses the specified risk threshold.

## Required metric definitions
- `match_rate` = common transactions with identical amount and status / total ledger transactions.
- `chargeback_ratio` = chargeback transaction count / all transaction count.
- `success_rate` = captured transaction count / all transaction count.
- `total_gmv` = sum of `amount_inr` across all ledger transactions.
- Per-merchant `chargeback_ratio` = that merchant's chargeback count / that merchant's total transaction count.
