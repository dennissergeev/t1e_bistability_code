# -*- coding: utf-8 -*-
"""Paths to data."""
from pathlib import Path

home = Path.home()

# Top-level directory containing code and data (one level up)
topdir = Path(__file__).absolute().parent.parent

# Modelling results
datadir = topdir.parent.parent / "modelling" / "um" / "results"

sadir = datadir / "sa"  # standalone suites directory

constdir = topdir / "code" / "const"

# Plotting output
plotdir = topdir / "plots"
# plotdir = topdir.parent / "plots"
plotdir.mkdir(parents=True, exist_ok=True)

# TeX output (tables)
tabdir = topdir / "tables"
tabdir.mkdir(parents=True, exist_ok=True)
