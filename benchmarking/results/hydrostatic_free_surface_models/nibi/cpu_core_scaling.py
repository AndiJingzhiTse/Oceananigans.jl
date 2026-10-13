#!/usr/bin/env python3
"""Compatibility entry point for existing Nibi jobs; use benchmark_suite.py for new runs."""
from pathlib import Path as _LegacyPath
exec(compile((next(p for p in _LegacyPath(__file__).resolve().parents if (p / "legacy").is_dir()) / "legacy" / "nibi" / "cpu_core_scaling.py").read_text(), __file__, "exec"))
