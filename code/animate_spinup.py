#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Make animations."""
import argparse
import warnings
from pathlib import Path
from time import time

import matplotlib as mpl
import matplotlib.animation
import matplotlib.pyplot as plt
import numpy as np
from cmcrameri import cm
from matplotlib.offsetbox import AnchoredText
from tqdm.notebook import tqdm

# My packages and local scripts
import mypaths
from aeolus.calc import precip_sum, water_path  # integrate,; vertical_mean,
from aeolus.const import add_planet_conf_to_cubes, init_const
from aeolus.coord import get_cube_rel_days, isel
from aeolus.core import AtmoSim
from aeolus.io import load_data
from aeolus.model import um  # , um_stash
from aeolus.plot import subplot_label_generator  # tex2cf_units
from aeolus.subset import DimConstr  # , l_range_constr
from commons import GLM_SUITE_ID, SIM_LABELS  # free_troposphere,; troposphere,
from pouch.clim_diag import calc_derived_cubes
from pouch.log import create_logger
from pouch.plot import (
    KW_AUX_TTL,  # KW_ZERO_LINE,; linspace_pm1,
    KW_MAIN_TTL,
    KW_SBPLT_LABEL,
    XLOCS,
    YLOCS,
    use_style,
)

# from math import prod


SCRIPT = Path(__file__).name

XY_VRBL = {
    "toa_alb": {
        "recipe": lambda cl: cl.extract_cube(um.toa_osr) / cl.extract_cube(um.toa_isr),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.tokyo,
            "levels": np.arange(0, 0.51, 0.05),
            # "extend": "max",
        },
        "title": "TOA albedo",
        "tex_units": "%",
    },
    "caf": {
        "recipe": lambda cl: cl.extract_cube(um.caf),
        "method": "contourf",
        "kw_plt": {"cmap": cm.davos, "levels": np.arange(0, 1.01, 0.05)},
        "title": "Cloud area fraction",
        "tex_units": "%",
    },
    "caf_vl": {
        "recipe": lambda cl: cl.extract_cube(um.caf_vl),
        "method": "contourf",
        "kw_plt": {"cmap": cm.davos, "levels": np.arange(0, 1.01, 0.05)},
        "title": "Very low cloud area fraction",
        "tex_units": "%",
    },
    "caf_l": {
        "recipe": lambda cl: cl.extract_cube(um.caf_l),
        "method": "contourf",
        "kw_plt": {"cmap": cm.davos, "levels": np.arange(0, 1.01, 0.05)},
        "title": "Low cloud area fraction",
        "tex_units": "%",
    },
    "caf_m": {
        "recipe": lambda cl: cl.extract_cube(um.caf_m),
        "method": "contourf",
        "kw_plt": {"cmap": cm.davos, "levels": np.arange(0, 1.01, 0.05)},
        "title": "Medium cloud area fraction",
        "tex_units": "%",
    },
    "caf_h": {
        "recipe": lambda cl: cl.extract_cube(um.caf_h),
        "method": "contourf",
        "kw_plt": {"cmap": cm.davos, "levels": np.arange(0, 1.01, 0.05)},
        "title": "High cloud area fraction",
        "tex_units": "%",
    },
    "wvp": {
        "recipe": lambda cl: water_path(cl, kind="water_vapour"),
        "method": "contourf",
        "kw_plt": {"cmap": cm.lapaz_r, "levels": np.arange(0, 201, 10)},
        "title": "Water vapour path",
        "tex_units": "$kg$ $m^{-2}$",
    },
    "iwp": {
        "recipe": lambda cl: water_path(cl, kind="ice_water"),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.devon_r,
            "levels": np.logspace(-6, 0, 7),
            "norm": mpl.colors.LogNorm(),
        },
        "title": "Ice water path",
        "tex_units": "$kg$ $m^{-2}$",
    },
    "lwp": {
        "recipe": lambda cl: water_path(cl, kind="liquid_water"),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.devon_r,
            "levels": np.logspace(-5, 1, 7),
            "norm": mpl.colors.LogNorm(),
        },
        "title": "Liquid water path",
        "tex_units": "$kg$ $m^{-2}$",
    },
    "cwp": {
        "recipe": lambda cl: water_path(cl, kind="cloud_water"),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.devon_r,
            "levels": np.logspace(-5, 1, 7),
            "norm": mpl.colors.LogNorm(),
        },
        "title": "Cloud water path",
        "tex_units": "$kg$ $m^{-2}$",
    },
    "sfc_shf": {
        "recipe": lambda cl: cl.extract_cube(um.sfc_shf),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.bilbao,
            "levels": np.arange(-50, 101, 25),
        },
        "title": "Sensible heat flux",
        "tex_units": "$W$ $m^{-2}$",
    },
    "sfc_lhf": {
        "recipe": lambda cl: cl.extract_cube(um.sfc_lhf),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.acton_r,
            "levels": np.arange(-25, 301, 25),
        },
        "title": "Latent heat flux",
        "tex_units": "$W$ $m^{-2}$",
    },
    "precip_sum": {
        "recipe": lambda cl: precip_sum(cl),
        "method": "contourf",
        "kw_plt": {
            "cmap": cm.acton_r,
            "levels": sorted([*np.logspace(-1, 3, 5)] + [*np.logspace(-1, 3, 5) / 2]),
            "norm": mpl.colors.LogNorm(),
        },
        "title": "Precipitation",
        "tex_units": "$mm$ $day^{-1}$",
    },
}


