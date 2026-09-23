"""Compatibility import; implementation is in src/olist_analytics/bias_audit.py."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.olist_analytics.bias_audit import *  # noqa: F401,F403
