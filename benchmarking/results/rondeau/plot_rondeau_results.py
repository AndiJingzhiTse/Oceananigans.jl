#!/usr/bin/env python3
"""Historical plot compatibility entry point."""
from pathlib import Path as _LegacyPath
exec(compile((_LegacyPath(__file__).resolve().parents[2] / "legacy" / "rondeau" / "plot_rondeau_results.py").read_text(), __file__, "exec"))
