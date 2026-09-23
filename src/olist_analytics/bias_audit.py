"""Reproducible, descriptive Step 5 diagnostics; never infer protected labels."""
from pathlib import Path
from types import SimpleNamespace
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import partial_dependence
from sklearn.metrics import mean_absolute_error

from .daily_forecasting import FEATURES, TEST_START, prepare_daily_sales


def selection_rates(customers, minimum_size=50):
    """Unadjusted state rates for a specified hypothetical binary decision.

    Wilson intervals describe sampling uncertainty in each rate, not proof of
    fairness or a confidence interval for the max/min disparity itself.
    """
    table = customers.groupby("customer_state", dropna=False).agg(
        customers=("selected", "size"), selected=("selected", "sum"))
    table["selection_rate"] = table["selected"] / table["customers"]
    n, rate, z = table["customers"], table["selection_rate"], 1.96
    centre = (rate + z*z/(2*n)) / (1 + z*z/n)
    radius = z * np.sqrt(rate*(1-rate)/n + z*z/(4*n*n)) / (1 + z*z/n)
    table["lower_95"] = (centre - radius).clip(0, 1)
    table["upper_95"] = (centre + radius).clip(0, 1)
    table["included_in_gap"] = (n >= minimum_size) & (table.index != "Unknown")
    supported = table.loc[table["included_in_gap"], "selection_rate"]
    if len(supported) < 2:
        gap = ratio = np.nan
    else:
        gap = float(supported.max() - supported.min())
        ratio = float(supported.min()/supported.max()) if supported.max() > 0 else np.nan
    return table.sort_values("customers", ascending=False), gap, ratio


def latest_customer_states(raw, cutoff):
    """One state per persistent customer, from their latest pre-cutoff order."""
    customers = pd.read_csv(raw / "olist_customers_dataset.csv", dtype="string",
                           usecols=["customer_id", "customer_unique_id", "customer_state"])
    orders = pd.read_csv(raw / "olist_orders_dataset.csv", dtype="string",
                        usecols=["order_id", "customer_id", "order_approved_at"])
    orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"], errors="coerce")
    past = orders.loc[orders["order_approved_at"] < cutoff]
    linked = past.merge(customers, on="customer_id", how="left", validate="one_to_one")
    assert linked["customer_unique_id"].notna().all()
    latest = (linked.sort_values(["order_approved_at", "order_id"])
              .drop_duplicates("customer_unique_id", keep="last"))
    assert latest["order_approved_at"].lt(cutoff).all()
    return latest.set_index("customer_unique_id")[["customer_state"]]


