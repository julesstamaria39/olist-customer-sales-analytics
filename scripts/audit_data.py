"""Reusable, read-only table profiling helpers; analysis stays in the notebook."""

from pathlib import Path
import hashlib

import pandas as pd


def load_tables(raw_directory, filenames, manifest, date_columns, numeric_types):
    """Verify original files and parse explicit types without changing the CSVs."""
    tables = {}
    checks = []
    for name, filename in filenames.items():
        path = Path(raw_directory) / filename
        expected = manifest["files"][filename]
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != expected["sha256"]:
            raise ValueError(f"Source checksum changed: {filename}")

        # Read identifiers as strings, including postal-code prefixes.
        frame = pd.read_csv(path, dtype="string")
        if len(frame) != expected["rows"] or list(frame.columns) != expected["columns"]:
            raise ValueError(f"Source rows or columns changed: {filename}")
        for column in frame:
            source = frame[column]
            if column in date_columns:
                parsed = pd.to_datetime(source, format="%Y-%m-%d %H:%M:%S", errors="coerce")
            elif column in numeric_types:
                parsed = pd.to_numeric(source, errors="coerce")
            else:
                continue
            failures = int((source.notna() & parsed.isna()).sum())
            checks.append({"table": name, "field": column, "parse_failures": failures})
            if failures:
                raise ValueError(f"{name}.{column}: {failures} values failed parsing")
            if column in numeric_types:
                parsed = parsed.astype(numeric_types[column])
            frame[column] = parsed
        tables[name] = frame
    return tables, pd.DataFrame(checks)


def table_inventory(tables):
    """Summarize source sizes, exact repeated rows, and missing cells."""
    rows = []
    for name, frame in tables.items():
        rows.append({
            "table": name, "rows": len(frame), "columns": len(frame.columns),
            "exact_duplicate_rows": int(frame.duplicated().sum()),
            "missing_cells": int(frame.isna().sum().sum()),
        })
    return pd.DataFrame(rows)


def profile_columns(tables):
    """Observed types, missingness, uniqueness, and ranges for every field."""
    rows = []
    for name, frame in tables.items():
        for column, values in frame.items():
            observed = values.dropna()
            unique = int(observed.nunique())
            if observed.empty:
                summary = "No observed values"
            elif pd.api.types.is_numeric_dtype(values) or pd.api.types.is_datetime64_any_dtype(values):
                summary = f"{observed.min()} to {observed.max()}"
            elif unique <= 30:
                summary = ", ".join(sorted(observed.unique()))
            else:
                lengths = observed.str.len()
                summary = f"{unique:,} distinct strings; {lengths.min()}-{lengths.max()} characters"
            rows.append({
                "table": name, "field": column, "loaded_type": str(values.dtype),
                "missing": int(values.isna().sum()),
                "missing_pct": round(float(values.isna().mean() * 100), 3),
                "distinct": unique, "observed_range_or_values": summary,
            })
    return pd.DataFrame(rows)


def key_check(table_name, frame, columns):
    """Inspect a candidate key; duplicates count rows beyond the first."""
    return {
        "table": table_name, "candidate_key": " + ".join(columns),
        "missing_key_rows": int(frame[columns].isna().any(axis=1).sum()),
        "duplicate_key_rows": int(frame.duplicated(columns).sum()),
    }


def relationship_check(child_name, child, child_key, parent_name, parent, parent_key):
    """Measure unmatched foreign keys without materializing a multiplying join."""
    values = child[child_key]
    unmatched = values.notna() & ~values.isin(parent[parent_key].dropna())
    return {
        "relationship": f"{child_name}.{child_key} -> {parent_name}.{parent_key}",
        "parent_key_unique": bool(parent[parent_key].is_unique),
        "missing_child_key_rows": int(values.isna().sum()),
        "unmatched_child_rows": int(unmatched.sum()),
        "unmatched_distinct_keys": int(values[unmatched].nunique()),
    }


def numeric_profile(tables, excluded_columns=()):
    """Describe numeric distributions; IQR flags are review prompts, not deletions."""
    rows = []
    for name, frame in tables.items():
        for column in frame.select_dtypes(include="number"):
            if column in excluded_columns:
                continue
            values = frame[column].dropna()
            q1, median, q3 = values.quantile([0.25, 0.5, 0.75])
            iqr = q3 - q1
            flagged = (values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)
            rows.append({
                "table": name, "field": column, "observed": len(values),
                "min": values.min(), "q25": q1, "median": median,
                "q75": q3, "p99": values.quantile(0.99), "max": values.max(),
                "zero_values": int(values.eq(0).sum()),
                "negative_values": int(values.lt(0).sum()),
                "iqr_flag_pct": round(float(flagged.mean() * 100), 2),
            })
    return pd.DataFrame(rows)
