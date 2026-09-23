"""Read-only context counts for Step 1; not a full audit or target-label analysis."""

from pathlib import Path
import json

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def summarize() -> dict:
    raw = PROJECT_ROOT / "data" / "raw" / "olist"
    orders = pd.read_csv(
        raw / "olist_orders_dataset.csv",
        parse_dates=["order_purchase_timestamp", "order_approved_at"],
        dtype={"customer_id": "string", "order_id": "string"},
    )
    customers = pd.read_csv(raw / "olist_customers_dataset.csv", dtype="string")
    items = pd.read_csv(raw / "olist_order_items_dataset.csv", dtype={"product_id": "string"})
    joined = orders.merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id", how="left", validate="one_to_one",
    )
    if joined.customer_unique_id.isna().any() or len(joined) != len(orders):
        raise ValueError("Customer join lost identity or changed order-row count.")
    counts = joined.groupby("customer_unique_id").order_id.nunique()
    approved = joined.loc[joined.order_approved_at.notna()]
    approved_counts = approved.groupby("customer_unique_id").order_id.nunique()
    return {
        "dataset_handle": "olistbr/brazilian-ecommerce/versions/2",
        "scope": "Full-history descriptive counts; not 90-day future-label prevalence or a full audit.",
        "orders": len(orders),
        "unique_customers": len(counts),
        "customers_with_multiple_orders": int((counts > 1).sum()),
        "repeat_customer_pct_full_history": float((counts > 1).mean() * 100),
        "approved_orders": len(approved),
        "customers_with_approved_orders": len(approved_counts),
        "customers_with_multiple_approved_orders": int((approved_counts > 1).sum()),
        "missing_approval_timestamp": int(orders.order_approved_at.isna().sum()),
        "purchase_timestamp_min": str(orders.order_purchase_timestamp.min()),
        "purchase_timestamp_max": str(orders.order_purchase_timestamp.max()),
        "item_rows": len(items),
        "products_with_item_rows": int(items.product_id.nunique()),
        "explicit_quantity_column_present": "quantity" in items.columns,
    }


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
