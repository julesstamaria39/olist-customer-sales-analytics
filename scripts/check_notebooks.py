"""Read-only notebook schema/error checks; does not execute notebook code."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
import warnings

import nbformat


def check_notebook(path: Path) -> list[str]:
    """Return actionable issues without modifying the supplied notebook."""
    try:
        text = path.read_text(encoding="utf-8-sig")
        if not text.strip():
            return ["file is empty; save the notebook before validation"]
        notebook = json.loads(text)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot read notebook: {exc}"]

    issues: list[str] = []
    # Work on a copy: nbformat versions can normalize metadata during validation.
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            nbformat.validate(copy.deepcopy(notebook))
        issues.extend(f"schema warning: {item.message}" for item in caught)
    except Exception as exc:
        return [f"invalid notebook schema: {exc}"]

    seen_ids: set[str] = set()
    for number, cell in enumerate(notebook.get("cells", []), start=1):
        cell_id = cell.get("id")
        if cell_id is not None:
            if cell_id in seen_ids:
                issues.append(f"cell {number}: duplicate ID {cell_id!r}")
            seen_ids.add(cell_id)
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                issues.append(
                    f"cell {number}: stored {output.get('ename', 'error')}: "
                    f"{output.get('evalue', '')}"
                )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.notebooks:
        issues = check_notebook(path)
        if issues:
            failed = True
            print(f"FAIL {path}")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"PASS {path} (structure and saved errors only; not executed)")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
