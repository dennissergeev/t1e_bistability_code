#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interpolate UM output to pressure levels."""
import numpy as np
from tqdm import tqdm

from aeolus.const import add_planet_conf_to_cubes, init_const
from aeolus.coord import interp_cubelist_from_height_to_pressure_levels
from aeolus.io import load_data, save_cubelist
from aeolus.model import um

from commons import GLM_SUITE_ID, OPT_LABELS, SUITE_LABELS
from pouch.clim_diag import calc_derived_cubes
import mypaths


P_LEVELS = np.arange(950, 0, -50) * 1e2

img_prefix = "ch111_spinup"
time_prof = "mean_days0_499"
plotdir = mypaths.plotdir / "sa" / GLM_SUITE_ID / img_prefix

for suite_label, suite_prop in tqdm(SUITE_LABELS.items()):
    top_label = f"{GLM_SUITE_ID}_{suite_label}"
    planet = suite_prop["planet"]
    const = init_const(planet, directory=mypaths.constdir)
    procdir = mypaths.sadir / top_label
    for opt_label in tqdm(OPT_LABELS.keys(), leave=False):
        if opt_label not in ["base"]:
            continue
        sim_label = f"{suite_label}_{opt_label}"
        cl = load_data(
            files=procdir / f"{top_label}_{opt_label}_{time_prof}.nc",
        )
        add_planet_conf_to_cubes(cl, const)
        # Derive additional fields
        calc_derived_cubes(cl, const=const, model=um)
        # Use the cube list to initialise an AtmoSim object
        cl_p = interp_cubelist_from_height_to_pressure_levels(
            cl.extract(
                [
                    um.u,
                    um.v,
                    um.w,
                    um.dens,
                    um.temp,
                    um.ghgt,
                    um.sh,
                    um.pres,
                ]
            ),
            levels=P_LEVELS,
        )
        gl_attrs = {
            "name": sim_label,
            "planet": planet,
            "timestep": cl[0].attributes["timestep"],
            "processed": "True",
        }
        fname = procdir / f"{top_label}_{opt_label}_{time_prof}_plev.nc"
        save_cubelist(cl_p, fname, **gl_attrs)
