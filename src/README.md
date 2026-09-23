# Reusable analysis code

`olist_analytics/` contains the implementation used by the single notebook:

- `forecasting.py`: chronological weekly model selection, forecasts and charts.
- `daily_forecasting.py`: calendar-only daily Random Forest experiments.
- `bias_audit.py`: PDP/ICE explanations and geographic disparity checks.

Run the notebook from the repository using the root README instructions. The matching files under `scripts/` preserve older imports; acquisition, execution, checks and report exporters remain utilities there. The model methods and evaluation dates have not changed during packaging.
