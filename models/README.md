# Step 4 model inventory

Run `.venv\Scripts\python.exe scripts/run_notebook.py` from the project folder to regenerate all files. Binaries are ignored by Git; use the recorded dependency versions. No deployed or causal performance is claimed.

| Artifact | Fitted contents | Population and use |
| --- | --- | --- |
| cluster_00.joblib | Selected four-feature K-Means, 2 clusters, preprocessing, sample IDs/labels | 6,000 sampled customer profiles before 2 April 2018; a broad descriptive split |
| cluster_11.joblib | Two-component PCA K-Means finalist and preprocessing | Same sample; alternative representation, no improvement established |
| cluster_19.joblib | PCA DBSCAN finalist (`eps=0.4`, `min_samples=30`), preprocessing, sample IDs/labels | Same sample; -1 is noise; DBSCAN has no native new-customer prediction method |
| forecast_models.joblib | Tuned Decision Tree and Random Forest, ordered features/targets, selected forecast name and baseline rules | 180 product-origin rows with all four targets complete before 2 April 2018; five early-selected products |
| daily_random_forest.joblib | Five product-specific Random Forest regressors, ordered calendar features, date origin, product IDs and settings | Section 4.9: top five products by 2017 training-period item counts; refitted through 1 April 2018 for fixed daily forecasts on 2 April-22 July |

Daily models use day number since 2 January 2017, month, day of month, and day of week. No lagged sales enter these models. See configs/step4_daily_forecast.json for splits, tuning, and trend rules. The daily experiment selects depth 6/minimum leaf size 7 on validation, then refits once before testing. It misses all five observed trend labels under the stated rule and does not beat the average benchmark overall. These models should not be described as reliable trend detectors or contemporary forecasts.

The selected ML forecaster is **Random forest 2** (100 trees, depth 3, minimum leaf size 5), chosen by the existing validation ranking among ML candidates only. The four-week mean and last-week rules are benchmarks, not candidates. The bundle retains both learned models and the baseline rules. This policy changed on 24 September 2026 after the earlier test was inspected; settings and all predictions are unchanged. It must not be described as a newly untouched evaluation. Random Forest has not shown an overall accuracy gain over the average benchmark. At a new forecast date, supply the five lag/mean inputs in the saved order; baselines repeat lag_1 or mean_last_4 across four horizons. Do not supply item_count or future targets as predictors.

The customer bundles include fitted preparation and optional PCA. Apply the stored transforms before K-Means prediction. DBSCAN reload verification checks saved labels and core samples rather than inventing a prediction API. Customer identifiers in these ignored artifacts identify fitted sample rows, not predictive features.

See ../configs/step4_models.json for dates, seeds, search spaces, source manifest, software versions, and selected trial. See ../reports/tables/ for tuning, stability, profiles, test predictions, and errors. Reload equivalence is checked in the notebook. A fresh Windows/Python 3.13 environment passed the full notebook and model reload checks on 24 September 2026.

Additional interpretation outputs include validation permutation-importance summaries and a historical 2 April 2018 planning table in reports/tables/. The selected forecast name is stored in the bundle under selected and in configs/step4_models.json under selected_ml_from_validation. The configuration records ML-only selection, the review date, prior evaluation inspection, and explanation settings. The test comparison CSV uses selected_ml, not a claim that the revised policy preceded the original test inspection.
