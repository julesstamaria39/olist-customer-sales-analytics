# Final-project execution plan

## Current delivery status - 2026-09-24

The active scope is B customer segmentation and C weekly/daily sales forecasting; A classification is retired. The combined final report and two 10-slide decks are complete. All 36 notebook code cells passed in a fresh Windows/Python 3.13 environment (27.0 seconds), with raw-data checksum, model reload, temporal-leakage and fairness-calculation checks. Raw data were verified locally, not freshly downloaded in that run. Public GitHub publication is explicitly authorized by the user's Step 7 request and is being finalized. See the root README and STATUS.md for the verified URL/status. This update supersedes older planning/status statements below. Protected-group evidence and mitigation validation remain gaps; no grade or full fairness compliance is claimed.

## Step 5 update - 2026-09-24

The assignment's Step 5 is now the notebook's Critical Thinking, Ethical AI & Bias Auditing section. It implements PDP/ICE, fit/error diagnostics, a state-based hypothetical outreach audit with rates/uncertainty, and proposed mitigations. reports/final_report.md contains the generated Bias & Fairness Analysis section only. Protected-group coverage remains unavailable; do not infer demographic labels or treat geography as socioeconomic status. Further report chapters, approved-data fairness work, mitigation validation, decks, and clean-environment reproduction remain separate outstanding deliverables. Earlier references to Step 8 fairness are superseded by Step 5.

## Current model milestone - 2026-09-23

Step 4 now includes trained/tuned K-Means and DBSCAN comparisons for B and Decision Tree/Random Forest regressors for C, with matching baselines, chronological forecast evaluation, metrics, configs, and reload-verified model artifacts. Lag 3 is included. B selects a broad two-group K-Means sample segmentation; C selects Random Forest as the best ML candidate by existing validation MAE, while the four-week mean and last-week rules are benchmarks only. This ML-only policy was requested on 24 September 2026 after the earlier test had been inspected; settings and predictions are unchanged. Random Forest does not beat the overall benchmark. The notebook includes validation input-reliance analysis, all-product forecast examples, and product-level planning limitations. Test results and limitations are recorded in the notebook and STATUS.md. The April-July test outcomes are now inspected; do not retune on them while calling them untouched. Earlier planning text below is superseded for this milestone. Next: interpretation/explainability and supported-group fairness, with the existing protected-attribute gap unresolved.


## Active scope update - 2026-09-23

The user removed A (repeat-purchase prediction) from modeling after the feasibility review. Repeat behavior remains descriptive EDA. **B customer segmentation and C observed-sales forecasting are the active tasks.** This decision supersedes earlier A/B/C scope statements and classifier plans below. The supplied rubric asks for justified task types, not mandatory classification.

Step 3 now uses a single pre-2-April-2018 customer snapshot, correlation-based feature selection, median/log/scaling preparation, and PCA for B; weekly product lags remain for C. No repeat labels, classifiers, or AP comparisons are run. Active artifacts are data/processed/customer_profiles.csv, customer_features_scaled.csv, customer_features_pca.csv, product_week_features.csv, and artifacts/step3_bc/. Prior classifier artifacts are retired. Model importance/explainability will be addressed through forecasting; clustering comparisons and final evaluation remain pending. R3 does not yet establish that PCA improves clustering, and R4/R5 remain incomplete.


Status: Steps 1-3 implemented through a chronological development feature experiment; final evaluation design is next. Work follows PROJECT_BRIEF.md and the supplied RUBRIC_SOURCE.txt, with acceptance evidence tracked in RUBRIC_ALIGNMENT.md. The latest user instruction incorporates rubric-required outputs, including decks and a public repository. Deadlines remain excluded.

## Working outcome

Produce an understandable, reproducible project covering the three selected eCommerce questions and every Outstanding/Exemplary descriptor. Target 100 available points (95 core + 5 bonus), supported by actual evidence rather than promised scores. R4 and R5 account for 40 points and receive explicit modeling/explainability/fairness work.

## eCommerce application of the plan

The user has selected all three eCommerce directions: repeat-purchase prediction, customer segmentation, and demand forecasting. Each is a core module of a shared project. Initial data feasibility has been audited; predictive usefulness and final evaluation choices remain unconfirmed. PROJECT_BRIEF.md records the current scope; the detailed phase plan will be refined as we fill the files one at a time.

| Direction | Business question | Scope tradeoff |
| --- | --- | --- |
| Repeat-purchase prediction — selected | Who will buy again within a defined future period? | Clear predictive target; requires careful historical feature and outcome windows |
| Customer segmentation | What purchase-behavior groups exist? | Useful exploratory project; may not satisfy a supervised-learning requirement |
| Demand forecasting | How much will sell in a future period? | Useful operational problem; needs time-series validation and sufficiently dense product histories |

