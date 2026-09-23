"""Forecasting utilities for the single capstone notebook.

Keep tuning loops, diagnostics, charts, and artifact checks here so the notebook
can focus on the question, results, and business interpretation. Dates, grids,
ML-only selection, and benchmark comparisons match the reviewed Step 4 method.
"""
from pathlib import Path
from types import SimpleNamespace
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import threadpoolctl
from sklearn.base import clone
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance

def run_forecasting(forecast_table, transactions, chosen_products, *, history_start,
                    features, targets, raw_directory, seed=42):
    """Fit the reviewed grids, select ML by validation, and reproduce later results.

    Three mature-target folds: Oct 2 / Nov 6 2017 and Jan 1 2018.
    Evaluation origins: Apr 2-Jun 25 2018; final targets end Jul 23.
    This period was inspected before the user requested ML-only selection.
    Baselines remain benchmarks, and all diagnostic outputs use fixed settings.
    """
    SEED = seed
    forecast_features = features
    forecast_targets = targets
    consolidated_df = transactions
    sales_start = history_start
    raw = Path(raw_directory)

    assert forecast_features == ["lag_1", "lag_2", "lag_3", "lag_4", "mean_last_4"]
    assert not set(forecast_features) & set(forecast_targets + ["item_count", "product_id"])
    validation_starts = pd.to_datetime(["2017-10-02", "2017-11-06", "2018-01-01"])
    test_start = pd.Timestamp("2018-04-02")
    last_test_origin = pd.Timestamp("2018-06-25")
    test_outcome_end = last_test_origin + pd.Timedelta(weeks=4)
    forecast_candidates = {}
    for family, grid in [
        ("Decision tree", {"max_depth": [2, 4, None], "min_samples_leaf": [3, 8]}),
        ("Random forest", {"max_depth": [3, 6, None], "min_samples_leaf": [2, 5]}),
    ]:
        for number, params in enumerate(ParameterGrid(grid)):
            model = (DecisionTreeRegressor(**params, random_state=SEED) if family == "Decision tree"
                     else RandomForestRegressor(**params, n_estimators=100, random_state=SEED, n_jobs=2))
            forecast_candidates[f"{family} {number+1}"] = {"family": family, "model": model}

    fold_rows = []
    for start in validation_starts:
        train = forecast_table.loc[forecast_table["week_start"] + pd.Timedelta(weeks=4) <= start]
        valid = forecast_table.loc[(forecast_table["week_start"] >= start)
                                  & (forecast_table["week_start"] < start + pd.Timedelta(weeks=4))]
        assert len(train) > 0 and len(valid) == 20
        assert train["week_start"].max() + pd.Timedelta(weeks=4) <= valid["week_start"].min()
        assert valid["week_start"].max() + pd.Timedelta(weeks=4) <= test_start
        fold_rows.append({"validation_start": start, "training_rows": len(train), "validation_rows": len(valid),
                          "last_train_origin": train["week_start"].max(),
                          "validation_outcomes_end": valid["week_start"].max() + pd.Timedelta(weeks=4)})
    forecast_cv_rows = []
    for start in validation_starts:
        train = forecast_table.loc[forecast_table["week_start"] + pd.Timedelta(weeks=4) <= start]
        valid = forecast_table.loc[(forecast_table["week_start"] >= start)
                                  & (forecast_table["week_start"] < start + pd.Timedelta(weeks=4))]
        actual = valid[forecast_targets].to_numpy(dtype=float)
        predictions = {
            "Last week": np.repeat(valid[["lag_1"]].to_numpy(), 4, axis=1),
            "Four-week mean": np.repeat(valid[["mean_last_4"]].to_numpy(), 4, axis=1),
        }
        for name, candidate in forecast_candidates.items():
            fitted = clone(candidate["model"]).fit(train[forecast_features], train[forecast_targets])
            predictions[name] = fitted.predict(valid[forecast_features])
        for name, prediction in predictions.items():
            forecast_cv_rows.append({"candidate": name, "validation_start": start,
                "family": forecast_candidates[name]["family"] if name in forecast_candidates else "Baseline",
                "mae": mean_absolute_error(actual, prediction),
                "bias": float(np.mean(prediction - actual))})
    forecast_cv = pd.DataFrame(forecast_cv_rows)
    forecast_ranking = forecast_cv.groupby(["candidate", "family"], as_index=False).agg(
        validation_mae=("mae", "mean"), fold_mae_std=("mae", "std"), validation_bias=("bias", "mean"),
    ).sort_values(["validation_mae", "candidate"])
    best_by_family = forecast_ranking.drop_duplicates("family")
    ml_ranking = forecast_ranking.loc[forecast_ranking["family"] != "Baseline"].copy()
    baseline_ranking = forecast_ranking.loc[forecast_ranking["family"] == "Baseline"].copy()
    chosen_forecast_name = ml_ranking.iloc[0]["candidate"]
    assert chosen_forecast_name in forecast_candidates
    chosen_baseline_name = best_by_family.loc[best_by_family["family"] == "Baseline", "candidate"].iloc[0]
    chosen_ml_names = best_by_family.loc[best_by_family["family"] != "Baseline", "candidate"].tolist()

    chosen_settings = pd.DataFrame([
        {"candidate": name, "max_depth": forecast_candidates[name]["model"].max_depth,
         "min_samples_leaf": forecast_candidates[name]["model"].min_samples_leaf,
         "trees": getattr(forecast_candidates[name]["model"], "n_estimators", 1)}
        for name in chosen_ml_names
    ])
    # Reproduce the existing later-period evaluation with unchanged models and settings.
    later_items = consolidated_df.loc[
        (consolidated_df["order_approved_at"] >= sales_start)
        & (consolidated_df["order_approved_at"] < test_outcome_end)
        & consolidated_df["product_id"].isin(chosen_products["product_id"])
    ].copy()
    later_items["week_start"] = later_items["order_approved_at"].dt.to_period("W-SUN").dt.start_time
    later_weeks = pd.date_range(sales_start, test_outcome_end, freq="W-MON", inclusive="left")
    later_grid = pd.MultiIndex.from_product([chosen_products["product_id"], later_weeks], names=["product_id", "week_start"])
    later_weekly = (later_items.groupby(["product_id", "week_start"]).size().reindex(later_grid, fill_value=0)
                    .rename("item_count").reset_index().sort_values(["product_id", "week_start"]))
    later_counts = later_weekly.groupby("product_id")["item_count"]
    for lag in [1, 2, 3, 4]:
        later_weekly[f"lag_{lag}"] = later_counts.shift(lag)
    later_weekly["mean_last_4"] = later_counts.transform(lambda counts: counts.shift(1).rolling(4).mean())
    for horizon in range(1, 5):
        later_weekly[f"target_week_{horizon}"] = later_counts.shift(-(horizon - 1))
    forecast_test = later_weekly.loc[later_weekly["week_start"].between(test_start, last_test_origin)].copy()
    assert len(forecast_test) == 65 and forecast_test[forecast_features + forecast_targets].notna().all().all()
    assert forecast_table["week_start"].max() + pd.Timedelta(weeks=4) <= forecast_test["week_start"].min()

    # Reconcile the rebuilt development portion with Step 3 before scoring.
    rebuilt = later_weekly.set_index(["product_id", "week_start"])
    original = forecast_table.set_index(["product_id", "week_start"])
    assert np.allclose(rebuilt.loc[original.index, forecast_features + forecast_targets], original[forecast_features + forecast_targets])
    forecast_models = {}
    test_predictions = {
        "Last week": np.repeat(forecast_test[["lag_1"]].to_numpy(), 4, axis=1),
        "Four-week mean": np.repeat(forecast_test[["mean_last_4"]].to_numpy(), 4, axis=1),
    }
    for name in chosen_ml_names:
        fitted = clone(forecast_candidates[name]["model"]).fit(forecast_table[forecast_features], forecast_table[forecast_targets])
        forecast_models[name] = fitted
        test_predictions[name] = fitted.predict(forecast_test[forecast_features])
    test_actual = forecast_test[forecast_targets].to_numpy(dtype=float)
    test_comparison = pd.DataFrame([
        {"model": name, "test_mae": mean_absolute_error(test_actual, predictions),
         "test_rmse": float(np.sqrt(np.mean((predictions-test_actual)**2))),
         "test_bias": float(np.mean(predictions-test_actual)), "selected_ml": name == chosen_forecast_name,
         "role": "ML candidate" if name in forecast_models else "Benchmark only"}
        for name, predictions in test_predictions.items()
    ])
    baseline_mae = test_comparison.set_index("model").loc[chosen_baseline_name, "test_mae"]
    test_comparison["mae_reduction_vs_baseline_pct"] = (
        100 * (baseline_mae - test_comparison["test_mae"]) / baseline_mae if baseline_mae > 0 else np.nan
    )
    forecast_error_rows = []
    for name, predictions in test_predictions.items():
        for row, (_, record) in enumerate(forecast_test.iterrows()):
            for horizon in range(4):
                actual, prediction = test_actual[row, horizon], predictions[row, horizon]
                forecast_error_rows.append({"model": name, "product_id": record["product_id"],
                    "origin": record["week_start"], "horizon": horizon+1,
                    "actual": actual, "prediction": prediction,
                    "absolute_error": abs(prediction-actual), "signed_error": prediction-actual})
    forecast_errors = pd.DataFrame(forecast_error_rows)
    chosen_errors = forecast_errors.loc[forecast_errors["model"] == chosen_forecast_name]
    horizon_errors = chosen_errors.groupby("horizon").agg(mae=("absolute_error", "mean"), bias=("signed_error", "mean"))
    product_errors = chosen_errors.groupby("product_id").agg(mae=("absolute_error", "mean"), bias=("signed_error", "mean"),
                                                             mean_actual=("actual", "mean"))
    origin_errors = chosen_errors.groupby("origin")["absolute_error"].mean()
    from sklearn.inspection import permutation_importance

    explanation_rows = []
    for start in validation_starts:
        train = forecast_table.loc[forecast_table["week_start"] + pd.Timedelta(weeks=4) <= start]
        valid = forecast_table.loc[(forecast_table["week_start"] >= start)
                                  & (forecast_table["week_start"] < start + pd.Timedelta(weeks=4))]
        explanation_model = clone(forecast_candidates[chosen_forecast_name]["model"]).fit(
            train[forecast_features], train[forecast_targets])
        shuffled = permutation_importance(explanation_model, valid[forecast_features], valid[forecast_targets],
            scoring="neg_mean_absolute_error", n_repeats=10, random_state=SEED, n_jobs=1)
        for feature, effect, spread in zip(forecast_features, shuffled.importances_mean, shuffled.importances_std):
            explanation_rows.append({"feature": feature, "validation_start": start,
                                     "mae_increase": effect, "shuffle_std": spread})
    explanation_folds = pd.DataFrame(explanation_rows)
    explanation_summary = explanation_folds.groupby("feature").agg(
        mean_mae_increase=("mae_increase", "mean"),
        min_fold_effect=("mae_increase", "min"), max_fold_effect=("mae_increase", "max"),
    ).sort_values("mean_mae_increase")
    product_ids = chosen_products["product_id"].tolist()
    product_aliases = [f"Product {i+1}" for i in range(len(product_ids))]

    # Add category labels only after forecasting, for interpreting the results.
    product_context = pd.read_csv(raw / "olist_products_dataset.csv",
                                  usecols=["product_id", "product_category_name"], dtype="string")
    category_translation = pd.read_csv(raw / "product_category_name_translation.csv", dtype="string")
    product_context = product_context.merge(category_translation, on="product_category_name",
                                             how="left", validate="many_to_one")

    # A target week appears in several overlapping forecasts; count its actual sales once.
    business_forecasts = chosen_errors.copy()
    business_forecasts["target_week"] = pd.to_datetime(business_forecasts["origin"]) + pd.to_timedelta(
        7 * (business_forecasts["horizon"] - 1), unit="D")
    assert business_forecasts.groupby(["product_id", "target_week"])["actual"].nunique().eq(1).all()
    unique_actual_weeks = business_forecasts.drop_duplicates(["product_id", "target_week"])
    product_business = unique_actual_weeks.groupby("product_id").agg(
        recorded_items=("actual", "sum"), observed_weeks=("actual", "size"),
        zero_sales_weeks=("actual", lambda values: (values == 0).sum()),
        median_weekly_items=("actual", "median"),
    ).join(product_errors[["mae", "bias"]]).reset_index()
    product_business = product_business.merge(product_context, on="product_id", how="left", validate="one_to_one")
    product_business["category"] = product_business["product_category_name_english"].fillna("Unknown")
    alias_map = dict(zip(product_ids, product_aliases))
    product_business["product"] = product_business["product_id"].map(alias_map)
    product_business["selected_product_sales_share_pct"] = (
        100 * product_business["recorded_items"] / product_business["recorded_items"].sum())
    product_business = product_business.sort_values("product")
    assert len(product_business) == 5 and product_business["observed_weeks"].eq(16).all()

    planning_rows = []
    for product_id in product_ids:
        info = product_business.loc[product_business["product_id"] == product_id].iloc[0]
        details = chosen_errors.loc[(chosen_errors["origin"] == test_start)
            & (chosen_errors["product_id"] == product_id)].sort_values("horizon")
        feature_row = forecast_test.loc[(forecast_test["week_start"] == test_start)
            & (forecast_test["product_id"] == product_id)].iloc[0]
        planning_rows.append({"forecast_date": test_start, "product": info["product"], "product_id": product_id,
            "category": info["category"], "past_four_week_items": sum(feature_row[f"lag_{h}"] for h in range(1,5)),
            **{f"ml_week_{h}": details.loc[details["horizon"] == h,"prediction"].iloc[0] for h in range(1,5)},
            "ml_four_week_total": details["prediction"].sum(), "actual_four_week_total": details["actual"].sum()})
    planning_table = pd.DataFrame(planning_rows)

    return SimpleNamespace(
        forecast_features=forecast_features,
        forecast_targets=forecast_targets,
        validation_starts=validation_starts,
        test_start=test_start,
        last_test_origin=last_test_origin,
        test_outcome_end=test_outcome_end,
        forecast_candidates=forecast_candidates,
        fold_rows=fold_rows,
        forecast_cv=forecast_cv,
        forecast_ranking=forecast_ranking,
        ml_ranking=ml_ranking,
        baseline_ranking=baseline_ranking,
        chosen_forecast_name=chosen_forecast_name,
        chosen_baseline_name=chosen_baseline_name,
        chosen_ml_names=chosen_ml_names,
        chosen_settings=chosen_settings,
        forecast_test=forecast_test,
        forecast_models=forecast_models,
        test_predictions=test_predictions,
        test_actual=test_actual,
        test_comparison=test_comparison,
        forecast_errors=forecast_errors,
        chosen_errors=chosen_errors,
        horizon_errors=horizon_errors,
        product_errors=product_errors,
        origin_errors=origin_errors,
        explanation_folds=explanation_folds,
        explanation_summary=explanation_summary,
        product_business=product_business,
        product_ids=product_ids,
        product_aliases=product_aliases,
        planning_table=planning_table,
        chosen_products=chosen_products,
    )

