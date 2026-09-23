# Rubric alignment and evidence tracker

## Current delivery status - 2026-09-24

The active scope is B customer segmentation and C weekly/daily sales forecasting; A classification is retired. The combined final report and two 10-slide decks are complete. All 36 notebook code cells passed in a fresh Windows/Python 3.13 environment (27.0 seconds), with raw-data checksum, model reload, temporal-leakage and fairness-calculation checks. Raw data were verified locally, not freshly downloaded in that run. Public GitHub publication was explicitly authorized by the user's Step 7 request. The [public repository](https://github.com/julesstamaria39/olist-customer-sales-analytics) was published and verified on 24 September 2026 with all required directories and deliverables. R7 delivery is verified for this Windows environment; other platforms are not tested. This update supersedes older planning/status statements below. Protected-group evidence and mitigation validation remain gaps; no grade or full fairness compliance is claimed.

Step 3 report packaging (24 September 2026): reports/final_report.md now includes the EDA + Feature Engineering Report, with executed findings, justifications, figures and links to reproducible notebook code and artifacts. It covers the implemented R3 work and preserves the PCA/no-improvement and generalization limits. The existing Bias & Fairness Analysis remains intact; this does not imply completion of all final-report chapters or remaining rubric gaps.

Step 6 milestone (24 September 2026): technical_deck.pptx and business_deck.pptx contain 10 slides each, with matching PDFs, evidence footers, notes, reproducible generation and explicit ROI assumptions. Both native files reopened and all 20 matching PDF pages were reviewed; native Office rendering is unavailable. R6 deliverables exist and are checked; remaining report, fairness and publication work is not implied complete.

Step 5 milestone (24 September 2026): actual weekly-model PDP/ICE, fit/validation/test diagnostics, zero-versus-positive-sales error analysis, and a state-based hypothetical outreach audit are implemented. The latter reports selection-rate differences/ratios and Wilson rate intervals, with minimum group counts and chronological state assignment. Proposed mitigations and the missing sensitive-attribute/outcome limits are explicit. The requested Bias & Fairness Analysis is generated into reports/final_report.md; the rest of the report remains pending. This is partial R5 coverage, not a completed protected-group fairness audit.

Section 4.9 (24 September 2026) adds daily Random Forest predictions, training-only top-five selection, chronological train/validation/test separation, a fixed average benchmark, trend comparisons, saved artifacts, and a future-outcome mutation check. This adds R4 comparison and limitation evidence, not demonstrated forecasting improvement: MAE 0.850 versus benchmark 0.817, with 0/5 trend labels matched. All 31 notebook code cells executed; the previously inspected historical test period is disclosed. Earlier weekly split checks and descriptive clustering/stability practices were reviewed; no unseen-customer performance is claimed.

Presentation update (24 September 2026): forecasting Sections 4.5-4.8 now use short explanations and three focused charts. Supporting code is in scripts/forecasting.py; detailed comparisons remain in reports/tables/ and configs/. R4 computations and R5 input-reliance evidence are preserved. All 29 notebook code cells executed successfully, with unchanged predictions. This simplification does not resolve existing rubric gaps.

## Current model milestone - 2026-09-23

Step 4 now includes trained/tuned K-Means and DBSCAN comparisons for B and Decision Tree/Random Forest regressors for C, with matching baselines, chronological forecast evaluation, metrics, configs, and reload-verified model artifacts. Lag 3 is included. B selects a broad two-group K-Means sample segmentation; C selects Random Forest as the best ML candidate by existing validation MAE, while the four-week mean and last-week rules are benchmarks only. This ML-only policy was requested on 24 September 2026 after the earlier test had been inspected; settings and predictions are unchanged. Random Forest does not beat the overall benchmark. The notebook includes validation input-reliance analysis, all-product forecast examples, and product-level planning limitations. Test results and limitations are recorded in the notebook and STATUS.md. The April-July test outcomes are now inspected; do not retune on them while calling them untouched. Earlier planning text below is superseded for this milestone. Next: interpretation/explainability and supported-group fairness, with the existing protected-attribute gap unresolved.