def run_bias_audit(forecasts, daily_forecasts, cluster_profiles, forecast_table,
                   transactions, raw, project_root, cutoff):
    root, raw = Path(project_root), Path(raw)
    tables = root / "reports" / "tables"
    tables.mkdir(parents=True, exist_ok=True)

    # Real PDP/ICE calculations on development inputs, for output week 1.
    model = forecasts.forecast_models[forecasts.chosen_forecast_name]
    inputs = forecast_table[forecasts.forecast_features]
    explanations, curve_rows = {}, []
    for feature in ["lag_1", "mean_last_4"]:
        result = partial_dependence(model, inputs, [feature], method="brute", kind="both",
                                    grid_resolution=15, percentiles=(0.05, 0.95))
        grid, average, individual = result["grid_values"][0], result["average"][0], result["individual"][0]
        np.testing.assert_allclose(average, individual.mean(axis=0))
        explanations[feature] = {"grid": grid, "average": average, "individual": individual}
        curve_rows.extend({"feature": feature, "input_value": x, "week_1_prediction": y}
                          for x, y in zip(grid, average))

    # Schema inspection confirms that these concepts have no direct fields.
    schema = {path.name: pd.read_csv(path, nrows=0).columns.tolist() for path in sorted(raw.glob("*.csv"))}
    availability = pd.DataFrame([
        {"Attribute": name, "Available": "No", "Use": "Cannot audit; do not infer"}
        for name in ["Gender", "Race", "Age", "Income / socioeconomic status"]
    ] + [{"Attribute": "Customer state", "Available": "Yes", "Use": "Geographic comparison only"}])

    # A model cluster alone is not a benefit/denial. Define the consequence first.
    median_spend = cluster_profiles.groupby("segment")["observed_spend"].median().sort_values(ascending=False)
    preferred_segment = int(median_spend.index[0])
    assert len(median_spend) >= 2 and cluster_profiles.index.is_unique
    customers = cluster_profiles.join(latest_customer_states(raw, cutoff), how="left", validate="one_to_one")
    assert len(customers) == len(cluster_profiles)
    customers["customer_state"] = customers["customer_state"].fillna("Unknown")
    customers["selected"] = customers["segment"].eq(preferred_segment)
    states, gap, ratio = selection_rates(customers)
    eligible = states.loc[states["included_in_gap"]]
    geography = {
        "scenario": "Hypothetical offer only to the cluster with higher median recorded spending; no offers sent",
        "preferred_segment": preferred_segment, "customers": len(customers),
        "selected_customers": int(customers["selected"].sum()),
        "unknown_state_customers": int(customers["customer_state"].eq("Unknown").sum()),
        "minimum_state_size": 50, "states_in_gap": len(eligible),
        "customers_in_gap": int(eligible["customers"].sum()),
        "selection_rate_gap": gap, "min_max_selection_ratio": ratio,
        "equalized_odds": None,
        "equalized_odds_reason": "No observed eligibility/benefit label for the hypothetical offer; no protected attributes",
        "protected_group_audit": "Not measurable from supplied data; geographic parity is not protected-group fairness",
    }

    errors = []
    for name, records, actual_column, prediction_column in [
        ("Weekly RF", forecasts.chosen_errors, "actual", "prediction"),
        ("Daily RF", daily_forecasts.predictions, "items", "prediction"),
    ]:
        records = records.copy()
        records["sales_days"] = np.where(records[actual_column] == 0, "Zero sales", "Positive sales")
        records["absolute_error"] = (records[prediction_column] - records[actual_column]).abs()
        records["signed_error"] = records[prediction_column] - records[actual_column]
        for group, rows in records.groupby("sales_days"):
            errors.append({"Model": name, "Sales period": group, "Forecasts": len(rows),
                           "Share (%)": 100*len(rows)/len(records),
                           "MAE": rows["absolute_error"].mean(), "Bias": rows["signed_error"].mean()})
    sales_errors = pd.DataFrame(errors)

    fit_rows = []
    for name, fitted in forecasts.forecast_models.items():
        fit_rows.append({"Model": name, "Unit": "items / product-week",
            "Training MAE": mean_absolute_error(forecast_table[forecasts.forecast_targets], fitted.predict(inputs)),
            "Validation MAE": float(forecasts.ml_ranking.set_index("candidate").loc[name, "validation_mae"]),
            "Test MAE": float(forecasts.test_comparison.set_index("model").loc[name, "test_mae"])})
    daily, _ = prepare_daily_sales(transactions)
    train_errors = []
    for product_id, fitted in daily_forecasts.models.items():
        rows = daily.loc[(daily["product_id"] == product_id) & (daily["date"] < TEST_START)]
        train_errors.extend(np.abs(fitted.predict(rows[FEATURES]) - rows["items"]))
    fit_rows.append({"Model": "Daily Random Forest", "Unit": "items / product-day",
        "Training MAE": float(np.mean(train_errors)),
        "Validation MAE": float(daily_forecasts.ranking.iloc[0]["validation_mae"]),
        "Test MAE": float(daily_forecasts.summary["rf_mae"].mean())})
    fit_review = pd.DataFrame(fit_rows)
    audit = SimpleNamespace(explanations=explanations, curves=pd.DataFrame(curve_rows),
        availability=availability, states=states, geography=geography, sales_errors=sales_errors,
        fit_review=fit_review)
    for name, table in {"pdp": audit.curves, "attribute_availability": availability,
                        "state_selection": states.reset_index(), "sales_errors": sales_errors,
                        "fit_review": fit_review}.items():
        table.to_csv(tables / f"05_{name}.csv", index=False)
    config = {"geography": geography, "schema_columns": schema,
              "explanation": {"tool": "sklearn.inspection.partial_dependence", "kind": "both",
                  "model": forecasts.chosen_forecast_name, "target": "week 1", "features": list(explanations),
                  "reference": "180 development product-origin rows", "method": "brute",
                  "percentiles": [0.05, 0.95], "grid_resolution": 15, "ice_lines_shown": 30,
                  "limitation": "Correlated lags/mean can create unrealistic input combinations; not causal"},
              "state_assignment": "Last approved order before profile cutoff; order_id breaks timestamp ties",
              "profile_cutoff": str(pd.Timestamp(cutoff).date()), "mitigations": "Proposed; not deployed",
              "evaluation_previously_inspected": True}
    (root / "configs" / "step5_bias_audit.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    return audit


def show_model_explanation(audit, figure_directory):
    labels = {"lag_1": "Last week's item sales", "mean_last_4": "Recent four-week average"}
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    for ax, (feature, data) in zip(axes, audit.explanations.items()):
        indices = np.random.default_rng(42).choice(len(data["individual"]), 30, replace=False)
        for j, line in enumerate(data["individual"][indices]):
            ax.plot(data["grid"], line, color="#b0c9de", linewidth=0.7,
                    label="Individual response (ICE)" if j == 0 else None)
        ax.plot(data["grid"], data["average"], color="#174a72", linewidth=3, label="Average response (PDP)")
        ax.set(xlabel=labels[feature], ylabel="Predicted items in week 1", title=labels[feature])
        ax.legend(fontsize=8)
        change = data["average"][-1] - data["average"][0]
        print(f"{labels[feature]}: average prediction changes by {change:+.2f} items from the left to right end of the chart.")
    fig.suptitle("How the weekly Random Forest responds to its inputs")
    fig.tight_layout()
    fig.savefig(Path(figure_directory)/"05_pdp_ice.png", dpi=150, bbox_inches="tight")
    plt.show()


def show_geographic_audit(audit, figure_directory):
    from IPython.display import display
    table = audit.states.loc[audit.states["included_in_gap"]]
    visible = table[["customers", "selected", "selection_rate"]].copy()
    visible["selection_rate"] *= 100
    display(visible.rename(columns={"customers": "Customers", "selected": "Hypothetically selected",
                                    "selection_rate": "Selected (%)"}).round(2))
    g = audit.geography
    print(f"Geographic selection-rate gap: {100*g['selection_rate_gap']:.2f} percentage points; min/max ratio: {g['min_max_selection_ratio']:.2f}.")
    print(f"Comparison covers {g['states_in_gap']} states and {g['customers_in_gap']:,}/{g['customers']:,} customers; unknown state: {g['unknown_state_customers']}.")
    fig, ax = plt.subplots(figsize=(9, 5))
    rates = table["selection_rate"]*100
    ax.barh(table.index, rates, color="#306998", xerr=np.maximum(0, np.array([
        (table["selection_rate"]-table["lower_95"])*100,
        (table["upper_95"]-table["selection_rate"])*100])), capsize=3)
    ax.invert_yaxis()
    ax.set(title="Who would receive a segment-only offer?", xlabel="Selected customers (%) with 95% rate intervals",
           ylabel="Customer state (at least 50 sample customers)")
    fig.tight_layout()
    fig.savefig(Path(figure_directory)/"05_state_selection.png", dpi=150, bbox_inches="tight")
    plt.show()


def markdown_table(table):
    """Small report table without an extra rendering dependency."""
    def cell(value):
        if isinstance(value, (float, np.floating)):
            return "Not measurable" if np.isnan(value) else f"{value:.3f}"
        return str(value).replace("|", "/").replace("\n", " ")
    lines = ["| " + " | ".join(map(str, table.columns)) + " |",
             "| " + " | ".join(["---"]*len(table.columns)) + " |"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in table.itertuples(index=False, name=None)]
    return "\n".join(lines)


def export_bias_report(audit, project_root):
    """Derive only the requested report section from notebook text and results."""
    root = Path(project_root)
    notebook = json.loads((root/"notebooks"/"Final_Project.ipynb").read_text(encoding="utf-8"))
    g = audit.geography
    evidence = {
        "bias5explain": markdown_table(audit.curves.groupby("feature", sort=False).agg(
            first_prediction=("week_1_prediction", "first"), last_prediction=("week_1_prediction", "last")).reset_index())
            + "\n\n![PDP and ICE](figures/05_pdp_ice.png)",
        "bias5limits": markdown_table(audit.fit_review.round(3)) + "\n\n" + markdown_table(audit.sales_errors.round(3)),
        "bias5attributes": markdown_table(audit.availability),
        "bias5geography": markdown_table(audit.states.reset_index().round(4))
            + f"\n\nGeographic rate gap: **{100*g['selection_rate_gap']:.2f} percentage points**. "
            + f"Min/max selection ratio: **{g['min_max_selection_ratio']:.2f}**. "
            + f"Coverage: {g['customers_in_gap']:,}/{g['customers']:,} customers across {g['states_in_gap']} states; unknown: {g['unknown_state_customers']}."
            + "\n\n![Geographic selection rates](figures/05_state_selection.png)",
    }
    section, active = [], False
    for cell in notebook["cells"]:
        if cell["id"] == "56188f84":
            active = True
        elif cell["id"] == "00300ce5":
            break
        if not active:
            continue
        if cell["cell_type"] == "markdown":
            source = "".join(cell["source"]).replace('<a id="step-5"></a>\n\n', '')
            source = source.replace("# Step 5: Critical Thinking, Ethical AI & Bias Auditing\n\n", "")
            section.append(source)
        elif cell["id"] in evidence:
            section.append(evidence[cell["id"]])
    start, end = "<!-- BEGIN GENERATED BIAS AUDIT -->", "<!-- END GENERATED BIAS AUDIT -->"
    generated = start + "\n\n" + "\n\n".join(section) + "\n\n" + end
    path = root/"reports"/"final_report.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else (
        "# Final report\n\nThis report currently contains the requested Step 5 section, generated from the notebook. "
        "Other final-report chapters and the presentation decks remain pending.\n\n")
    if start in existing:
        assert existing.count(start) == existing.count(end) == 1
        before, rest = existing.split(start, 1)
        _, after = rest.split(end, 1)
        output = before + generated + after
    else:
        output = existing.rstrip() + "\n\n" + generated + "\n"
    path.write_text(output, encoding="utf-8")
    print("Saved reports/final_report.md: Bias & Fairness Analysis section.")
