# Workspace status

## Step 7 published - 2026-09-24

Public repository: [https://github.com/julesstamaria39/olist-customer-sales-analytics](https://github.com/julesstamaria39/olist-customer-sales-analytics). Unauthenticated GitHub API checks confirmed public visibility, main as default branch, the initial commit matching local HEAD, and all required deliverables among 96 tracked files. The README and notebook now link the repository. Final report PDF: 12 pages and six embedded charts; both decks: 10 slides each. Source code, data acquisition instructions, model regeneration inventory and reproduction commands are published. No raw/processed datasets, model binaries, credentials or local environments were uploaded. Commits use the account's GitHub noreply email. This completes Step 7 publication; previously stated analytical/fairness limitations remain.

## Step 7 publication preparation - 2026-09-24

- Created the local Git repository and moved reusable analysis into src/olist_analytics, preserving script compatibility imports. Rewrote the public README with setup, results, deliverables and limits; added contributing and attribution/reuse notices. Code licensing remains unselected.
- Completed final-report framing, source overview, model comparisons, recommendations and conclusions from existing evidence. Rebuilt the PDF (12 pages, six embedded charts) and both 10-slide decks.
- Fresh isolated Python 3.13 environment: pinned requirements installed, pip check passed, nine raw CSV checksums verified, all 36 notebook cells executed in 27.0 seconds, and model reloads, daily future-outcome mutation and fairness arithmetic/state-leakage checks passed. Existing local raw files were used; this was not a fresh network acquisition. No changes to model choices or evaluation dates.
- Public upload candidates passed credential-pattern and file-size checks. Raw/derived datasets, fitted customer bundles, credentials, environments and preview caches are excluded. User explicitly authorized a public repository; GitHub sign-in succeeded. Publication is pending final upload and URL verification.
- Remaining analytical limits: no protected-group fairness data, no validated mitigations, no observed business ROI and no overall forecasting advantage over simple benchmarks.

## Final report PDF - 2026-09-24

Exported reports/final_report.md to reports/final_report.pdf: nine pages with all six existing charts embedded, readable tables, captions and page numbers. Added scripts/export_report_pdf.py for regeneration and pinned the Markdown parser in requirements-presentations.txt. Verified section text and six embedded images; all nine pages rendered successfully and the layout was visually reviewed. Preview evidence is in artifacts/report_preview. No notebook, data or model computations changed; remaining report chapters and previously recorded project gaps remain pending.

## Step 3 report visualizations - 2026-09-24

The EDA + Feature Engineering Report now embeds all four existing Step 3 figures: recency/spending box plots, the customer-feature heatmap/scatter plot, PCA variance/projection, and the historical forecast window. Added short captions explaining each result and its interpretation limits. Reused notebook-generated images; no charts, data or model computations were changed. The newly embedded relationship/PCA images were visually reviewed and all report image paths verified.

## Step 3 report packaged - 2026-09-24

Added the EDA + Feature Engineering Report to reports/final_report.md before the existing Bias & Fairness Analysis. It summarizes executed cleaning/join counts, customer EDA, the four selected features and correlation filter, imputation/log/scaling, the PCA finding, chronological weekly feature construction, and reproducibility commands/artifacts. Two existing figures and links to the single notebook support the narrative. This is documentation derived from stored evidence; no model, dataset, notebook code or outputs changed. Other final-report chapters and previously recorded validation/fairness/publication gaps remain pending.

Verification: all local report links resolve; customer counts, missingness, selected features and weekly row counts match saved artifacts. Hash comparisons confirm the notebook and existing fairness section are unchanged. One-notebook inventory passed. No computation rerun was needed for this report-only addition.

## Step 6: Technical and business presentations - 2026-09-24

- Created presentations/technical_deck.pptx and business_deck.pptx, each 10 slides, with matching PDFs, editable text/tables/diagrams/bar charts, speaker notes and evidence footers. The technical deck covers data, features, temporal evaluation, model results, PDP/ICE and fairness limits. The business deck covers customer/product priorities, forecast readiness, ROI assumptions, risks and a proposed pilot.
- Business ROI is explicitly hypothetical: 1,000 contacts, BRL 40 contribution per extra order, BRL 1/contact and BRL 500 setup. Scenario net values are -1,100/-300/+500 at 1/3/5 percentage-point uplift; break-even is 3.75 pp or 38 whole extra orders. No observed ROI, model improvement or full fairness compliance is claimed.
- Added scripts/build_presentations.py, requirements-presentations.txt, presentations/README.md, roi_scenarios.csv and a build manifest with evidence hashes. Presentation packages were installed only under ignored artifacts/presentation_tools; the shared environment was not changed. No upload/publication occurred.
- Notebook Step 6 now links the two decks and PDFs, with the retired classification scope preserved elsewhere. Only notebook markdown changed; all 36 executed code-cell outputs were preserved. The partial report header now points to the completed decks.
- Validation: both PowerPoints reopen with 10 slides and speaker notes; ZIP/XML integrity, measured text/object bounds and ROI arithmetic checks passed. All 20 matching PDF pages were rendered and visually reviewed. PowerPoint/LibreOffice is unavailable locally, so visual verification uses the shared-layout PDFs rather than native Office rendering; this limit is recorded in presentations/README.md. Notebook schema and sole-notebook checks passed.
- Remaining project gaps: other final-report chapters, clean-environment recreation, protected-group fairness evidence, mitigation validation and authorized repository publication. Presentation deliverables are complete; no rubric points are self-awarded.

## Step 5: Bias & Fairness Analysis - 2026-09-24

- Replaced the Step 5 placeholder with the assignment's ethical-AI section. Added real sklearn PDP/ICE calculations for the selected weekly Random Forest's week-1 output, using 180 development rows, two inputs, and 30 displayed ICE lines. Correlated-input/unrealistic-combination and noncausal limits are explicit. Updated navigation and redirected the old Step 8 fairness placeholder.
- Added training/validation/test errors and zero-versus-positive-sales diagnostics. Weekly RF has 70.4% zero targets and underpredicts positive-sales periods by 1.182 items on average; daily RF has 72.3% zero days and underpredicts positive-sales days by 1.074 items. Daily fit/validation/test MAE is 0.615/1.017/0.850; time shifts and differing fitted samples limit any overfitting conclusion.
- Defined a hypothetical offer to the higher-median-spend segment (200/6,000 sampled customers), without contacting anyone. Joined each persistent customer to their latest pre-cutoff state with validated keys. Among 14 states with at least 50 customers (5,718/6,000 covered), rate gap is 3.95 percentage points and min/max ratio 0.00. PA is 0/54; SP 94/2,380. Wilson rate intervals and the omitted model-selection uncertainty are shown; no unknown states in the sample. All state counts are exported, including groups excluded from the gap.
- Sensitive-group fairness remains unmeasurable: the schema lacks gender/race/age/income, and geography/spending are not inferred demographic labels. Equalised odds is not calculated without a real eligibility/benefit label. Reweighting, inclusive outreach, consent-based audit data, and future validated thresholds are proposals, not implemented/validated mitigations. No legal compliance or absence of discrimination is claimed.
- Generated the requested Bias & Fairness Analysis section in reports/final_report.md directly from notebook narrative and computed evidence. Other report chapters remain pending. Added scripts/bias_audit.py, scripts/check_bias_audit.py, five 05_* tables, two figures, and configs/step5_bias_audit.json; no fitted models or scope changed.
- Validation: all 36 code cells passed in a fresh kernel in 27.4 seconds, with no errors/stderr. Both new charts visually reviewed. Targeted parity arithmetic, support/zero-denominator cases, confidence bounds, and future-state mutation checks passed. Report generation, audit count/rate reconciliation, notebook schema, execution order, and sole-notebook checks passed. Remaining gaps: protected-group evidence, mitigation validation, clean-environment reproduction, remaining report/decks, and authorized publication.

## Daily product forecasting (Section 4.9) - 2026-09-24

- Added calendar-only Random Forest daily item forecasts, training-only top-five product selection, zero-sales dates, five actual/predicted daily charts, and a predicted-versus-observed direction chart/table. Products are ranked on 2 January-31 December 2017 item counts, independently of the earlier weekly subset.
- Train: 364 days/1,820 rows; validation: 1 January-1 April 2018, 91 days/455 rows; test: 2 April-22 July, 112 days/560 rows. Four parameter settings are compared on validation MAE. Five product-specific forests use the selected depth 6/minimum leaf size 7, 100 trees, seed 42, one worker for deterministic predictions. Refit once using train+validation; no test refitting or sales-history inputs.
- Trend is the last 28 test days' average minus the first 28, with a predeclared +/-0.1 items/day flat band. RF matched 0/5 observed directions; overall MAE 0.850 versus 0.817 for the fixed pre-test 28-day mean benchmark. Observed directions: daily products 1/4 upward, 2/5 downward, 3 roughly flat. These descriptive labels are not significance tests; calendar-only RF cannot extrapolate sustained temporal growth/decline. No deployment benefit is claimed.
- Earlier-model review: weekly models already enforce mature targets and chronological train/validation/test boundaries; early product selection avoids the later evaluation. Clustering refits preprocessing/PCA in its stability runs and is explicitly descriptive, with full-development feature selection and no unseen-customer claim. Existing model settings/results were retained. Prior inspection of these dates remains disclosed; this is a historical backtest, not fresh untouched evidence.
- Saved scripts/daily_forecasting.py, models/daily_random_forest.joblib, configs/step4_daily_forecast.json, reports/tables/04_daily_*.csv, and reports/figures/04_daily_sales_trends.png. Leakage regression checks in scripts/check_daily_forecasting.py change future outcomes and verify unchanged selected products, features, validation ranking, forecasts, and benchmark predictions.
- Validation: all 31 code cells passed a fresh-kernel run in 25.1 seconds; reload checks, targeted leakage checks, notebook structure, and nine raw-file manifest checks passed. Chart visually reviewed. Existing clean-environment, fairness, final-report/deck, and publication gaps remain open.

## Forecasting presentation simplified - 2026-09-24

- Replaced the lengthy Sections 4.5-4.8 with short explanations, a small business-insight table, and three charts: model error, forecasts versus actual sales for all five products, and input reliance.
- Moved tuning, diagnostics, plotting, and artifact exports into scripts/forecasting.py. The single notebook retains the model comparison, business findings, and short calls to the utility. Detailed evidence remains available in exported tables and configuration.
- Fresh-kernel execution passed all 29 code cells. Notebook structure and sole-notebook checks passed; all 1,040 prediction/error records match the previous results within 1e-12. Saved-model reload checks passed and all three charts were visually reviewed.
- This changes presentation, not model choices or performance. Random Forest remains the selected ML model and still trails the simple benchmarks. Existing rubric gaps remain unchanged.

## Forecasting review and ML-only selection - 2026-09-24

- User requested removal of the four-week average from model choices and a thorough, presentable business review of 4.5 onward. ML selection now considers Decision Tree and Random Forest only; baselines remain benchmark-only. Random forest 2 wins existing validation MAE (1.996 versus tree 2.110). The policy changed after prior test inspection; provenance explicitly records this instead of claiming an untouched evaluation.
- Forecasting inputs, grids, folds, dates, and fitted model predictions are unchanged. All 1,040 model/product/origin/horizon prediction and error records were reconciled with pre-review results. RF test MAE remains 1.021 versus 0.894 for the average benchmark (14.2% higher error). No inflated accuracy or operational uplift is claimed.
- Rebuilt selected-model horizon/product/business summaries around RF. Added an ML-versus-benchmark selection chart, validation permutation importance across three folds (10 shuffles each), and a historical planning table/chart covering all five products on 2 April 2018. Four-week average and last-week sales are the strongest reliance signals, with mean shuffled MAE increases 0.458 and 0.342; correlations and noncausal interpretation are explicit.
- Explained forecast failure modes: RF underpredicts the main product on average while missing individual timing; it produces positive estimates for low/no-activity products. Single-date forecasts are distinguished from full-period averages. No automatic stock quantities, cost savings, or contemporary forecasts are claimed.
- Updated models/forecast_models.joblib, configs/step4_models.json, model inventory, result tables, charts, and scope/evidence records. Old selected_forecast_before_test metadata is replaced by selected_ml_from_validation with policy date and evaluation_previously_inspected. Original classification remains retired and clustering is unchanged.
- Validation: all 35 code cells executed in a fresh kernel in 25.0 seconds; new charts visually reviewed. Reload checks passed. Final follow-up only adds interpretation/docs; no model or computation changes. Remaining gaps include clean-environment reproduction, full R5 explainability/fairness requirements, final report/decks, and authorized publication.


## Business interpretation of model results - 2026-09-23

Reworked Section 4.4 around two observed sample profiles: 5,800 single-order customers and 200 repeat or broader-basket customers (89% repeat, 90% multiple products). Added spending shares, recency, missingness, concrete action hypotheses, and a frank assessment that the split may add little beyond simple purchasing summaries. Forecast interpretation now uses product categories as post-model context, unique product-week actuals to avoid double-counting overlapping targets, inactivity, MAE/bias, and planning implications. Product 1 accounts for 63/81 observed items; Product 4 has no recorded sales in 16 test weeks. No category-wide demand, loyalty, causal uplift, or optimal inventory claims. Added two reproducible business-profile CSVs under reports/tables/. Category joins validated; no training features or selected models changed. All 32 code cells passed in a fresh kernel in 21.0 seconds; structure, execution order, and sole-notebook checks passed.


## Additional model-performance visuals - 2026-09-23

Added Step 4 charts for common-sample clustering silhouette, assignment coverage, assigned/noise-inclusive resampling stability; forecasting MAE across validation windows and later dates; and error by horizon and product. Plots reuse existing results, keep all compared methods, identify the frozen choice, and explain noise exclusions, overlapping windows, and quiet products. Exported 04_cluster_performance.png, 04_forecast_error_over_time.png, and 04_forecast_error_breakdown.png under reports/figures/. Fresh-kernel execution passed for all 30 code cells; all three rendered charts reviewed. Model settings, selections, scope, and remaining rubric gaps are unchanged.


## Step 4 implemented - 2026-09-23

Verification: final fresh-kernel run passed all 27 code cells in 17.7 seconds with no stderr. Notebook schema, sequential execution, sole-notebook inventory, mature-target fold boundaries, lag_3 inclusion, 1,040 unique model/product/origin/horizon forecast records, artifact reloads, dependency consistency, and all nine raw-file hashes passed. Reviewed both Step 4 figures. No packages installed or external publication performed.

The active notebook now trains and compares B/C models in Step 4. Lag 3 is included in Step 3 features, exported data, and the window diagram. Earlier statements below that model fitting is planned are historical.

- B: 22 K-Means/DBSCAN trials on the same seeded 6,000-customer development sample, comparing selected features with two-component PCA. Coverage/size screens, a common silhouette space/sample, RFM reference, and three preprocessing-refitted 80% stability runs per finalist are recorded. Selected four-feature K-Means has two groups, common silhouette 0.741 and mean ARI 1.000. Groups contain 5,800/200 customers; this is a broad purchasing-activity split, not validated marketing effectiveness. Full-population and future stability remain open.
- C: 12 tree/forest settings across three chronological validation windows, with training targets mature before each scoring start. The four-week mean baseline won validation (MAE 1.954). Frozen later evaluation uses 65 product-origin rows, 2 April-25 June 2018, with outcomes ending 23 July. MAE: selected mean 0.894; last week 0.869; Random Forest 1.021; Decision Tree 1.097. No learned-model gain is claimed; quiet products partly explain low later error. The model choice was not changed after test inspection.
- Deliverables: fitted clustering finalists and both tuned regressors in models/; exact search/selection rules, dates, source manifest, versions, and parameters in configs/step4_models.json; tuning/stability/profile/error CSVs in reports/tables/; customer assignments and test features in ignored data/processed/. Reloaded transformations, K-Means assignments, DBSCAN labels/core samples, and forecast predictions match.
- Business evidence is descriptive segment sizes/spending shares and forecast error reduction, not causal ROI. R4 has implemented comparisons and saved artifacts; clean-environment recreation, R5 explainability/fairness, final report/decks, and publication remain incomplete. The later test period is now inspected and must not be reused for unreported tuning.


## Step 4 model introduction - 2026-09-23

Added a short opening paragraph naming K-Means/DBSCAN for B and Decision Tree/Random Forest regressors for C, with task justification, comparison metrics, baselines, and saved-artifact requirements. Renamed the Step 4 heading/navigation to Model Implementation to match the assignment. Markdown-only edit: all code and outputs preserved; no models trained or new performance claimed. Lag 3 remains a preparation change to make before forecasting model implementation.


## Forecast-window visualization - 2026-09-23

Section 3.6 now illustrates the first forecasting row using actual weekly product counts: four past weeks (3, 7, 8, 2), their mean of 5, and four future targets (5, 4, 11, 8). The forecast boundary, lag names, and distinction between observed targets and predictions are explicit. Saved reports/figures/03_forecast_window.png and visually checked readability. Fresh-kernel execution passed for all 18 code cells in 11.1 seconds. R3 gains a feature-window explanation; no modeling or scope changes.


## Grouped customer EDA - 2026-09-23

Added Section 3.2 summaries for 1/2/3+ orders and spending box plots by recency band, with group sizes, missing and incomplete spending counts, and median behavior. Original customer profiles and model inputs are unchanged. Groups contain 62,556 / 1,789 / 149 customers; recency-band spending medians are BRL 89.90 / 89.00 / 89.00. Added interpretation and exported reports/figures/03_spending_by_recency.png. Fresh-kernel execution passed: 17 code cells in 11.4 seconds; chart visually reviewed. R3 gains descriptive EDA evidence; later clustering validation and other rubric gaps remain open.


## Active scope update - 2026-09-23

The user removed A (repeat-purchase prediction) from modeling after the feasibility review. Repeat behavior remains descriptive EDA. **B customer segmentation and C observed-sales forecasting are the active tasks.** This decision supersedes earlier A/B/C scope statements and classifier plans below. The supplied rubric asks for justified task types, not mandatory classification.

Step 3 now uses a single pre-2-April-2018 customer snapshot, correlation-based feature selection, median/log/scaling preparation, and PCA for B; weekly product lags remain for C. No repeat labels, classifiers, or AP comparisons are run. Active artifacts are data/processed/customer_profiles.csv, customer_features_scaled.csv, customer_features_pca.csv, product_week_features.csv, and artifacts/step3_bc/. Prior classifier artifacts are retired. Model importance/explainability will be addressed through forecasting; clustering comparisons and final evaluation remain pending. R3 does not yet establish that PCA improves clustering, and R4/R5 remain incomplete.


## B/C revision verification - 2026-09-23

Fresh-kernel execution passed for all 15 code cells in 9.6 seconds; regenerated PCA chart reviewed. Correlation filtering retains recency, frequency, observed spend, and product variety. PCA at 95% retains all four: no additional compression; its two-dimensional visualization retains 67.8%. Reloaded preparation/PCA outputs match. Original source data were not edited. Retired classification outputs are archived under artifacts/retired_repeat_purchase/ and do not feed current work.

## Current workflow - 2026-09-23

Use [notebooks/Final_Project.ipynb](../notebooks/Final_Project.ipynb), the sole analysis notebook. Step 1 initial framing is complete, with directional business KPIs; detailed business measurement is deferred to evaluation design. Step 2 now contains focused three-table consolidation, basic cleaning, IQR-filtered price EDA, and simple charts. Step 3 now contains customer/product features, preparation, model-based feature selection, and PCA with a chronological development comparison. Steps 4-9 remain planned. Next: freeze Step 4 evaluation choices and baselines. Utilities and project-control documents remain separate. Earlier entries below are a chronological history; superseded filenames are historical only.

## Step 3 feature preparation - 2026-09-23

- Added eight readable code cells to the sole notebook. Customer profiles use distinct approved orders and past item prices; missing item details remain unknown, with spend-coverage and missingness indicators. EDA-only IQR exclusions do not remove target events or valid spending.
- October 2017 profiles: 26,682 customers, 242 future-90-day positives; January 2018 profiles: 43,916 customers, 323 positives. Training labels mature before the later profiles, and both outcome windows end before 2 April 2018. Final holdout design remains Step 4 work.
- Training-only median imputation, log transforms, scaling, recency-band encoding, forest importance selection, and PCA implemented. Five selected features versus 13 prepared inputs; PCA retains five components and 96.7% variance. January AP: constant 0.00735, recency 0.00840, all features 0.01356, selected 0.01218, PCA 0.01431. These are untuned feature experiments, not final model claims.
- Correlations and PCA charts include interpretation. Strongly correlated histories/spending and duplicated missingness indicators affect the projection; the isolated missing-data group must not be labeled a business segment.
- Five products chosen using sales before 3 July 2017 yield 180 complete four-week forecast-origin rows, with shifted lags and trailing means. An independent transaction-count check verifies the first row's past-week features.
- Saved three processed CSVs and artifacts/step3/ experiment/configuration/scores; all three reloaded models reproduce predictions. requirements.txt adds the already-installed scikit-learn and joblib versions; no package installation. Clean-environment recreation remains unverified.
- Fresh-kernel execution and chart inspection passed; 16 code cells. Section 2.1's kept/excluded source-column display is now executed. R3 has implemented evidence; fold-specific refits, B-specific representation decisions, final model comparisons, broader R2 dictionary details, and R5 sensitive-group coverage remain open.

## Customer-frequency EDA clarification - 2026-09-23

- Updated the chart to recorded orders per customer before 2 April 2018, with 1/2/3/4+ bins, counts, and percentage table. Counts are 62,556 / 1,789 / 121 / 28. Frequency counts distinct order_id per customer_unique_id from approved-order history, not item rows or order-specific customer_id.
- Linked the publisher's customer-ID explanation. Added a short comparison by time since first recorded approval: under 90 days has 403 of 20,522 customers with multiple orders (1.96%); 90 days or more has 1,535 of 43,972 (3.49%). Unequal observation windows, first-observed versus first-ever purchase, and noncausal interpretation are explicit.
- Connected the findings to complete future label windows, rare repeat outcomes, and recency/spending features for segmentation. Added reconciliation checks for distinct order totals and customer counts across observation groups.
- Fresh-kernel execution passed for all eight code cells in 5.8 seconds; reviewed the regenerated reports/figures/02_simple_eda.png. No model fitting, raw-data changes, or IQR-policy changes.

## Section 2 simplification - 2026-09-23

- Replaced the expanded audit with six readable notebook code cells: load needed columns, discover shared column names, remove nulls/duplicates, connect three tables, remove IQR price outliers for EDA, and plot basic patterns. No audit_data.py import remains in the notebook; that helper is retained as optional reference.
- orders/customer_id connects customers; items/order_id connects orders. Validated joins produce consolidated_df with 112,635 approved-order item rows and six columns. Removed 160 orders missing approval dates; 15 item rows have no usable approved-order match. No exact duplicates or invalid prices/sequences were found in the selected fields.
- Keep orders_with_customers for the complete approved-order history, including 629 orders lacking item details. This avoids erasing known purchases when forming repeat labels.
- Price IQR bounds from pre-2018-04-02 data are -101.25 to 275.15 BRL. Removed 5,648 of 75,407 development item rows from eda_df, leaving 69,759. consolidated_df retains valid transactions for purchase/sales targets.
- Generated reports/figures/02_simple_eda.png with price, customer-frequency, and weekly-sales charts. Detailed audit/dictionary coverage is no longer claimed complete in the rubric tracker; basic R3 cleaning/EDA is partial.
- Fresh-kernel execution passed for all seven current code cells in 5.9 seconds. Separate offline verification confirmed all nine original CSV hashes/counts/columns still match. No model training or package changes occurred.
- Reviewed the simplified chart and passed final notebook structure, execution-count, single-notebook, and local-link checks. Removed the temporary build file and two superseded chart exports. Historical audit entries below describe the previous version, not the active deliverable.

## Step 2 source audit and dictionary - 2026-09-22

- Implemented all Step 2 analysis in the sole notebook. Added reusable profiling utilities in scripts/audit_data.py and an in-place fresh-kernel runner in scripts/run_notebook.py. Recorded direct dependencies in requirements.txt without installing or upgrading packages.
- Documented all 52 source fields across nine tables: definitions/join roles, units, availability assumptions, loaded types, missingness, distinct values, and ranges. Hashes, source counts/columns, and type parsing passed.
- Audited keys, join coverage, missing values, outliers, timestamps, and independently aggregated item/payment totals. Observed 261,831 exact repeated geolocation rows, 160 missing approvals, 629 approved orders without item rows, 1,359 carrier-before-approval timestamps, 23 customer-delivery-before-carrier timestamps, and 292 extra orders sharing a customer/purchase timestamp. Four shipping deadlines exceed approval by over 365 days.
- Found 303 matched orders with payment/item-plus-freight differences above one cent. Raw item-payment joins would expand 112,650 item rows to 117,601 rows; aggregate children separately.
- Behavioral diagnostics use approvals before 2018-04-02. Three 90-day development checks have 125/242/323 positive customers (0.863%/0.907%/0.735%). About 97% of development customers have one approved order. These are descriptive feasibility results, not model metrics.
- Product feasibility uses 65 whole weeks from 2017-01-02: 424 products have at least 13 active weeks, and 277 also sold within the last four development weeks. Keep product-level C in scope for a smaller baseline experiment; no final product selection or model training occurred.
- Full-file monthly coverage reveals sparse 2016 and post-August-2018 edges. Later customer/product outcomes were not used for behavioral feasibility; final train/validation/test splits remain pending.
- Validation: all nine current code cells executed in a fresh shared-environment kernel in 29.9 seconds. Reviewed both rendered charts and exported them under reports/figures/. Raw source checksums match the acquisition manifest. Clean-environment recreation is still unverified.
- Final checks passed: notebook schema/saved-error validation, exactly one authored notebook, 44 local links/anchors, both standalone figure exports, utility syntax, and installed versions matching the recorded direct analysis dependencies. Removed temporary build/preview files.
- Next: Step 3 preparation/EDA and feature definitions. Keep detailed business measurement for evaluation design and the unresolved sensitive-group fairness gap visible.

## Framing simplification - 2026-09-22

- Simplified the descriptive context code cell into three commented stages: locate the project, import the summary function normally, and display its result. Replaced next/generator discovery and runpy namespace lookup with explicit folder branches and a direct import. Verified folder discovery from all three supported locations, fresh-kernel output identical to the prior summary, notebook structure, and the single-notebook inventory. Preserved the cell ID and all other cells.
- Follow-up: rewrote framing Section 7 as a short explanation of the learning-program connection, correcting punctuation corrupted during the previous edit. Verified exact save/read preservation, notebook structure, one-notebook inventory, and that all other cells are unchanged. No code execution was needed.
- Simplified notebook Section 5 into three business directions with indicative KPIs. Removed fixed top-10% targeting, action-coverage targets, detailed formulas, and ROI equations from the framing section; detailed business measurement is deferred to evaluation design before model comparisons.
- Clarified program Module 1 versus Capstone Step 1 and project analyses A/B/C. Interpreted Module 1 as Overview of AI and ML using the user's description; an official syllabus title has not been independently verified.
- Synchronized the brief, plan, and rubric tracker. R1 remains partial for detailed business KPI specification; technical metric choices remain in place.
- Markdown-only changes: preserved cell IDs, metadata, and all code cells and saved outputs exactly. Computational execution was not needed for this wording edit.
- Validation passed: notebook structure and saved-error checks; exactly one authored notebook remains in the project.

## Single-notebook rebuild - 2026-09-21

- Consolidated all existing analysis into notebooks/Final_Project.ipynb. Preserved the Step 1 analytical cells, IDs, metadata, and descriptive computation; added navigation and explicitly planned sections for the remaining work.
- Renamed the former framing notebook, removed the zero-byte root notebook, and removed the separate framing report only after verifying its full narrative matched the notebook. No raw data or utility scripts were changed.
- Updated AGENTS.md, README.md, the brief, plan, prompt templates, and rubric tracker to require one notebook. Audit/dictionary, model comparisons, and fairness analysis now belong in notebook sections. Required final report and decks will be derived from notebook evidence.
- Verified exactly one authored notebook under this project and 42 resolving local links/explicit notebook anchors. Executed the existing code cell in a fresh shared-.venv kernel from the notebooks directory; its descriptive output reproduced exactly. Later analytical sections remain unimplemented.
- Next: fill Step 2 with the Olist audit and complete data dictionary. R2-R8 evidence gaps remain; this reorganization does not add modeling results or earned rubric points.

## Verified on 2026-09-17

- `Final_Project.ipynb` was 0 bytes on disk; it contains no readable requirements.
- `5.0 Final Project/` was empty.
- Existing `.venv` reports Python 3.13.0 and has nbformat 5.10.4 installed.
- This workspace was not a Git repository.
- Added project instructions, setup guidance, prompt templates, ignore rules, and a read-only notebook checker.

## Validation

- `.venv/Scripts/python.exe -m pip check`: no broken requirements found.
- Checker accepted `3.1 Clustering/k-Means Clustering.ipynb` structurally; no notebook code was executed.
- Checker correctly rejected the empty `Final_Project.ipynb`.
- Seven temporary fixture checks passed: valid notebook, saved execution error, duplicate cell IDs, empty file, invalid JSON, invalid schema, and missing file. Existing bytes were preserved in all file-backed cases.
- Dependency reproduction in a clean environment and fresh-kernel notebook execution have not been performed.

## Current constraints

Olist version 2 has been acquired, integrity-checked, and audited. Development diagnostics support baseline investigation, but rare repeats, sparse histories, and uncertain historical availability keep modeling choices provisional. The supplied Pillar 5 rubric now defines required outputs, superseding the earlier exclusion of submission requirements. Deadlines remain excluded. The rubric is preserved in docs/RUBRIC_SOURCE.txt; notebooks/Final_Project.ipynb is the canonical analysis file. Sensitive-group fairness coverage is an unresolved gap: the recorded schema has geography but no explicit age, gender, or race attributes.

## Setup location

All generated setup files now live under `5.0 Final Project/`: AGENTS.md, README.md, .gitignore, requirements-tools.txt, docs/, and scripts/. Commands run from that directory using `../.venv/Scripts/python.exe`. The original empty requirements notebook was removed during the single-notebook rebuild; docs/RUBRIC_SOURCE.txt preserves the supplied requirements. Paths in the earlier validation record are relative to the parent AIM_PGD workspace.

## Planning

Added `docs/PROJECT_PLAN.md` with sequential phases, deliverables, completion checks, a provisional file layout, and collaboration expectations. The user selected eCommerce and all three modules: A (repeat-purchase prediction), B (customer segmentation), and C (demand forecasting). Updated PROJECT_BRIEF.md with the combined problem statement, proposed audience, module outputs, evaluation ideas, and shared data design. Synchronized the plan's scope to avoid treating B/C as optional. No dataset has been downloaded and no experiments or model implementation have started. Final technical methods remain provisional pending the Olist audit.

## Dataset decision — 2026-09-18

The user selected the Brazilian E-Commerce Public Dataset by Olist. Updated the brief and plan to replace the previous UCI candidate with Olist. Documented source, listed license, planned tables, identity/join rules, and feasibility checks. Repeat-customer coverage, forecasting density, and empirical quality remain unmeasured. No dataset acquisition or model execution was performed during this documentation update.

## Next action

The user confirmed the combined eCommerce management-team audience and purpose on 2026-09-18: marketing uses customer segments and repeat-purchase predictions; operations uses sales forecasts for planning. Recorded this in PROJECT_BRIEF.md.

Proceed to Step 3 in notebooks/Final_Project.ipynb: implement reproducible preparation and development EDA using the Step 2 audit. Document unknown-spend and simultaneous-order policies, build historical customer/product tables, and extend the dictionary with engineered features. Primary technical metrics and directional business KPIs are documented; detailed business measurement is pending. Keep the sensitive-group fairness gap explicit (R5). Update docs/RUBRIC_ALIGNMENT.md with observed evidence. Do not request deadlines.

## Dataset acquisition — 2026-09-21

- Installed KaggleHub 1.0.2 and Kaggle SDK 0.1.37 in the shared `.venv`; existing packages were not upgraded. Dependency check passed.
- Added `scripts/download_olist.py`, with dataset version 2 pinned, project-relative output paths, offline verification, and refusal to overwrite unverified existing data.
- Downloaded all nine source CSVs into `data/raw/olist/` without a login prompt. Total CSV size: 126,186,995 bytes.
- Recorded version, source/license, acquisition timestamp, tools, SHA-256 hashes, row counts, and columns in `docs/DATA_MANIFEST.json`.
- All CSVs parsed with consistent row widths; offline hash verification passed. Pandas loading passed for orders (99,441 x 8) and customers (99,441 x 5), including purchase timestamp parsing.
- Observed purchase timestamps span 2016-09-04 21:15:19 through 2018-10-17 17:30:18. These endpoints are not a claim of complete coverage for every intervening period.
- No models were trained; no repeat-purchase or forecasting feasibility conclusions have been drawn.
- Verified the default rerun performs offline validation. Five isolated checks with mocked downloads passed: initial acquisition, offline reuse, fresh-checkout restoration against an existing manifest, modified-file rejection, and protection of existing files without a manifest.

## Rubric integration — 2026-09-21

- Preserved the user's exact pasted rubric in docs/RUBRIC_SOURCE.txt and created docs/RUBRIC_ALIGNMENT.md with R1-R8, weights (95 core + 5 bonus), planned evidence paths, acceptance checks, and current gaps.
- Integrated the objective into AGENTS.md, PROJECT_BRIEF.md, PROJECT_PLAN.md, README.md, and prompt templates. Both feature selection and dimensionality reduction, multiple tuned models, saved artifacts/configs, explanation tools, quantitative fairness/mitigation, two decks, and public repository readiness are explicit.
- Added 10-slide outlines for each deck, business KPI/ROI assumptions, and the proposed creativity contribution. These are plans, not completed reports, models, or presentations.
- Checked DATA_MANIFEST.json column lists: no explicit age/gender/race attributes. Geographic audits alone cannot be claimed as full sensitive-group rubric coverage; R5 remains a gap.
- No model training, new dataset enrichment, repository creation, commits, or public publication performed as part of this update.
- Documentation verification passed: rubric source preserved byte-for-byte; all eight criterion weights sum to 95 core plus 5 bonus; 19 local Markdown links resolve. Reviewed the plan for obsolete optional-deck and single-model guidance and updated it to match the rubric.

## Step 1 — Problem understanding and framing

- Created reports/01_problem_framing.md and notebooks/00_problem_framing.ipynb with the business problem, classification/clustering/forecasting rationale, target definitions, primary metrics, baseline-relative success criteria, KPI formulas, assumptions, and Capstone Steps 1-3 linkage.
- Selected AP for repeat-purchase classification, silhouette with stability checks for segmentation, and MAE for forecasting. Top-10% precision/lift, segment shares/action coverage, error reduction, and bias define business-facing KPIs. ROI is scenario-based, not claimed realized impact.
- Added read-only scripts/summarize_framing_data.py and executed its notebook cell in a fresh shared-.venv IPython kernel. Observed 96,096 unique customers and 2,997 with multiple orders across full history (3.12%); this is not 90-day label prevalence. Also found 160 missing approval timestamps and no explicit item quantity column.
- Step 1's written deliverable is complete; R1 framing evidence is documented. Step 2 must audit the provisional approved-order definition, horizons, and actual split dates. No trained models, final performance values, full data audit, or business impact have been claimed.
- Validation passed: fresh-kernel execution, notebook structure/saved-error checks, matching report/notebook narrative, count reconciliation with the data manifest, 26 local document links, and offline verification that all nine raw CSVs still match their original hashes.