def plot_errors(results, figure_directory):
    """Compare two trained models and two benchmarks on matching later rows."""
    table = results.test_comparison.copy()
    labels = [name.replace(" 2", "") + (" (selected ML)" if name == results.chosen_forecast_name
              else " (benchmark)" if name not in results.forecast_models else "") for name in table["model"]]
    colors = ["#306998" if name in results.forecast_models else "#b0b0b0" for name in table["model"]]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    bars = ax.barh(labels, table["test_mae"], color=colors)
    ax.bar_label(bars, fmt="%.2f", padding=4)
    ax.set(title="Forecast error: lower is better", xlabel="Average error in weekly item counts",
           xlim=(0, table["test_mae"].max()*1.2))
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(Path(figure_directory)/"04_forecast_simple_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()


def plot_product_forecasts(results, figure_directory):
    """Show the first evaluation date for all products, without cherry-picking."""
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for ax, product_id in zip(axes.flat, results.product_ids):
        info = results.product_business.loc[results.product_business["product_id"] == product_id].iloc[0]
        rows = results.chosen_errors.loc[(results.chosen_errors["origin"] == results.test_start)
            & (results.chosen_errors["product_id"] == product_id)].sort_values("horizon")
        ax.plot(rows["horizon"], rows["actual"], "o-", color="#333333", label="What happened")
        ax.plot(rows["horizon"], rows["prediction"], "o--", color="#306998", label="Random Forest forecast")
        ax.set(title=f"{info['product']}: {info['category'].replace('_', ' ')}", xlabel="Weeks ahead",
               ylabel="Item counts", xticks=[1,2,3,4], ylim=(0,None))
        ax.legend(fontsize=7)
        ax.grid(alpha=0.2)
    axes.flat[-1].axis("off")
    axes.flat[-1].text(0, 0.85, "Blue: what the model expected\nBlack: what actually happened\n\nOne historical forecast date.\nEach panel has its own scale.\nForecasts are not stock-order instructions.",
                       va="top", fontsize=11, transform=axes.flat[-1].transAxes)
    fig.suptitle(f"Four-week forecasts made on {results.test_start:%d %B %Y}", fontsize=14)
    fig.tight_layout()
    fig.savefig(Path(figure_directory)/"04_ml_product_forecasts.png", dpi=150, bbox_inches="tight")
    plt.show()


def plot_input_reliance(results, figure_directory):
    """Show validation shuffling effects; these are not causal effects."""
    table = results.explanation_summary
    labels = {"lag_1": "Last week's sales", "lag_2": "Two weeks ago", "lag_3": "Three weeks ago",
              "lag_4": "Four weeks ago", "mean_last_4": "Recent four-week average"}
    fig, ax = plt.subplots(figsize=(8, 3.5))
    effects = table["mean_mae_increase"]
    spread = np.vstack([effects-table["min_fold_effect"], table["max_fold_effect"]-effects])
    ax.barh([labels[f] for f in table.index], effects, xerr=spread, color="#306998", capsize=3)
    ax.set(title="Which inputs does the model rely on?", xlabel="Extra forecast error when an input is shuffled")
    ax.axvline(0, color="black", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(Path(figure_directory)/"04_forecast_input_reliance.png", dpi=150, bbox_inches="tight")
    plt.show()


def save_results(results, clustering, project_root, provenance, elapsed_seconds):
    """Save both tasks and verify reloads; keep exact provenance and policy history."""
    project_root = Path(project_root)
    model_directory = project_root / "models"
    result_directory = project_root / "reports" / "tables"
    config_directory = project_root / "configs"
    processed_directory = project_root / "data" / "processed"
    for directory in [model_directory, result_directory, config_directory, processed_directory]:
        directory.mkdir(parents=True, exist_ok=True)
    SEED = 42
    cluster_X = clustering["spaces"]["Selected features"]
    configuration = provenance
    finalists = clustering["finalists"]
    cluster_fits = clustering["fits"]
    cluster_preparation = clustering["preparation"]
    cluster_pca = clustering["pca"]
    selected_features = clustering["features"]
    cluster_customers = clustering["customers"]
    chosen_cluster_id = clustering["selected"]
    cluster_spaces = clustering["spaces"]
    cluster_comparison = clustering["trials"]
    stability_results = clustering["stability"]
    segment_summary = clustering["summary"]
    cluster_profiles = clustering["profiles"]
    score_rows = clustering["score_rows"]
    common_rows = clustering["common_rows"]
    rfm_common_silhouette = clustering["reference_silhouette"]
    segmentation_stable = clustering["stable"]
    rfm_spend_median = clustering["spend_median"]
    profile_cutoff = clustering["cutoff"]
    selection_end = clustering["product_selection_end"]
    forecast_features = results.forecast_features
    forecast_targets = results.forecast_targets
    validation_starts = results.validation_starts
    test_start = results.test_start
    last_test_origin = results.last_test_origin
    test_outcome_end = results.test_outcome_end
    forecast_candidates = results.forecast_candidates
    fold_rows = results.fold_rows
    forecast_cv = results.forecast_cv
    forecast_ranking = results.forecast_ranking
    ml_ranking = results.ml_ranking
    baseline_ranking = results.baseline_ranking
    chosen_forecast_name = results.chosen_forecast_name
    chosen_baseline_name = results.chosen_baseline_name
    chosen_ml_names = results.chosen_ml_names
    chosen_settings = results.chosen_settings
    forecast_test = results.forecast_test
    forecast_models = results.forecast_models
    test_predictions = results.test_predictions
    test_actual = results.test_actual
    test_comparison = results.test_comparison
    forecast_errors = results.forecast_errors
    chosen_errors = results.chosen_errors
    horizon_errors = results.horizon_errors
    product_errors = results.product_errors
    origin_errors = results.origin_errors
    explanation_folds = results.explanation_folds
    explanation_summary = results.explanation_summary
    product_business = results.product_business
    product_ids = results.product_ids
    product_aliases = results.product_aliases
    planning_table = results.planning_table
    chosen_products = results.chosen_products
    saved_cluster_paths = []
    for _, row in finalists.iterrows():
        trial_id = row["trial"]
        fitted = cluster_fits[trial_id]
        bundle = {"preparation": cluster_preparation, "pca": cluster_pca,
                  "features": selected_features, "representation": fitted["representation"],
                  "model": fitted["model"], "customer_ids": cluster_customers.index.to_list(),
                  "labels": fitted["labels"], "selected": trial_id == chosen_cluster_id}
        model_path = model_directory / f"{trial_id}.joblib"
        joblib.dump(bundle, model_path)
        loaded = joblib.load(model_path)
        loaded_X = loaded["preparation"].transform(cluster_customers[loaded["features"]])
        if loaded["representation"] == "PCA (2)":
            loaded_X = loaded["pca"].transform(loaded_X)
        assert np.allclose(loaded_X, cluster_spaces[loaded["representation"]])
        if row["family"] == "K-Means":
            assert np.array_equal(loaded["model"].predict(loaded_X), loaded["labels"])
        else:
            assert np.array_equal(loaded["model"].labels_, loaded["labels"])
            assert np.allclose(loaded["model"].components_, loaded_X[loaded["model"].core_sample_indices_])
        saved_cluster_paths.append(model_path.name)

    forecast_bundle = {"models": forecast_models, "features": forecast_features, "targets": forecast_targets,
        "selected": chosen_forecast_name, "baseline_reference": chosen_baseline_name,
        "selection_policy": "ML-only; baselines retained as benchmarks", "evaluation_previously_inspected": True,
        "baseline_rules": {"Last week": "repeat lag_1 for four weeks", "Four-week mean": "repeat mean_last_4 for four weeks"}}
    joblib.dump(forecast_bundle, model_directory / "forecast_models.joblib")
    loaded = joblib.load(model_directory / "forecast_models.joblib")
    for name, model in loaded["models"].items():
        assert np.allclose(model.predict(forecast_test[loaded["features"]]), test_predictions[name])
    for name, feature in [("Last week", "lag_1"), ("Four-week mean", "mean_last_4")]:
        assert np.allclose(np.repeat(forecast_test[[feature]].to_numpy(), 4, axis=1), test_predictions[name])

    tables_to_save = {
        "cluster_trials": cluster_comparison, "cluster_finalists": finalists, "cluster_stability": stability_results,
        "segment_profiles": segment_summary.reset_index(), "forecast_folds": pd.DataFrame(fold_rows),
        "forecast_cv": forecast_cv, "forecast_ml_ranking": ml_ranking, "forecast_benchmarks": baseline_ranking, "forecast_selected_settings": chosen_settings, "forecast_validation_ranking": forecast_ranking,
        "forecast_test_comparison": test_comparison, "forecast_test_predictions": forecast_errors,
        "forecast_planning_example": planning_table, "forecast_explanation_folds": explanation_folds,
        "forecast_explanation_summary": explanation_summary.reset_index(),
        "forecast_horizon_errors": horizon_errors.reset_index(), "forecast_product_errors": product_errors.reset_index(),
    }
    for name, table in tables_to_save.items():
        table.to_csv(result_directory / f"04_{name}.csv", index=False)
    cluster_profiles.to_csv(processed_directory / "customer_segments_sample.csv")
    forecast_test.to_csv(processed_directory / "forecast_test.csv", index=False)
    step4_config = {
        "seed": SEED, "sample_customers": len(cluster_customers), "score_sample": len(score_rows),
        "profile_cutoff": str(profile_cutoff.date()), "cluster_features": selected_features,
        "cluster_search": {"k": list(range(2,7)), "eps": [0.2,0.4,0.6], "min_samples": [10,30],
                           "representations": list(cluster_spaces)},
        "cluster_rules": {"min_coverage": 0.95, "min_cluster_share": 0.01, "max_clusters": 8, "min_stability": 0.75},
        "resample_seeds": [7,21,84], "resample_fraction": 0.8,
        "selected_cluster": chosen_cluster_id, "common_evaluation_customers": len(common_rows),
        "rfm_common_silhouette": float(rfm_common_silhouette), "stability_passed": segmentation_stable,
        "cluster_artifacts": saved_cluster_paths, "rfm_reference": {"recency_days": 90, "frequency": 1, "spend_median": rfm_spend_median},
        "forecast_features": forecast_features, "forecast_targets": forecast_targets,
        "selected_products": chosen_products["product_id"].tolist(), "product_selection_end": str(selection_end.date()),
        "validation_starts": [str(date.date()) for date in validation_starts], "validation_origin_weeks": 4,
        "train_maturity_rule": "origin + 28 days <= validation/test start",
        "test_start": str(test_start.date()), "last_test_origin": str(last_test_origin.date()),
        "test_outcome_end_exclusive": str(test_outcome_end.date()), "test_refit": False,
        "forecast_search": {name: candidate["model"].get_params() for name,candidate in forecast_candidates.items()},
        "selected_ml_from_validation": chosen_forecast_name,
        "selection_policy": "Best validation MAE among Decision Tree and Random Forest only; baselines benchmark-only",
        "selection_policy_revision_date": "2026-09-24", "evaluation_previously_inspected": True,
        "explanation": {"method": "validation permutation importance", "repeats": 10, "seed": SEED}, "selected_baseline": chosen_baseline_name,
        "versions": {**configuration["versions"], "threadpoolctl": threadpoolctl.__version__}, "source_manifest": configuration["source_manifest"],
        "elapsed_seconds": elapsed_seconds,
    }
    (config_directory / "step4_models.json").write_text(json.dumps(step4_config, indent=2), encoding="utf-8")
    product_business.to_csv(result_directory / "04_forecast_business_profiles.csv", index=False)
    return {"selected_model": chosen_forecast_name, "model_file": str(model_directory / "forecast_models.joblib"),
            "reload_checks": "passed"}

