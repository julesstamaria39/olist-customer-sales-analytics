# Olist data

Source: [Brazilian E-Commerce Public Dataset by Olist, version 2](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/versions/2). Publisher: Olist. Publisher-listed license: CC BY-NC-SA 4.0. Preserve attribution and source terms when reusing data.

Raw CSVs live in `raw/olist/` and are excluded from version control. Derived data should go into `processed/` and must be reproducible from raw inputs.

From `5.0 Final Project`:

```powershell
.venv\Scripts\python.exe scripts/download_olist.py
.venv\Scripts\python.exe scripts/download_olist.py --verify-only
```

Install the acquisition tools from requirements-tools.txt if needed. See the [project README](../README.md) for environment details and [data manifest](../docs/DATA_MANIFEST.json) for the source version, acquisition time, original file hashes, row counts, and columns. The downloader does not overwrite unverified existing data.

Acquisition/integrity checks are complete. The single project notebook now uses three relevant tables for a readable consolidation, basic cleaning, and EDA workflow. The earlier expanded source audit has been replaced. Raw files are preserved; model results and limitations are recorded in the final report. No protected demographic attributes should be invented to fill the fairness requirement. See the [rubric tracker](../docs/RUBRIC_ALIGNMENT.md) for the documented gap.