Proposed build order: shared data audit and preparation, B (customer segments), A (repeat purchases), C (product sales forecasts), then integrated conclusions and reproduction. Reuse data preparation while keeping module-specific eligibility and validation rules explicit.

For B, build customer profiles from historical recency, frequency, and spending. Evaluate segment separation, sizes, stability, and interpretability. Fit any segmentation reused as a predictor only within the corresponding training folds.

For C, start with a small development-selected product set and weekly observed sales. Compare a naive baseline with two suitable forecasting approaches using chronological backtesting and justified tuning (R4 planning target). Four weeks ahead is a provisional horizon. Distinguish observed sales from unconstrained demand when inventory/stockout data is unavailable.

For A, implement the phases as follows:

1. **Define the decision:** specify the customer population and a provisional 90-day repeat-purchase horizon. Confirm these against the rubric. Avoid calling every non-repeat customer permanently churned.
2. **Audit selected data:** inspect Olist, document provenance/license, and check customer identity, time coverage, order statuses, missing joins, duplicate item lines, and value anomalies. Use customer_unique_id for customer history and count distinct order_id values for purchase frequency. Verify join cardinality before aggregating sales. Record exclusion counts and repeated-purchase coverage per chronological split.
3. **Create historical snapshots:** calculate recency, number of distinct purchases, spend, average order value, and product diversity using only data available at each cutoff. Define a qualifying purchase consistently for features and labels. Store identifiers for joins, not as direct predictive features.
4. **Create observable labels and time splits:** label purchases in the 90 days after each cutoff. Exclude cutoffs without a complete future window. Ensure training labels would already be known before validation/test scoring dates; avoid overlapping label windows across splits. Fit transformations only on training folds. Repeated customers are acceptable only if the intended use is future scoring of existing customers; evaluate unseen-customer performance separately if claimed.
5. **Establish comparisons:** start with a prevalence baseline and a simple recency rule, then compare three suitable classifier families with justified tuning, as our R4 planning target. Use the same eligible cohorts and time protocol. Tune only using development periods, keep test outcomes untouched, and record actual compute costs.
6. **Interpret and deliver:** inspect errors and performance across useful customer groups, relate findings to Module B's profiles where appropriate, freeze the model, evaluate the final period, and write practical conclusions with limitations. Predictions do not prove the causal benefit of marketing interventions.

Selected source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/metadata), chosen by the user on 2026-09-18. Version 2 was downloaded on 2026-09-21 via scripts/download_olist.py; CSV parsing, counts, and checksums were verified and recorded in docs/DATA_MANIFEST.json. Step 2 empirical diagnostics are complete; model quality remains untested. Follow the dataset rules in PROJECT_BRIEF.md. Measure repeat-purchase coverage and forecasting-series density before fixing horizons or granularity. The specific algorithms and metrics above remain proposed choices, not assignment requirements.

## Phase 1 — Establish requirements and scope

