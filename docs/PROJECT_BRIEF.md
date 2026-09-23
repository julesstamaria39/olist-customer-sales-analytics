# Final-project brief

## Current delivery status - 2026-09-24

The active scope is B customer segmentation and C weekly/daily sales forecasting; A classification is retired. The combined final report and two 10-slide decks are complete. All 36 notebook code cells passed in a fresh Windows/Python 3.13 environment (27.0 seconds), with raw-data checksum, model reload, temporal-leakage and fairness-calculation checks. Raw data were verified locally, not freshly downloaded in that run. Public GitHub publication was explicitly authorized by the user's Step 7 request. The [public repository](https://github.com/julesstamaria39/olist-customer-sales-analytics) was published and verified on 24 September 2026 with all required directories and deliverables. R7 delivery is verified for this Windows environment; other platforms are not tested. This update supersedes older planning/status statements below. Protected-group evidence and mitigation validation remain gaps; no grade or full fairness compliance is claimed.

## Current model milestone - 2026-09-23

Step 4 now includes trained/tuned K-Means and DBSCAN comparisons for B and Decision Tree/Random Forest regressors for C, with matching baselines, chronological forecast evaluation, metrics, configs, and reload-verified model artifacts. Lag 3 is included. B selects a broad two-group K-Means sample segmentation; C selects Random Forest as the best ML candidate by existing validation MAE, while the four-week mean and last-week rules are benchmarks only. This ML-only policy was requested on 24 September 2026 after the earlier test had been inspected; settings and predictions are unchanged. Random Forest does not beat the overall benchmark. The notebook includes validation input-reliance analysis, all-product forecast examples, and product-level planning limitations. Test results and limitations are recorded in the notebook and STATUS.md. The April-July test outcomes are now inspected; do not retune on them while calling them untouched. Earlier planning text below is superseded for this milestone. Next: interpretation/explainability and supported-group fairness, with the existing protected-attribute gap unresolved.


## Active scope update - 2026-09-23

The user removed A (repeat-purchase prediction) from modeling after the feasibility review. Repeat behavior remains descriptive EDA. **B customer segmentation and C observed-sales forecasting are the active tasks.** This decision supersedes earlier A/B/C scope statements and classifier plans below. The supplied rubric asks for justified task types, not mandatory classification.

Step 3 now uses a single pre-2-April-2018 customer snapshot, correlation-based feature selection, median/log/scaling preparation, and PCA for B; weekly product lags remain for C. No repeat labels, classifiers, or AP comparisons are run. Active artifacts are data/processed/customer_profiles.csv, customer_features_scaled.csv, customer_features_pca.csv, product_week_features.csv, and artifacts/step3_bc/. Prior classifier artifacts are retired. Model importance/explainability will be addressed through forecasting; clustering comparisons and final evaluation remain pending. R3 does not yet establish that PCA improves clustering, and R4/R5 remain incomplete.


Status: domain, analytical scope, dataset, audience, and rubric objective confirmed. The user supplied the [Pillar 5 rubric](RUBRIC_SOURCE.txt); it is the requirements source. All analysis lives in notebooks/Final_Project.ipynb.

The [step-by-step project plan](PROJECT_PLAN.md) implements the [rubric evidence tracker](RUBRIC_ALIGNMENT.md). Step 2 focuses on three connected source tables, basic cleaning, and simple EDA. Step 3 adds historical customer profiles, five-product weekly features, and a training-only selection/PCA development experiment; final evaluation design follows in Step 4. Final splits, eligibility rules, and model choices remain provisional pending preparation and baseline evaluation.

## Source of truth

The user's confirmed decisions and supplied rubric govern current work. The latest request includes the rubric's presentations and public GitHub requirements; deadlines remain outside scope. Earlier coursework is reference material, not evidence of final-project requirements.

## Program objective

Develop a reproducible Olist eCommerce analytics project covering repeat-purchase prediction, customer segmentation, and sales forecasting, with evidence meeting every Outstanding/Exemplary rubric descriptor. Target the full **100 available points (95 core + 5 bonus)** through analytical quality, responsible evaluation, clear communication, and reproducibility. A grade cannot be guaranteed.