def parse_args(args=None):
    """Argument parser."""
    ap = argparse.ArgumentParser(
        SCRIPT,
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f"""Usage:
./{SCRIPT} varname1, varname2
""",
    )
    ap.add_argument(
        "--names",
        required=True,
        nargs="+",
        help="Variable names",
        choices=[*XY_VRBL.keys()],
    )
    ap.add_argument(
        "-f",
        "--frames",
        type=int,
        default=100,
        help="Number of frames",
    )
    ap.add_argument(
        "--one_frame",
        type=int,
        default=None,
        help="If not zero, show that frame only",
    )
    ap.add_argument(
        "--add_min_max",
        action="store_true",
        default=False,
        help="Add min/max values to the plot",
    )
    return ap.parse_args(args)


def main(args=None):
    """Main entry point."""

    def _make_frame(it):
        iletters = subplot_label_generator()
        for key, ax in axd.items():
            ax.clear()
            if not key.endswith("-cax"):
                ax.set_title(f"{next(iletters)}", **KW_SBPLT_LABEL)
                ax.set_ylim(-90, 90)
                ax.set_yticks(YLOCS)
                ax.set_yticklabels(YLOCS, fontsize="xx-small")
                ax.set_xlim(-180, 180)
                ax.set_xticks(XLOCS)
                ax.set_xticklabels(XLOCS, fontsize="xx-small")
                ax.grid()
        for (sim_label, sim_prop) in SIM_LABELS.items():
            the_run = runs[sim_label]
            days = get_cube_rel_days(the_run._cubes.extract(DimConstr().relax.t)[0])
            lons, lats = the_run.coord.x.points, the_run.coord.y.points
            cubes = isel(the_run._cubes, um.t, it)
            for vrbl_key in vrbls_to_show:
                vrbl_prop = XY_VRBL[vrbl_key]
                ax = axd[f"{vrbl_key}-{sim_label}"]
                cax = axd[f"{vrbl_key}-{sim_label}-cax"]
                # ax.set_ylabel("Latitude [$\degree$]", fontsize="xx-small")
                # ax.set_xlabel("Longitude [$\degree$]", fontsize="xx-small")
                if ax.get_subplotspec().is_first_row():
                    ax.set_title(sim_prop["title"], **KW_MAIN_TTL)
                ax.set_title(
                    f'{vrbl_prop["title"]} [{vrbl_prop["tex_units"]}]', **KW_AUX_TTL
                )
                cube = vrbl_prop["recipe"](cubes)
                _p0 = getattr(ax, vrbl_prop["method"])(
                    lons, lats, cube.data, **vrbl_prop["kw_plt"]
                )
                fig.colorbar(_p0, cax=cax, pad=0.02)
                if add_min_max:
                    cube_min = cube.data.min()
                    cube_max = cube.data.max()
                    at = AnchoredText(
                        f"Min: {cube_min:>3.1e}\nMax: {cube_max:>3.1e}",
                        prop=dict(color="k", size="x-small"),
                        frameon=False,
                        loc="lower right",
                    )
                    at.patch.set_facecolor(mpl.colors.to_rgba(bg_color, alpha=0.75))
                    ax.add_artist(at)
        for ax in axd.values():
            if (
                ax.get_subplotspec().is_last_col()
                and ax.get_subplotspec().is_first_row()
            ):
                ax.set_title(f"Day:{int(days[it])+1:>4d}\n", loc="right")

    t0 = time()
    L = create_logger(Path(__file__))
    # Parse command-line arguments
    args = parse_args(args)
    # Use custom mplstyle
    use_style()
    bg_color = mpl.colors.to_rgb(plt.rcParams["figure.facecolor"])
    # fg_color = mpl.colors.to_rgb(plt.rcParams["text.color"])

    # Variables
    vrbls_to_show = args.names
    add_min_max = args.add_min_max

    # Common directories
    img_prefix = f"{GLM_SUITE_ID}_spinup"
    inp_dir = mypaths.sadir / f"{GLM_SUITE_ID}_spinup"
    time_prof = "mean_days0_499"
    plotdir = mypaths.plotdir / img_prefix
    vidname = f"{img_prefix}__{'_'.join(SIM_LABELS)}__{'_'.join(vrbls_to_show)}"
    frames = args.frames
    vidname = plotdir / f"{vidname}_0-{frames:03d}d.mp4"

    # Load processed data
    runs = {}
    for sim_label, sim_prop in tqdm(SIM_LABELS.items()):
        planet = sim_prop["planet"]
        const = init_const(planet, directory=mypaths.constdir)
        L.info(
            f"Loading data from {inp_dir / f'{GLM_SUITE_ID}_{sim_label}_{time_prof}.nc'}"
        )
        cl = load_data(
            files=inp_dir / f"{GLM_SUITE_ID}_{sim_label}_{time_prof}.nc",
        )
        add_planet_conf_to_cubes(cl, const)
        # Derive additional fields
        calc_derived_cubes(cl, const=const, model=um)
        # Use the cube list to initialise an AtmoSim object
        runs[sim_label] = AtmoSim(
            cl,
            name=sim_label,
            planet=planet,
            const_dir=mypaths.constdir,
            timestep=cl[0].attributes["timestep"],
            model=um,
            vert_coord="z",
        )

    # Make the figure
    ncols = len(SIM_LABELS)
    nrows = len(vrbls_to_show)
    mosaic = [
        [
            i
            for j in [
                [f"{vrbl_key}-{sim_label}", f"{vrbl_key}-{sim_label}-cax"]
                for sim_label in SIM_LABELS
            ]
            for i in j
        ]
        for vrbl_key in vrbls_to_show
    ]
    fig = plt.figure(constrained_layout=True, figsize=(ncols * 8, nrows * 3))
    axd = fig.subplot_mosaic(
        mosaic,
        gridspec_kw={
            # set the width ratios between the columns
            "width_ratios": [30, 1]
            * ncols
        },
    )

    if args.one_frame is not None:
        L.info(f"Showing frame {args.one_frame}")
        _make_frame(args.one_frame)
        plt.show()
    else:
        L.info(f"Making {vidname.stem}")
        _make_frame(0)
        anim = mpl.animation.FuncAnimation(
            fig, _make_frame, frames=frames, interval=100, blit=False
        )
        anim.save(vidname)
        plt.close()
        L.success(f"Saved to {vidname}")
    L.info(f"Execution time: {time() - t0:.1f}s")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")  # noqa
    main()
