import pandas as pd


def reconcile_payments(ledger_df, gateway_df):
    """
    Reconcile a ledger DataFrame against a gateway export.

    Returns:
        missing_in_gateway: ledger transactions absent from gateway
        missing_in_ledger: gateway transactions absent from ledger
        amount_mismatches: common transactions whose amounts differ
        status_mismatches: common transactions whose statuses differ
    """
    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    # Set operations identify missing/extra transaction IDs.
    missing_gateway_ids = ledger_ids - gateway_ids
    missing_ledger_ids = gateway_ids - ledger_ids

    missing_in_gateway = ledger_df[
        ledger_df["transaction_id"].isin(missing_gateway_ids)
    ].copy()

    missing_in_ledger = gateway_df[
        gateway_df["transaction_id"].isin(missing_ledger_ids)
    ].copy()

    # Pairwise comparison is performed only for transaction IDs present in both files.
    common_ledger = ledger_df[
        ledger_df["transaction_id"].isin(ledger_ids & gateway_ids)
    ].copy()
    common_gateway = gateway_df[
        gateway_df["transaction_id"].isin(ledger_ids & gateway_ids)
    ].copy()

    merged = pd.merge(
        common_ledger,
        common_gateway,
        on="transaction_id",
        how="inner",
        suffixes=("_ledger", "_gateway"),
    )

    # Amount mismatches with computed difference: gateway amount - ledger amount.
    amount_mismatches = merged[
        merged["amount_inr_ledger"] != merged["amount_inr_gateway"]
    ][[
        "transaction_id",
        "amount_inr_ledger",
        "amount_inr_gateway",
    ]].copy()
    amount_mismatches["difference_inr"] = (
        amount_mismatches["amount_inr_gateway"]
        - amount_mismatches["amount_inr_ledger"]
    )

    status_mismatches = merged[
        merged["status_ledger"] != merged["status_gateway"]
    ][[
        "transaction_id",
        "status_ledger",
        "status_gateway",
    ]].copy()

    return (
        missing_in_gateway.sort_values("transaction_id").reset_index(drop=True),
        missing_in_ledger.sort_values("transaction_id").reset_index(drop=True),
        amount_mismatches.sort_values("transaction_id").reset_index(drop=True),
        status_mismatches.sort_values("transaction_id").reset_index(drop=True),
    )


if __name__ == "__main__":
    ledger = pd.read_csv("ledger.csv")
    gateway = pd.read_csv("gateway_export.csv")

    missing_gateway, missing_ledger, amount_mismatches, status_mismatches = (
        reconcile_payments(ledger, gateway)
    )

    print("Reconciliation results")
    print("----------------------")
    print(f"Missing in gateway: {len(missing_gateway)}")
    print(f"Missing in ledger (extra in gateway): {len(missing_ledger)}")
    print(f"Amount mismatches: {len(amount_mismatches)}")
    print(f"Status mismatches: {len(status_mismatches)}")

    print("\nAmount mismatches:")
    print(amount_mismatches.to_string(index=False))

    print("\nStatus mismatches:")
    print(status_mismatches.to_string(index=False))