Use [RUBRIC_ALIGNMENT.md](RUBRIC_ALIGNMENT.md) as the criterion-by-criterion acceptance checklist. It requires a complete data dictionary; documented preprocessing and EDA; justified feature selection AND dimensionality reduction; multiple tuned models with saved artifacts/configs; explainability; sensitive-group fairness metrics and mitigations; two 8-12-slide decks; a final report and reproducible public GitHub repository; and a coherent originality contribution. Planned outputs are not completed evidence.

## Technical decisions to resolve

- Evaluate baselines for all three analyses using Step 2's evidence on rare repeats and sparse product histories.
- Step 1 selects AP for A, silhouette with stability checks for B, and MAE for C. Audit cohort support, horizons, time splits, and model choices before freezing the evaluation contract.
- Establish practical runtime limits as experiments are designed.
- Resolve the rubric's sensitive-group fairness coverage: current Olist schema has location fields but no explicit age, gender, or race labels. Geographic disparity checks alone must not be represented as full coverage.

## Working domain and proposed direction

User-selected domain: **eCommerce**. User-selected scope: **A. Repeat-purchase prediction, B. Customer segmentation, and C. Demand forecasting**. User-selected dataset: **Brazilian E-Commerce Public Dataset by Olist** (2026-09-18). Empirical suitability and assignment compatibility remain to be established.

### Decisions we will fill in together

| Item | Current entry | Status |
| --- | --- | --- |
| Domain | eCommerce | User selected |
| Analytical scope | Repeat-purchase prediction, customer segmentation, and demand forecasting | User selected |
| Intended audience | eCommerce management team, including marketing/customer analytics and inventory/operations | User confirmed |
| Business purpose | Support customer planning with segments and repeat-purchase predictions, and operations planning with sales forecasts | User confirmed |
| Repeat-purchase horizon | Next 90 days | Provisional; verify purchase cadence |
| Forecast horizon and granularity | Approved-order item-record counts for each of the next four complete weeks, for an eligible product set | Working definition; verify semantics, coverage, and scope |
| Dataset | Brazilian E-Commerce Public Dataset by Olist, version 2 | Downloaded and integrity-verified; three relevant tables consolidated in Step 2 |
| Quality objective | Outstanding/Exemplary for R1-R8; 100 available points | User requested; evidence pending |
| Required communication | Separate technical and business decks, each 8-12 slides; final report | Rubric requirement; planned |
| Public portfolio | Structured, reproducible public GitHub repository with genuine history | Rubric requirement; prepare locally, publication authorization pending |

### Step 1 problem framing