## Active scope update - 2026-09-23

The user removed A (repeat-purchase prediction) from modeling after the feasibility review. Repeat behavior remains descriptive EDA. **B customer segmentation and C observed-sales forecasting are the active tasks.** This decision supersedes earlier A/B/C scope statements and classifier plans below. The supplied rubric asks for justified task types, not mandatory classification.

Step 3 now uses a single pre-2-April-2018 customer snapshot, correlation-based feature selection, median/log/scaling preparation, and PCA for B; weekly product lags remain for C. No repeat labels, classifiers, or AP comparisons are run. Active artifacts are data/processed/customer_profiles.csv, customer_features_scaled.csv, customer_features_pca.csv, product_week_features.csv, and artifacts/step3_bc/. Prior classifier artifacts are retired. Model importance/explainability will be addressed through forecasting; clustering comparisons and final evaluation remain pending. R3 does not yet establish that PCA improves clustering, and R4/R5 remain incomplete.


## Objective and source

Build the eCommerce project to meet every Outstanding/Exemplary descriptor in the user's [Pillar 5 rubric](RUBRIC_SOURCE.txt). Target: **100/100 available points = 95 core + 5 bonus**. This is an evidence and quality target, not a promised grade or permission to fabricate results. Final marks belong to the evaluator.

The supplied rubric now governs required project outputs, including presentations and the public repository. Deadlines remain excluded as requested. Preserve the confirmed Olist dataset and all three modules: A repeat-purchase classification, B customer segmentation, C sales forecasting.

Section 3.2 also includes executed order-group summaries and spending box plots by recency band, with missingness counts and interpretation (R3).

Additional Step 4 visual evidence compares clustering separation/coverage/stability and forecast error across periods, products, and horizons. These charts support R4 interpretation; the 24 September ML-only selection revision is explicitly recorded.

Step 4 now interprets customer behavior and product planning outcomes with measured segment shares, repeat/variety rates, product categories, unique weekly actuals, zero-sales coverage, and explicit action hypotheses. These support business communication; no causal ROI or full fairness coverage is claimed.

## Tracking rules

- Status values: Planned, Partial, Verified, Gap. Verified requires an actual artifact plus a recorded check; a plan or empty file does not count.
- All analysis evidence belongs in notebooks/Final_Project.ipynb; Step 2 has executed focused consolidation/cleaning/EDA evidence; Step 3 has executed customer/product features, selection, PCA, and development comparison evidence; sections 4-9 remain planned. Final report/decks are derived deliverables.
- Paths below are planned outputs unless linked to existing evidence. Add file/cell/figure references and verification commands as work is completed.
- Treat model scores, business outcomes, fairness, and rubric completion as separate claims. Do not assign ourselves earned points.
- Reassess this table after every milestone. Preserve failed experiments and unresolved limitations when they inform decisions.

## Maximum-points criteria