Step 1 written framing is complete in [Step 1 of notebooks/Final_Project.ipynb](../notebooks/Final_Project.ipynb#step-1). AP, silhouette, and MAE are selected as the respective primary metrics; business direction and indicative KPIs are outlined. Detailed business KPI calculations and targets will be defined during evaluation design. The notebook's context cell executed in a fresh kernel. The Phase 2 audit now informs preparation; final time splits and eligibility still need evaluation design. Step 3 now includes a small forest-based feature experiment; substantive tuned models remain pending.

1. Review the confirmed domain, three modules, Olist dataset, and management-team audience in PROJECT_BRIEF.md.
2. Define the output and acceptance check for each module.
3. Record relevant hardware, runtime limits, and external-service choices as needed for implementation.
4. Separate core analytical work from optional improvements. List unresolved technical decisions explicitly.
5. Map work to R1-R8. Outline business direction and indicative KPIs for A/B/C; define detailed KPI calculations, baselines, and measurement windows during evaluation design before model comparisons. Separate observed KPIs from assumed ROI scenarios. Review the sensitive-group coverage gap before committing to fairness claims.

Deliverable: a completed brief and project acceptance checklist.

Complete when: each selected objective has a planned output and acceptance check. Keep untested technical choices provisional.

## Phase 2 — Choose the question and establish data feasibility

Updated on 2026-09-23: notebook Step 2 uses orders, customers, and items only. Shared-key discovery, null/duplicate removal, explicit joins, a six-column consolidated DataFrame, IQR-filtered price EDA, and simple charts replace the expanded audit. Eight notebook code cells ran in a fresh kernel, including the customer observation-time check. Broader rubric dictionary coverage is tracked as partial.

1. Use the assigned topic/data if prescribed. Otherwise compare a small number of candidate questions by usefulness, data availability, scope, and compute needs.
2. State the question, intended audience, unit of analysis, and what a useful result would mean.
3. Inspect a small data sample or schema; verify source, access, permitted use, labels if needed, size, and obvious quality issues.
4. Record what information would be available at prediction/use time, if applicable.

Current deliverable: a readable Step 2 in notebooks/Final_Project.ipynb with three relevant tables, shared keys, required-field cleaning, consolidated_df, a short field guide, and IQR-filtered price EDA. Extend source/feature documentation only as needed; keep remaining R2 requirements in the tracker.

Complete when: the questions are answerable with available data and practical compute. If data cannot support a selected module, discuss adjustments before changing its scope.

## Phase 3 — Establish evaluation and the minimum runnable structure

1. Select evaluation criteria aligned with the question and rubric before optimizing results.
2. For supervised work, choose a time/group-aware or other appropriate split, a primary metric, secondary diagnostics, and a simple baseline. Keep final test data out of tuning.
3. For clustering or exploratory work, define stability, interpretability, and task-relevant validation. For generative work, define a fixed evaluation set, scoring rubric, quality/failure checks, and cost constraints. Use only the branch relevant to the assignment.
4. Verify imports in the intended environment, record direct dependencies, and define relative data paths and the notebook working directory.
5. Create only the files needed for the first complete run. Record seeds and configuration explicitly.

Deliverable: evaluation protocol, initial project layout, dependency manifest, and a quick validation command.

Complete when: a small representative input can be loaded and the evaluation procedure is specified. Detailed layout below is a proposal, not yet implemented.

## Phase 4 — Audit and explore the data

1. Check types, missing values, duplicates, labels, class balance where applicable, outliers, and possible leakage.
2. Explore the development/training data with a small set of question-driven summaries and plots. Protect any held-out test set from exploratory model decisions.
3. Document cleaning choices, exclusions, and limitations. Keep original data immutable.
4. Implement learned transformations inside the appropriate training pipeline/folds.
5. Implement and justify BOTH a feature-selection method and dimensionality reduction (R3). Candidate choices: model-based selection and scaled PCA. Compare against the original feature set, document selected variables/components and explained variance, and fit within training folds when predictive.
6. Produce interpretable distributions/correlations and business-relevant EDA findings, not just a gallery of plots. Save exclusion/reconciliation counts and transformation settings.

Deliverable: a data-quality summary, useful exploratory figures, and reproducible preprocessing.

Complete when: inputs/outputs and row-count changes are understood and cleaning decisions are justified.

## Phase 5 — Build an end-to-end baseline

1. Run the simplest suitable baseline through loading, preprocessing, evaluation, and result capture.
2. Implement the assignment's first required method using the same evaluation protocol.
3. Save actual metrics and runtime along with parameters, seeds, and data/version information.
4. Check representative predictions or outputs, including failure cases.

Deliverable: a working analysis notebook and first measured comparison.

Complete when: the full workflow runs on a small sample and then the intended development data within budget. This establishes a minimum complete project before optional complexity.

## Phase 6 — Run focused experiments

1. Implement remaining required methods and justified alternatives.
2. Keep data splits and evaluation rules comparable; record each experiment's purpose and outcome.
3. Tune on development data only with bounded searches. Run cheap checks before long jobs.
4. Analyze important errors, stability, and relevant subgroups; measure whether improvements are meaningful for the task.
5. Select the final approach using development evidence and its complexity/runtime tradeoffs.
6. Target baseline plus three classifier families for A, RFM reference plus two clustering approaches for B, and naive baseline plus two forecasting approaches for C. The rubric requires substantive comparisons/tuning, not these exact counts; document justified adjustments.
7. Save fitted models and preprocessing under models/, settings under configs/, and comparable results under reports/. Verify model reload predictions and record data hashes, cutoffs, seeds, versions, and tuning spaces (R4).

Deliverable: experiment comparison, error analysis, and a justified final choice.

Complete when: required comparisons are covered and further experiments have lower value than finishing validation and communication. A weak score should trigger honest analysis, not fabricated success or repeated test-set tuning.

## Phase 7 — Validate the final result and explain it

1. Freeze the selected approach before final held-out evaluation, if the task uses one.
2. Run final evaluation and report its limitations. Do not turn held-out results into another tuning loop without explicitly revising the evaluation design.
3. Explain the main result, failure modes, practical implications, and limits of generalization.
4. Run actual explainability tooling (SHAP/LIME/PDP/ICE as appropriate), interpret drivers and representative errors, and document correlation/causal limits.
5. Execute supported-group fairness diagnostics with counts, uncertainty, definitions, and reference groups. Report imbalance, leakage, overfitting, coverage, and generalization limits. Test feasible mitigations on development data, then freeze them before final evaluation. Follow R5's detailed protocol and keep sensitive-group coverage marked as a gap while appropriate attributes are unavailable.
6. Complete the notebook's Step 8 ethics/bias audit and Step 9 conclusions. Derive reports/final_report.md from notebook evidence. Build TWO professional decks, EACH 8-12 slides, using the 10-slide technical/business outlines in RUBRIC_ALIGNMENT.md. The business deck must cover scenario-based ROI, risks, and strategy; the technical deck must show methods, visuals, and metrics (R6).

Deliverable: final results, explanation figures, quantitative bias/mitigation evidence with unresolved gaps stated, final report, and two rendered decks plus editable sources.

Complete when: every quantitative claim traces to a real output and all conclusions are supported by the evidence.

## Phase 8 — Reproduce and document the project

1. Run structural notebook checks, then execute computational deliverables from a fresh kernel in documented order.
2. Verify environment recreation where feasible; report any remaining limitations.
3. Review required functions/pipelines with focused tests when they protect meaningful behavior, especially split and transformation boundaries.
4. Check paths, missing files, secret/sensitive outputs, filenames, and project acceptance criteria.
5. Update README.md with exact reproduction commands and STATUS.md with final evidence and any unresolved items.
6. Prepare the R7 repository with src/, notebooks/, data/, models/, README, requirements.txt, and final report. Keep a tracked data/README with acquisition instructions and a model inventory/regeneration strategy. Use real focused commits, inspect publishable contents, and verify clean-environment reproduction.
7. Prepare the complete local package before requesting authorization for public GitHub publication. R7 stays incomplete until the authorized public repository URL and contents are verified. Do not publish as a side effect of rubric integration.
8. Add the R8 creativity contribution after core evidence: a coherent A/B/C business scenario with sensitivity analysis and polished consistent visuals. Review rendered decks for clarity, slide count, and readability.

Deliverable: a reproducible project and completed acceptance checklist.

Complete when: the project reproduces as documented and R1-R8 each has verified evidence; record remaining gaps explicitly instead of assuming full marks.

## Single-notebook file layout

notebooks/Final_Project.ipynb is the only analysis notebook. Its section order is framing; data audit/dictionary; preparation/EDA/features; evaluation/baselines; segmentation (B); repeat purchases (A); forecasting (C); explainability/fairness; conclusions/reproducibility. Steps 1-3 are implemented; Steps 4-9 remain planned. The phases above describe work and completion checks, not separate notebooks. Add optional output directories only as their contents are implemented:

```text
5.0 Final Project/
  AGENTS.md
  README.md
  requirements-tools.txt
  requirements.txt         # direct dependencies used through Step 3
  docs/
    PROJECT_BRIEF.md        # scope, rubric mapping, key decisions
    PROJECT_PLAN.md         # this roadmap
    STATUS.md              # verified progress and next action
    PROMPTS.md
  notebooks/
    Final_Project.ipynb    # sole notebook for all analysis and narrative
  src/                     # shared, testable preparation/modeling/evaluation
  configs/                 # splits, seeds, features, tuning, final model settings
  data/
    raw/                   # original inputs; ignored by existing policy
    processed/             # reproducible derived inputs; ignored
    README.md              # tracked acquisition/provenance instructions
  models/                  # saved models/preprocessing and inventory
  artifacts/               # temporary/generated run outputs; ignored
  reports/                 # derived final report, generated tables and figures
  presentations/           # technical and business decks, sources and PDFs
  scripts/
    check_notebooks.py
    download_olist.py
    summarize_framing_data.py
    audit_data.py            # optional older utility; unused by active notebook
    run_notebook.py
  tests/                   # add for substantive reusable logic, when warranted
```

The proposed directory names are organizational choices. Ignored data/artifacts still need documented acquisition or regeneration steps so the project can be reproduced.

## How we will collaborate

- You supply preferences and substantive project choices where needed.
- Codex inspects files, implements authorized work, runs suitable checks, and records evidence. Routine reversible steps do not require repeated approval.
- Each work session has one concrete objective and ends with changed files, checks performed, unresolved issues, and the next action.
- Update PROJECT_BRIEF.md when scope changes and STATUS.md after meaningful milestones. Keep measured results separate from assumptions.
- Include reproduction and writing as part of each completed analytical module.

## Immediate next action

Review Step 4 findings before interpreting business actions: two broad customer groups and no forecasting gain over simple baselines. Continue with model explanations, error/coverage analysis, and supported-group fairness. Preserve the now-inspected test protocol; any new tuning needs a fresh evaluation period. Keep the sensitive-group gap explicit and build final deliverables from notebook evidence.