Completed written deliverable: [Step 1 in the project notebook](../notebooks/Final_Project.ipynb#step-1). This defines task types, observation/target units, technical metrics, baseline-relative success rules, business direction with indicative KPIs, and Capstone Steps 1-3 linkage. Detailed business KPI calculations and targets are deferred to evaluation design. Primary metrics are selected; data-dependent horizons and split dates remain provisional. No model performance target is claimed achieved.

An eCommerce business needs to understand its customers and anticipate future sales. This project will use historical transactions to identify customer groups, predict whether existing customers will purchase again within a defined period, and forecast product sales. The three analyses will share a documented data preparation process and produce evidence to support customer planning and inventory discussions. Each analysis will have its own evaluation criteria and limitations.

### Confirmed audience and business purpose

This project supports an eCommerce management team: marketing uses customer segments and repeat-purchase predictions, while operations uses sales forecasts to inform planning.

- **Marketing/customer analytics:** understand purchasing patterns and customer groups, and assess the likelihood of repeat purchases.
- **Inventory/operations:** use forecasts of observed sales to inform product planning discussions, within the limits of the available data.
- **Management:** review the combined findings, model performance, and limitations when considering business actions.

This is the intended audience for the academic project, not an assertion of a partnership with Olist. The project does not promise increased revenue, campaign effectiveness, or optimal inventory decisions.

This wording reflects the user's selected scope, not a claim about an actual business partner or an approved assignment scope. We will use Olist's historical marketplace data and refine the wording after auditing it and checking the rubric.

Working title: **eCommerce Customer and Sales Analytics: Segmentation, Repeat Purchases, and Demand Forecasting**.

### Three connected questions

| Module | Question | Planned output | Proposed evaluation |
| --- | --- | --- | --- |
| A. Repeat-purchase prediction | Will an existing customer place another approved order within 90 days? | Binary-classification probabilities | Primary: maximize average precision versus constant-score and recency baselines; business: repeat-purchase rate among prioritized customers |
| B. Customer segmentation | What distinct purchasing-behavior groups appear in customer history? | Unsupervised cluster assignments and profiles | Primary: silhouette in a common feature space, with stability and size checks; business: group sizes, purchasing patterns, and spending shares |
| C. Demand forecasting | How many approved-order item records will selected products accumulate in future weeks? | Numeric time-series forecasts for four complete weeks | Primary: minimize MAE versus naive and trailing-mean baselines; business: better sales planning, assessed through forecast errors |

The provisional repeat-purchase horizon is 90 days. Not purchasing within that horizon is not proof of permanent churn. The provisional forecast is four weeks ahead at weekly granularity for a small product set chosen using development data only. Both use a working approved-order event definition, with approval time determining information availability. Approval is not proof of completed delivery; later status must not leak into past predictors. See the notebook's Step 1 section for working windows, technical metrics, business direction, and caveats. Changes after the audit must be documented before model comparisons.

If data contains only transactions, Module C measures observed sales as a proxy for demand. Stockouts and lost demand cannot be inferred reliably without stock-availability or equivalent information.

### Scope and shared architecture

All three modules are core scope. Start with one shared data audit, then derive two analysis tables: historical customer snapshots for A/B and product-by-week sales for C. Missing customer IDs may exclude rows from customer analysis without automatically excluding valid sales from forecasting; document eligibility per module.

Build B first to describe customer behavior, A next to evaluate future purchasing, and C next to forecast sales. A can use the shared customer features without depending on cluster labels. If segment assignments become classifier inputs, fit the segmentation within training folds to prevent leakage.

Begin with baselines, then implement substantive tuned comparisons to meet R4. The project planning target is A: baseline plus three classifier families; B: an RFM reference plus two clustering approaches; C: a naive baseline plus two forecasting approaches. These counts are our implementation target, not numbers prescribed by the rubric. Document any evidence-based changes. Integrate findings in a final report and separate technical/business decks. Recommendation engines, deployment, and a live dashboard remain optional.

### Selected dataset: Olist

- **Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/metadata), published by Olist on Kaggle.
- **Publisher description:** approximately 100,000 orders from 2016-2018 across Brazilian marketplaces, with customer, product, payment, delivery, and review information.
- **Listed license:** CC BY-NC-SA 4.0. Preserve attribution and record the source/version and applicable terms when acquiring the files.
- **Current state:** version 2 downloaded through KaggleHub on 2026-09-21. All nine CSVs passed parsing and offline checksum verification. Step 1's read-only context check found 99,441 orders, 96,096 distinct customers, 2,997 customers with multiple orders across full history (3.12%), and 112,650 item rows. This full-history percentage is not 90-day target prevalence. Step 2 now contains focused cleaning, a six-column consolidated DataFrame, and EDA; modeling suitability remains conditional on baseline performance.
- **Raw-data location:** `data/raw/olist/`, relative to the final-project root. Original CSVs are preserved; acquisition time, source version, counts, schema, and checksums are recorded in [DATA_MANIFEST.json](DATA_MANIFEST.json). Use `scripts/download_olist.py` to reproduce acquisition or verify files.

| Source table | Intended role |
| --- | --- |
| Orders | Order identity, purchase timestamps, status, and delivery dates |
| Customers | Link order-specific customer IDs to persistent customer identity |
| Order items | Product-level purchase lines and values |
| Products and category translation | Product attributes and interpretable categories |
| Payments | Optional payment features and reconciled order totals |
| Reviews, sellers, and geolocation | Optional extensions only when needed for an agreed question |

