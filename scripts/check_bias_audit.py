"""Check parity arithmetic, missing outcomes, and time-safe state assignment."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.bias_audit import latest_customer_states, selection_rates


def main():
    groups = pd.DataFrame({"customer_state": ["A"]*4 + ["B"]*4 + ["C"] + ["Unknown"]*4,
                           "selected": [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]})
    table, gap, ratio = selection_rates(groups, minimum_size=2)
    assert np.isclose(gap, 0.5) and np.isclose(ratio, 1/3)
    assert not table.loc[["C", "Unknown"], "included_in_gap"].any()
    assert table["customers"].sum() == len(groups)
    assert (table["lower_95"] <= table["selection_rate"] + 1e-12).all()
    assert (table["upper_95"] >= table["selection_rate"] - 1e-12).all()
    _, gap, ratio = selection_rates(groups.assign(selected=0), minimum_size=2)
    assert gap == 0 and np.isnan(ratio), "An all-zero selection rate has no defined ratio."
    _, gap, ratio = selection_rates(groups, minimum_size=5)
    assert np.isnan(gap) and np.isnan(ratio), "Insufficient support must not appear perfectly fair."

    # Same persistent customer, different order-specific IDs. A future move must
    # not change the state used at the historical profile cutoff.
    customers = pd.DataFrame({"customer_id": ["c1", "c2", "c3"],
        "customer_unique_id": ["person"]*3, "customer_state": ["SP", "RJ", "PA"]})
    orders = pd.DataFrame({"order_id": ["o1", "o2", "o3"], "customer_id": ["c1", "c2", "c3"],
        "order_approved_at": ["2017-01-01", "2018-03-01", "2018-05-01"]})
    with TemporaryDirectory(prefix="bias_check_", dir=ROOT/"artifacts") as directory:
        raw = Path(directory)
        customers.to_csv(raw/"olist_customers_dataset.csv", index=False)
        orders.to_csv(raw/"olist_orders_dataset.csv", index=False)
        before = latest_customer_states(raw, pd.Timestamp("2018-04-02"))
        assert len(before) == 1 and before.loc["person", "customer_state"] == "RJ"
        customers.loc[2, "customer_state"] = "AM"
        customers.to_csv(raw/"olist_customers_dataset.csv", index=False)
        after = latest_customer_states(raw, pd.Timestamp("2018-04-02"))
        pd.testing.assert_frame_equal(before, after)
    print("PASS: parity gap/ratio, zero denominators, support exclusions, rate intervals, and no future-state leakage.")


if __name__ == "__main__":
    main()
