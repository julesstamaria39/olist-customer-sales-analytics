"""Download pinned Olist data, or verify the existing files without network access."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"
MANIFEST_PATH = PROJECT_ROOT / "docs" / "DATA_MANIFEST.json"
DATASET_HANDLE = "olistbr/brazilian-ecommerce/versions/2"
EXPECTED_FILES = (
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
)


def inventory(data_dir: Path) -> dict:
    """Read CSV records and hash original bytes without rewriting raw data."""
    result = {}
    for name in EXPECTED_FILES:
        path = data_dir / name
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            columns = next(reader)
            if not columns or len(columns) != len(set(columns)):
                raise ValueError(f"Invalid column header: {name}")
            rows = 0
            for row in reader:
                if len(row) != len(columns):
                    raise ValueError(f"Invalid CSV width in {name}, record {rows + 1}")
                rows += 1
        if rows == 0:
            raise ValueError(f"Empty CSV: {name}")
        result[name] = {
            "bytes": path.stat().st_size,
            "sha256": digest,
            "rows": rows,
            "columns": columns,
        }
    return result


def verify_existing() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("dataset_handle") != DATASET_HANDLE:
        raise ValueError("Manifest dataset version does not match the script.")
    actual = inventory(DATA_DIR)
    if actual != manifest.get("files"):
        raise ValueError("Raw files differ from DATA_MANIFEST.json; originals were not overwritten.")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Check local files without downloading.")
    args = parser.parse_args()

    if MANIFEST_PATH.exists():
        saved_manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if saved_manifest.get("dataset_handle") != DATASET_HANDLE:
            raise ValueError("Manifest dataset version does not match the script.")

    has_local_files = DATA_DIR.exists() and any(DATA_DIR.iterdir())
    if args.verify_only or (MANIFEST_PATH.exists() and has_local_files):
        records = verify_existing()
        print("Verified existing Olist files against the recorded manifest (no download).")
    else:
        if has_local_files:
            raise ValueError(
                "Raw directory is nonempty but has no manifest. Inspect it before retrying; "
                "existing files will not be overwritten."
            )
        # Import only for acquisition, so verification works without KaggleHub.
        import kagglehub

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {DATASET_HANDLE} to {DATA_DIR}", flush=True)
        downloaded = Path(kagglehub.dataset_download(DATASET_HANDLE, output_dir=str(DATA_DIR)))
        if downloaded.resolve() != DATA_DIR.resolve():
            raise ValueError("KaggleHub returned an unexpected download directory.")
        records = inventory(DATA_DIR)
        manifest = {
            "dataset_handle": DATASET_HANDLE,
            "source_url": "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/versions/2",
            "publisher": "Olist",
            "publisher_listed_license": "CC BY-NC-SA 4.0",
            "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
            "download_tool": {"kagglehub": version("kagglehub"), "kagglesdk": version("kagglesdk")},
            "raw_directory": "data/raw/olist",
            "files": records,
        }
        if MANIFEST_PATH.exists():
            # Fresh checkout: raw data is ignored, but the provenance manifest is tracked.
            if records != saved_manifest.get("files"):
                raise ValueError("Downloaded files differ from the recorded manifest.")
            print("Downloaded files match the existing manifest; original provenance retained.")
        else:
            MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
            with MANIFEST_PATH.open("x", encoding="utf-8") as stream:
                json.dump(manifest, stream, indent=2)
                stream.write("\n")
            print(f"Recorded source version, acquisition time, CSV counts, and hashes in {MANIFEST_PATH}")

    for name, record in records.items():
        print(f"  {name}: {record['rows']:,} rows, {len(record['columns'])} columns")
    print("Acquisition checks complete. Modeling feasibility has not been assessed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, csv.Error, StopIteration) as exc:
        print(f"Acquisition/verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
