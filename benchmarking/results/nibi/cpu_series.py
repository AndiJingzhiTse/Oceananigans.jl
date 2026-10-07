#!/usr/bin/env python3
"""Compatibility entry point for existing Nibi jobs; use benchmark_suite.py for new runs."""
from pathlib import Path as _LegacyPath
exec(compile((_LegacyPath(__file__).resolve().parents[2] / "legacy" / "nibi" / "cpu_series.py").read_text(), __file__, "exec"))
