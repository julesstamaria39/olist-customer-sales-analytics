r"""Check daily-forecast leakage safeguards with changed future sales.

Run from the project folder with ..\.venv\Scripts\python.exe
scripts/check_daily_forecasting.py. Temporary artifacts are isolated and removed.
"""
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from daily_forecasting import FEATURES, TEST_START, prepare_daily_sales, run_daily_forecasting, trend_direction


def main():
    # Include a product that becomes popular only after training: it must not
    # displace a training-period top product, even if future sales are huge.
    rows = []
    for product in range(6):
        for day in pd.date_range("2017-02-01", periods=6-product):
            rows.append({"product_id": f"p{product}", "order_approved_at": day,
                         "order_id": f"order{len(rows)}", "order_item_id": 1})
    original = pd.DataFrame(rows)
    future = pd.DataFrame([
        {"product_id": f"p{i % 6}", "order_approved_at": TEST_START + pd.Timedelta(days=i % 50),
         "order_id": f"future{i}", "order_item_id": 1} for i in range(600)
    ])
    changed = pd.concat([original, future], ignore_index=True)
    daily_a, top_a = prepare_daily_sales(original)
    daily_b, top_b = prepare_daily_sales(changed)
    pd.testing.assert_frame_equal(top_a, top_b)
    assert "p5" not in top_b["product_id"].tolist()
    pd.testing.assert_frame_equal(daily_a[FEATURES], daily_b[FEATURES])
    assert (daily_a["items"] == 0).any(), "Missing dates must be represented as zero sales."
    assert daily_b["items"].sum() == 520  # 20 training + 500 selected-product future items.
    provenance = {"source_manifest": "synthetic test", "versions": {}}
    artifacts = Path(__file__).resolve().parents[1] / "artifacts"
    artifacts.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="daily_check_", dir=artifacts) as directory:
        first = run_daily_forecasting(original, Path(directory) / "original", provenance)
        second = run_daily_forecasting(changed, Path(directory) / "changed", provenance)
        pd.testing.assert_frame_equal(first.ranking, second.ranking)
        np.testing.assert_allclose(first.predictions["prediction"], second.predictions["prediction"])
        np.testing.assert_allclose(first.predictions["benchmark"], second.predictions["benchmark"])
        assert not np.array_equal(first.predictions["items"], second.predictions["items"])
    assert trend_direction(0.2) == "Upward"
    assert trend_direction(-0.2) == "Downward"
    assert trend_direction(0.05) == "Roughly flat"
    print("PASS: changed future sales leave product selection, features, tuning, forecasts, and benchmarks unchanged.")
    print("PASS: zero-sales dates, count reconciliation, split boundaries, trend labels, and model reloads.")


if __name__ == "__main__":
    main()