| ID | Criterion | Available points | Evidence needed for Outstanding/Exemplary | Planned output | Current evidence/status |
| --- | --- | ---: | --- | --- | --- |
| R1 | Problem understanding and framing | 10 | Strong business and data-science framing; justified task types; measurable technical metrics and business KPIs | [Notebook Step 1](../notebooks/Final_Project.ipynb#step-1); PROJECT_BRIEF.md | Partial R1 coverage: initial task framing, technical metrics, baselines, indicative business KPIs, risks, and Capstone linkage documented; detailed business KPI calculations/targets deferred to evaluation design; context cell executed in fresh kernel. The R2 audit informs the provisional horizons; final splits and detailed KPI targets remain pending evaluation design. No model results or earned points claimed |
| R2 | Data collection and understanding | 10 | Justified, cited dataset; feature types, missingness, outliers, distributions; complete dictionary with types, ranges, units | [Notebook Step 2: audit and dictionary](../notebooks/Final_Project.ipynb#step-2) | Partial: simplified three-table source selection, shared-key discovery, six-field working dictionary, null/duplicate removal, consolidated item table, IQR-filtered price EDA. The previous complete 52-field audit is no longer in the active notebook; broader dictionary/range coverage remains pending where required. |
| R3 | Preprocessing, EDA, and feature engineering | 10 | Reproducible documented cleaning; null/outlier/duplicate policies; insightful visuals, distributions, correlations; domain features; at least one justified feature-selection method AND one dimensionality-reduction method | [Notebook Step 3](../notebooks/Final_Project.ipynb#step-3); reusable src/ utilities; generated reports/figures/ | Partial: executed cleaning/EDA, historical B/C features including lag_3, correlation selection, scaling, PCA, and original-versus-two-component clustering comparison. No PCA improvement claimed; Forecasting now includes validation permutation importance with correlated-input limitations; remaining R5 explainability requirements and fairness remain open. |
| R4 | Model implementation and comparison | 20 | Multiple appropriately tuned models; correct comparable metrics; saved models/configurations; result-based selection rationale | [Notebook Steps 4-7](../notebooks/Final_Project.ipynb#step-4); models/; configs/; reports/model_comparison.csv | Implemented comparisons: 22 clustering trials, stability/profile/reference checks; 12 forecasting settings across 3 mature-target temporal folds, frozen later-period comparison against 2 baselines. Models/configs/results saved and reload-verified. Random Forest selected within ML candidates using existing validation scores; simpler benchmarks still outperform overall; clean-environment reproduction remains unverified. |
| R5 | Critical thinking, ethical AI, and bias audit | 20 | Explainability tools with interpreted findings; imbalance/leakage/overfitting limitations; sensitive-group audit with fairness metrics; feasible mitigations | [Notebook Step 5](../notebooks/Final_Project.ipynb#step-5); [Bias & Fairness Analysis](../reports/final_report.md) | Partial: executed PDP/ICE, temporal fit/error diagnostics, geographic selection-rate gap/ratio and uncertainty, and proposed mitigations. Gender/race/age/income are absent; no true eligibility outcome for equalised odds. Geographic results do not establish sensitive-group fairness; mitigations are proposed, not validated. |
| R6 | Final presentation and communication | 10 | TWO professional concise decks, EACH 8-12 slides; technical methodology/visuals/metrics; business ROI/risks/strategy for nontechnical audience | [Technical PowerPoint](../presentations/technical_deck.pptx); [Business PowerPoint](../presentations/business_deck.pptx); matching PDFs and scripts/build_presentations.py | Verified deliverables: two 10-slide decks with visuals, notes, source references, and explicitly hypothetical ROI. Files reopen; 20 shared-layout PDF pages visually checked. Native Office rendering remains unverified; no grade awarded by this tracker. |
| R7 | GitHub profile and upload | 15 | Public repository with src/, notebooks/, data/, models/; README, requirements.txt, final report, reproducible code, clean professional history | public repository URL; README.md; requirements.txt; reports/final_report.md | Partial: local setup/acquisition reproducible; public repo, full structure, report, environment recreation, and commit history pending |
| R8 | Creativity and presentation bonus | 5 | Demonstrable originality and presentation quality beyond core criteria | integrated scenario analysis and cohesive figures in reports/decks | Planned; bonus work follows core coverage |
| Total | Core plus bonus | 100 | All criteria supported by inspectable evidence | Final rubric review | Not yet achieved |

## R1: measurable technical and business success

Define each KPI's population, formula, time window, baseline, and evidence source before evaluation. Set defensible comparison targets using business assumptions and development data; do not promise arbitrary accuracy.

Step 1 supplies initial framing and business direction in [Notebook Step 1](../notebooks/Final_Project.ipynb#step-1). Its selected primary metrics are AP (A), silhouette with stability checks (B), and MAE (C), with baseline-relative targets. At the user's request, Section 5 stays directional. The guidance below is for later evaluation design; detailed business KPI calculations and targets are pending, and no achieved performance is claimed.

- **A — classification:** predict a qualifying repeat purchase within an audited horizon. Candidate technical metrics: average precision versus prevalence baseline, precision/recall at a validation-chosen threshold, calibration. Candidate business KPI: precision/lift among the top-k customers within a stated contact capacity. This measures ranking usefulness, not causal campaign uplift.
- **B — clustering:** describe historical customer groups. Evaluate separation, stability, cluster sizes, and interpretable feature profiles. Business KPIs can include customer/revenue share by segment and coverage of a documented planning action. Segment narratives must follow observed profiles, not stereotypes or invented labels.
- **C — forecasting/regression:** forecast defined weekly observed-sales counts for eligible products or, if agreed after inspection, categories. Report MAE, forecast bias, and improvement over a simple baseline on matching forecast origins. Business KPIs: planning error reduction and scenario-based over/under-forecast cost. Sales alone do not reveal lost demand or optimal stock levels.
- **ROI:** label assumptions for contact cost, contribution margin, intervention uplift, holding cost, and stockout cost. Use sensitivity/break-even analysis when intervention/cost evidence is absent. For a marketing scenario: incremental contribution = contacts x assumed incremental purchase probability x assumed margin; net benefit subtracts contact/program cost. Never substitute predicted purchase probability for incremental treatment effect. Zero cost makes an ROI ratio undefined; show net benefit instead.

## R2-R3: data and transformation evidence

- Dictionary covers every source column and engineered feature used, with definition, type, unit, observed range/categories, missingness, key/join role, and known availability time. Preserve leading zeros in geographic identifiers. Distinguish identifiers from measurements.
- Audit nulls, duplicates at the correct table grain, anomalies, distributions, chronology, join cardinality, and row-count/revenue reconciliation. Retain raw inputs; explain every exclusion or imputation.
- Build customer features from history only; count distinct orders rather than item lines. Create sales lags/rolling features using past data only. Verify final order statuses, reviews, and delivery outcomes are not used before they were known.
- Apply a real feature-selection procedure within training folds (candidate: model-based selection or recursive feature elimination), and compare selected versus full features.
- Apply and justify dimensionality reduction (candidate: scaled PCA for correlated customer numeric features), report explained variance and retained components, and compare with the original feature representation. Fit scaling/PCA within training splits where used predictively; a decorative PCA plot alone is insufficient evidence of a justified method.
- Document EDA findings beneath figures and state their practical implications. Use development data for modeling decisions; held-out outcomes remain protected.

## R4: substantive comparisons and reproducibility

The rubric does not prescribe an exact model count. Our planning target for clear coverage is: A baseline plus three suitable classifier families; B a transparent RFM reference plus two clustering approaches; C a naive baseline plus two suitable forecasting approaches. Final algorithms depend on the audit and compute feasibility. Do not silently reduce to one minimally tuned model.

- Use comparable eligible populations, chronological folds/forecast origins, metrics, and preprocessing rules. Preserve a final holdout.
- Record tuning spaces, selected parameters, seeds, runtime, data hashes, split cutoffs, software versions, and results. Tune on development data only.
- Evaluate variability across folds/origins and justify choices using performance, interpretability, runtime, and stability. A complex model need not win.
- Save fitted preprocessing with models, configuration files, and output schemas. Verify reloaded artifacts reproduce predictions. Keep a model inventory with training data version and limitations.

## R5: explainability, sensitive-group coverage, and mitigation

1. Use at least one actual explainability tool such as SHAP, LIME, PDP, or ICE. Explain global drivers and representative successes/failures, relate findings to business context, and discuss correlated-feature limits. Explain predictive associations without claiming causation.
2. Explicitly evaluate class imbalance, cohort selection, leakage, overfitting, sparse repeats, data age/coverage, forecasting sparsity, and generalizability.
3. Inspect whether any available group has a justified sensitive-group interpretation. The manifest has location fields but no explicit age, gender, or race. State/region can support geographic disparity analysis; they are not validated demographic labels. Do not infer individual protected characteristics from names, reviews, ZIP codes, or geography.
4. For supported groups, report sample/positive counts and uncertainty alongside selection rates, TPR/FNR, FPR, precision, and calibration; summarize relevant differences/ratios at a fixed validation-selected decision rule. Explain the chosen fairness definitions, tradeoffs, and reference group. Mark metrics undefined for groups with missing denominators and avoid conclusions from tiny samples.
5. Geography-based checks may proceed, but **R5's sensitive-group component remains a documented gap** until appropriate, legitimately available group data or a confirmed acceptable scope exists. Do not manufacture attributes, relabel proxies as protected classes, or mark full compliance because a fairness section exists. Any enrichment or dataset/scope change needs a concrete proposal consistent with user authorization.
6. Propose feasible mitigations and evaluate those supported by data: improve coverage, review potentially harmful proxy features, compare weighting/regularization choices, or route uncertain cases to review. Select mitigations on development data and report before/after utility and disparity. Do not promise parity or treat unequal rates alone as proof of discrimination.

## R6: two presentation outlines

Each deck will contain **10 slides** (within the required 8-12), with readable charts, consistent styling, source notes, and editable originals plus PDF exports. Populate with real results only.

| Slide | Technical deck | Business deck |
| ---: | --- | --- |
| 1 | Problem, active tasks, and main finding | Executive decision and project purpose |
| 2 | Dataset, joins, and units of analysis | Customer/operations decisions and scope |
| 3 | Feature engineering, selection and PCA | Customer segments and spending implications |
| 4 | Temporal evaluation and tuning design | First-purchase investigation and outreach |
| 5 | Clustering comparison and stability | Forecast readiness and benchmarks |
| 6 | Weekly models and benchmark comparison | Product activity and planning priorities |
| 7 | Daily forecasts and observed direction | ROI scenarios and break-even assumptions |
| 8 | PDP/ICE findings | Risks, fairness, and data limitations |
| 9 | Bias metrics, limitations, mitigations | Pilot strategy and measurement plan |
| 10 | Reproduction, conclusions, remaining gaps | Recommendations, success KPIs, next steps |

Designated technical notes/final report carry detail that would clutter slides. Review the rendered PDFs for clipping, legibility, and audience fit, not merely slide count.

## R7-R8: publication readiness and originality

- Build src/, notebooks/, data/, models/, configs/, reports/, presentations/, and tests/ as their contents are implemented. Add a data/README with download/regeneration instructions so an ignored raw-data directory does not disappear from the public project.
- Keep secrets and raw customer-level data out of commits by default. Provide dataset attribution, requirements.txt, runnable entry points, final report, and an environment verified in a clean setup. Include saved-model provenance and an explicit distribution/regeneration strategy.
- Use genuine, focused commits with useful messages; never fabricate history or backdate activity. Inspect the repository before publication. Public upload is a required final artifact, but this rubric-integration request does not authorize publishing or creating a remote repository now. Keep R7 incomplete until publication is authorized and the public URL is verified.
- Bonus proposal: one coherent customer-and-sales decision scenario joining A/B/C findings with clear assumptions and sensitivity plots. Use consistent, accessible visual design. An additional dashboard is optional and must not replace core evidence.

## Current priority

Step 1 initial framing and simplified Step 2 consolidation/EDA are documented and checked. Step 3 feature preparation, selection, and PCA are implemented. Next freeze Step 4 evaluation choices (R4), then perform substantive tuned model comparisons. Keep missing R2 detail recorded without restoring the complex notebook workflow by default. Detailed business KPI targets remain pending (R1); retain the sensitive-group gap (R5). R4 and R5 jointly account for 40 points and need substantive work, not final-stage prose. Model, fairness, slide, and publication outputs remain incomplete.
