"""Calendar-only daily Random Forest experiment for notebook Section 4.9.

No lagged sales or rolling averages are model inputs. All settings, ranking
rules, and dates are fixed here before evaluation. The evaluation period has
already appeared in earlier analysis, so this is a historical backtest.
"""
from pathlib import Path
from types import SimpleNamespace
import json

import joblib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import ParameterGrid


START = pd.Timestamp("2017-01-02")
VALIDATION_START = pd.Timestamp("2018-01-01")
TEST_START = pd.Timestamp("2018-04-02")
END = pd.Timestamp("2018-07-23")  # Exclusive: avoid the dataset's incomplete tail.
FEATURES = ["day_number", "month", "day_of_month", "day_of_week"]
GRID = {"max_depth": [3, 6], "min_samples_leaf": [7, 14]}
TREND_WINDOW = 28
TREND_THRESHOLD = 0.1  # Items/day, a descriptive rule, not significance.


def prepare_daily_sales(transactions):
    """Rank products on training rows, then include every date for those IDs."""
    assert not transactions.duplicated(["order_id", "order_item_id"]).any()
    items = transactions[["product_id", "order_approved_at"]].copy()
    items["date"] = pd.to_datetime(items["order_approved_at"]).dt.normalize()
    items = items.loc[(items["date"] >= START) & (items["date"] < END)]
    training_items = items.loc[items["date"] < VALIDATION_START]
    top = (training_items.groupby("product_id").size().rename("training_items")
           .reset_index().sort_values(["training_items", "product_id"], ascending=[False, True])
           .head(5).reset_index(drop=True))
    assert len(top) == 5, "Need at least five products in the training period."
    top["product"] = [f"Daily product {rank}" for rank in range(1, 6)]
    dates = pd.date_range(START, END, inclusive="left")
    grid = pd.MultiIndex.from_product([top["product_id"], dates], names=["product_id", "date"])
    daily = (items.groupby(["product_id", "date"]).size().reindex(grid, fill_value=0)
             .rename("items").reset_index())
    daily["day_number"] = (daily["date"] - START).dt.days
    daily["month"] = daily["date"].dt.month
    daily["day_of_month"] = daily["date"].dt.day
    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["split"] = np.select(
        [daily["date"] < VALIDATION_START, daily["date"] < TEST_START],
        ["Train", "Validation"], default="Test")
    assert not daily.duplicated(["product_id", "date"]).any()
    assert daily["items"].sum() == items["product_id"].isin(top["product_id"]).sum()
    assert daily.groupby("product_id").size().eq(len(dates)).all()
    for earlier, later in [("Train", "Validation"), ("Validation", "Test")]:
        assert daily.loc[daily["split"] == earlier, "date"].max() < daily.loc[daily["split"] == later, "date"].min()
    return daily, top


def trend_direction(change):
    """Label a change in average items/day using the predeclared tolerance."""
    if change > TREND_THRESHOLD:
        return "Upward"
    if change < -TREND_THRESHOLD:
        return "Downward"
    return "Roughly flat"


