# Olist Customer and Sales Analytics

An eCommerce capstone using historical Olist transactions to explore **customer segments** and **product sales forecasts**. One Jupyter notebook contains the complete analysis; reusable code lives in `src/olist_analytics/`.

## Results at a glance

- **Customer segmentation:** K-Means finds two broad groups among 6,000 sampled customers. The single-order group is 96.7% of customers and contributes 93.8% of recorded sample spending.
- **Weekly forecasting:** Random Forest is the best tested ML candidate, but its test MAE of **1.021 items** is worse than the four-week mean benchmark's **0.894**.
- **Daily forecasting:** calendar-only Random Forest has MAE **0.850**, versus **0.817** for its benchmark. It matches **0 of 5** observed product trend directions.
- **Responsible use:** these findings support investigation, not automated offers or inventory decisions. Geographic auditing does not establish protected-group fairness. Presentation ROI is explicitly hypothetical.

Repeat-purchase classification was retired after the feasibility review; repeat behavior remains descriptive EDA. Sales counts represent approved-order item records, not total demand, profit or verified deliveries.

## Read the deliverables

| Deliverable | Files |
| --- | --- |
| Final report | [PDF with charts](reports/final_report.pdf) ? [Markdown](reports/final_report.md) |
| Complete analysis | [Final_Project.ipynb](notebooks/Final_Project.ipynb) |
| Technical presentation | [PowerPoint](presentations/technical_deck.pptx) ? [PDF](presentations/technical_deck.pdf) |
| Business presentation | [PowerPoint](presentations/business_deck.pptx) ? [PDF](presentations/business_deck.pdf) |
| Evidence | [Tables](reports/tables/) ? [Figures](reports/figures/) ? [Configurations](configs/) |

Both presentations contain 10 slides. Product numbers are local labels: use the saved product tables to identify their product IDs; daily and weekly top-five lists differ.

## Repository structure

```text
src/olist_analytics/  Reusable forecasting and fairness code
notebooks/           One executed analysis notebook
scripts/             Download, execution, checks and export utilities
data/                Source attribution and acquisition instructions
models/              Model inventory and regeneration instructions
configs/             Features, cutoffs, seeds and model settings
reports/             Final report, charts and result tables
presentations/       Two decks, PDFs and illustrative ROI scenarios
docs/                Data manifest, scope history, rubric and status
```

Raw/processed datasets, fitted model binaries, local environments and temporary artifacts are excluded from Git. Running the notebook regenerates the models and derived data. Older scope notes in `docs/` record planning history; the active scope and results above take precedence.

## Reproduce the analysis

Use **Python 3.13**. Clone with `git clone https://github.com/julesstamaria39/olist-customer-sales-analytics.git`, enter `olist-customer-sales-analytics`, then create an isolated environment and install the pinned direct dependencies:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts/download_olist.py
.venv\Scripts\python.exe scripts/download_olist.py --verify-only
.venv\Scripts\python.exe scripts/run_notebook.py
.venv\Scripts\python.exe scripts/check_notebooks.py notebooks/Final_Project.ipynb
.venv\Scripts\python.exe scripts/check_daily_forecasting.py
.venv\Scripts\python.exe scripts/check_bias_audit.py
```

On macOS/Linux, substitute `.venv/bin/python` for `.venv\Scripts\python.exe`. The analysis uses repository-relative paths. Local packaging validation is performed on Windows; other operating systems are not verified here. Select the same environment as your notebook kernel when running interactively.

The downloader retrieves **Olist version 2** and verifies nine original CSVs against [DATA_MANIFEST.json](docs/DATA_MANIFEST.json). If Kaggle requests authentication, configure it locally; never commit credentials. The notebook runner starts a fresh kernel, executes cells in order, checks model reloads and writes outputs only after success. Do not run it alongside an interactive notebook execution.

The source data remain unchanged. Dependencies are direct version pins, not a full cross-platform lockfile. See [STATUS.md](docs/STATUS.md) for the exact reproduction checks performed.

## Regenerate the report and slides

Install optional exporters into the same environment, then build from the notebook's saved evidence:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-presentations.txt
.venv\Scripts\python.exe scripts/export_report_pdf.py
.venv\Scripts\python.exe scripts/build_presentations.py
```

The exporters currently use Windows Arial font files. Committed PDFs and PowerPoints can be opened without these dependencies. Rebuilds overwrite generated files; save any manual deck edits before rebuilding. PowerPoint checks use matching PDF renders, not native Office rendering.

## Evaluation and limitations

Forecasting uses chronological training, validation and test periods. Product selection uses early training history. Features contain only information available at prediction time; the daily experiment uses calendar inputs only. Clustering is a descriptive sampled analysis with stability checks, not a predictive test on new customers.

The historical forecast test period was inspected before the later ML-only selection policy and daily extension. That history is disclosed; these results are not newly untouched evaluations. Models do not beat simple baselines overall. Sparse sales, the short observation period and missing stock data limit interpretation. Gender, race, age and income are unavailable, and proposed fairness mitigations have not been validated.

## Data attribution and contribution

Data: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/versions/2), publisher-listed license **CC BY-NC-SA 4.0**. See [NOTICE.md](NOTICE.md), [data/README.md](data/README.md) and [CONTRIBUTING.md](CONTRIBUTING.md). No separate open-source code license has been selected.

## Publication status

Public repository: [https://github.com/julesstamaria39/olist-customer-sales-analytics](https://github.com/julesstamaria39/olist-customer-sales-analytics). Published and verified on 24 September 2026. The required source, notebook, data instructions, model inventory, report and decks are present.