#### Data rules and feasibility checks

1. Use **customer_unique_id** for customer histories. Use **customer_id** to join customers to orders; it is order-specific in this dataset.
2. Check join cardinality and aggregate one-to-many tables before combining them. Joining item rows directly to multiple payment/review rows can multiply sales totals.
3. Define eligible orders consistently and report canceled/unavailable-order exclusions. Ensure every predictor was actually available at the scoring cutoff; final delivery outcomes and later reviews must not leak into historical predictions.
4. Measure repeat-customer counts and positive outcomes in each proposed time split. Do not assume that a 90-day label is learnable merely because customer IDs exist. If coverage is inadequate, discuss adjustments with the user while preserving all three selected modules as the intended scope.
5. Check whether frequency-based customer segmentation is informative; assess the distribution of one-order customers before choosing features and segment counts.
6. Measure product sales density and available history. If product-level forecasts are too sparse, propose category-level forecasting explicitly before changing the target. Choose eligible series using development data only.
7. Treat forecasts as observed marketplace sales, not total inventory demand or lost sales. Define whether the target counts item lines, units, or orders after inspecting the schema; do not assume a quantity field exists.
8. Record data coverage, exclusions, and limitations in the final report. Do not extrapolate automatically from this marketplace sample to all Brazilian eCommerce.

Evaluation contract: use the primary metrics and baseline comparisons in Step 1 of the notebook. Business KPIs are directional at this stage; choose ranking capacity, calculations, and targets during evaluation design before model comparisons. Predicting repeat purchase does not establish who would benefit from a retention offer; measured campaign uplift requires intervention evidence. Financial impact stays a labeled sensitivity scenario until suitable cost/outcome data exists.

### Step 2 audit decisions

[Notebook Step 2](../notebooks/Final_Project.ipynb#step-2) uses orders, customers, and items only. It finds common column names, removes missing required fields and exact duplicates, connects tables using customer_id/order_id, and produces consolidated_df with one row per approved-order item. Its six columns are order_id, order_item_id, customer_unique_id, product_id, order_approved_at, and price.

EDA and price IQR thresholds use approvals before 2018-04-02. Remove IQR outliers from eda_df for typical-price analysis; preserve valid transactions in consolidated_df for sales targets and orders_with_customers for repeat-purchase labels, including approved orders without item details. Later outcomes remain reserved for evaluation.

Keep A/B/C and the provisional 90-day/four-week horizons for baseline investigation. Build historical customer features and product-week tables from the connected data next. Retain the approval-event definition, distinguish unknown spending from zero, investigate simultaneous orders, and leave unreliable delivery/payment/geolocation features out of the initial predictors unless their availability can be justified. Final split dates and eligible product thresholds will be fixed during evaluation design.

## Project acceptance checks

These module checks supplement the full R1-R8 checklist in [RUBRIC_ALIGNMENT.md](RUBRIC_ALIGNMENT.md); passing them alone does not establish complete rubric coverage.

| Selected objective | Acceptance check | Status |
| --- | --- | --- |
| Repeat-purchase prediction | Compare with a baseline on chronological evaluation data and report limitations | Planned |
| Customer segmentation | Explain segment profiles and assess their stability and usefulness | Planned |
| Sales forecasting | Compare forecasts with a simple baseline using chronological backtesting | Planned |
| Reproducibility | Document data preparation and reproduce the analysis from a fresh kernel | Planned |

## Architecture decisions

Confirmed: preserve existing coursework and use `5.0 Final Project/` for final-project implementation. Maintain exactly one analysis notebook, `notebooks/Final_Project.ipynb`, with sequential sections for all modules. Keep utilities separate and derive the final report/decks from notebook evidence.

Selected task types: customer classification, customer clustering/profiling, and product-sales forecasting. Proposed shared design: cleaned transactions feed customer snapshots and product-week aggregates.

Selected dataset: Olist. Focused consolidation/cleaning/EDA implemented in Step 2; direct dependencies recorded in requirements.txt. Pending: feature-table implementation, configuration format, final evaluation design, and experiment storage. No model pipeline has been implemented.