def run_daily_forecasting(transactions, project_root, provenance):
    """Tune on validation, refit on train+validation, then score fixed models."""
    root = Path(project_root)
    daily, top = prepare_daily_sales(transactions)
    trials = []
    for candidate, params in enumerate(ParameterGrid(GRID)):
        for product_id in top["product_id"]:
            product = daily.loc[daily["product_id"] == product_id]
            train = product.loc[product["split"] == "Train"]
            valid = product.loc[product["split"] == "Validation"]
            model = RandomForestRegressor(**params, n_estimators=100, random_state=42, n_jobs=1)
            model.fit(train[FEATURES], train["items"])
            trials.append({"candidate": candidate, **params, "product_id": product_id,
                           "validation_mae": mean_absolute_error(valid["items"], model.predict(valid[FEATURES]))})
    tuning = pd.DataFrame(trials)
    ranking = (tuning.groupby(["candidate", "max_depth", "min_samples_leaf"], as_index=False)
               ["validation_mae"].mean().sort_values(["validation_mae", "candidate"]))
    selected = ranking.iloc[0]
    params = {key: int(selected[key]) for key in GRID}
    models, prediction_tables, summary_rows = {}, [], []
    for row in top.itertuples(index=False):
        product = daily.loc[daily["product_id"] == row.product_id]
        development = product.loc[product["date"] < TEST_START]
        test = product.loc[product["split"] == "Test"].copy()
        assert development["date"].max() < test["date"].min()
        model = RandomForestRegressor(**params, n_estimators=100, random_state=42, n_jobs=1)
        model.fit(development[FEATURES], development["items"])
        models[row.product_id] = model
        test["prediction"] = model.predict(test[FEATURES])
        test["benchmark"] = development.tail(TREND_WINDOW)["items"].mean()
        test["product"] = row.product
        first, last = test.head(TREND_WINDOW), test.tail(TREND_WINDOW)
        predicted_change = last["prediction"].mean() - first["prediction"].mean()
        actual_change = last["items"].mean() - first["items"].mean()
        summary_rows.append({
            "product": row.product, "product_id": row.product_id,
            "training_items": row.training_items,
            "predicted_start": first["prediction"].mean(), "predicted_end": last["prediction"].mean(),
            "predicted_change": predicted_change, "predicted_trend": trend_direction(predicted_change),
            "actual_start": first["items"].mean(), "actual_end": last["items"].mean(),
            "actual_change": actual_change, "actual_trend": trend_direction(actual_change),
            "rf_mae": mean_absolute_error(test["items"], test["prediction"]),
            "benchmark_mae": mean_absolute_error(test["items"], test["benchmark"]),
            "zero_sales_share": test["items"].eq(0).mean(),
        })
        prediction_tables.append(test)
    predictions = pd.concat(prediction_tables, ignore_index=True)
    summary = pd.DataFrame(summary_rows)
    splits = daily.groupby("split", sort=False).agg(
        start=("date", "min"), end=("date", "max"), days=("date", "nunique"), rows=("date", "size"))
    model_path = root / "models" / "daily_random_forest.joblib"
    config_path = root / "configs" / "step4_daily_forecast.json"
    table_directory = root / "reports" / "tables"
    for directory in [model_path.parent, config_path.parent, table_directory]:
        directory.mkdir(parents=True, exist_ok=True)
    bundle = {"models": models, "features": FEATURES, "date_origin": str(START.date()),
              "forecast_origin": str(TEST_START.date()), "selected_products": top,
              "target": "recorded item rows by approval date", "parameters": params}
    joblib.dump(bundle, model_path)
    loaded = joblib.load(model_path)
    for product_id, model in loaded["models"].items():
        rows = predictions.loc[predictions["product_id"] == product_id]
        np.testing.assert_allclose(model.predict(rows[loaded["features"]]), rows["prediction"])
    for name, table in {"products": top, "splits": splits.reset_index(), "tuning": tuning,
                        "ranking": ranking, "predictions": predictions, "trends": summary}.items():
        table.to_csv(table_directory / f"04_daily_{name}.csv", index=False)
    config = {
        "seed": 42, "n_estimators": 100, "n_jobs": 1, "features": FEATURES, "grid": GRID,
        "selected_parameters": params, "selection_metric": "mean validation MAE across five products",
        "product_selection": "top five training-period item counts; product_id breaks ties",
        "selected_products": top["product_id"].tolist(), "start": str(START.date()),
        "validation_start": str(VALIDATION_START.date()), "test_start": str(TEST_START.date()),
        "end_exclusive": str(END.date()), "refit": "train + validation, once before test",
        "trend_window_days": TREND_WINDOW, "trend_threshold_items_per_day": TREND_THRESHOLD,
        "trend_rule": "last 28 test days mean minus first 28 test days mean; predicted and actual separately",
        "benchmark": "fixed mean of last 28 pre-test days, separately per product; not an ML candidate",
        "evaluation_previously_inspected": True, "source_manifest": provenance["source_manifest"],
        "versions": provenance["versions"], "reload_checks": "passed",
        "limits": "Historical backtest, not unseen-data proof. Calendar-only RF cannot extrapolate a sustained time trend. Zero recorded sales do not prove zero demand or availability.",
    }
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return SimpleNamespace(summary=summary, predictions=predictions, products=top,
                           splits=splits, ranking=ranking, models=models)


def show_daily_results(results, figure_directory):
    """Display short tables, raw daily forecasts, and observed/predicted direction."""
    from IPython.display import display

    visible = results.summary[["product", "predicted_start", "predicted_end", "predicted_trend",
                               "actual_trend", "rf_mae", "benchmark_mae"]].rename(columns={
        "product": "Product", "predicted_start": "Predicted items/day: start",
        "predicted_end": "Predicted items/day: end", "predicted_trend": "Predicted trend",
        "actual_trend": "Actual trend", "rf_mae": "RF error", "benchmark_mae": "Average-rule error"})
    display(visible.round(2))
    summary = results.summary
    agrees = summary["predicted_trend"].eq(summary["actual_trend"]).sum()
    rf_error, reference_error = summary["rf_mae"].mean(), summary["benchmark_mae"].mean()
    print(f"Trend direction matched for {agrees}/5 products. Average daily error: RF {rf_error:.2f}; average rule {reference_error:.2f} items.")
    print("RF has lower error than the comparison rule." if rf_error < reference_error
          else "RF does not beat the comparison rule overall; use it cautiously for planning.")
    fig, axes = plt.subplots(3, 2, figsize=(13, 10))
    for ax, row in zip(axes.flat, results.products.itertuples(index=False)):
        data = results.predictions.loc[results.predictions["product_id"] == row.product_id]
        ax.plot(data["date"], data["items"], color="#777777", alpha=0.65, linewidth=1, label="Actual daily sales")
        ax.plot(data["date"], data["prediction"], color="#306998", linewidth=1.7, label="RF daily prediction")
        ax.set(title=f"{row.product} | ID: {row.product_id[:8]}...", ylabel="Items per day", ylim=(0, None))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.legend(fontsize=8)
        ax.grid(alpha=0.15)
    ax = axes.flat[-1]
    y = np.arange(len(summary))
    ax.barh(y - 0.18, summary["predicted_change"], height=0.35, color="#306998", label="Predicted change")
    ax.barh(y + 0.18, summary["actual_change"], height=0.35, color="#777777", label="Actual change")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.axvspan(-TREND_THRESHOLD, TREND_THRESHOLD, color="gray", alpha=0.1)
    ax.set_yticks(y, summary["product"])
    ax.invert_yaxis()
    ax.set(title="Direction: left = down, right = up", xlabel="Change in average items/day (last 28 vs first 28 days)")
    ax.legend(fontsize=8)
    fig.suptitle("Daily sales: fixed forecasts made on 2 April 2018", fontsize=14)
    fig.tight_layout()
    directory = Path(figure_directory)
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / "04_daily_sales_trends.png", dpi=150, bbox_inches="tight")
    plt.show()
