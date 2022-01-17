# -*- coding: utf-8 -*-
"""Definitions and objects commonly used between scripts."""
import iris

from aeolus.model import um
from aeolus.region import Region
from aeolus.subset import l_range_constr


SIM_LABELS = {
    "grcs_base": {"planet": "hab1", "title": "CTRL", "kw_plt": {"color": "C0"}},
    "grcs_sens-t280k": {"planet": "hab1", "title": "GR; $T_0=280K$", "kw_plt": {"color": "C1"}},
}


SUITE_LABELS = {
    "grcs": {
        "planet": "hab1",
        "title": "Conv: MassFlux",
        "kw_plt": {"color": "C0"},
    },
    "llcs": {
        "planet": "hab1",
        "title": "Conv: Adjust",
        "kw_plt": {"color": "C1"},
    },
}
OPT_LABELS = {
    "base": {
        "group": None,
        "title": "Control",
        "kw_plt": {"color": "C0", "linestyle": "-"},
    },
    "sens-noradcld": {
        "group": "rad",
        "title": "No CRE",
        "kw_plt": {"color": "C1", "linestyle": "-"},
    },
    "sens-fixedsst": {
        "group": "sst",
        "title": "Fixed $T_{s,global}$",
        "kw_plt": {"color": "C2", "linestyle": "-"},
    },
    "sens-fixedsst-day-night": {
        "group": "sst",
        "title": "Fixed $T_{s,night}$",
        "kw_plt": {"color": "C2", "linestyle": "-"},
    },
    "sens-hcapsea1e7": {
        "group": "hcapsea",
        "title": "Slab depth = 2.5m",
        "kw_plt": {"color": "C3", "linestyle": ":"},
    },
    "sens-hcapsea2e7": {
        "group": "hcapsea",
        "title": "Slab depth = 5m",
        "kw_plt": {"color": "C3", "linestyle": "--"},
    },
    "sens-hcapsea4e7": {
        "group": "hcapsea",
        "title": "Slab depth = 10m",
        "kw_plt": {"color": "C3", "linestyle": "-."},
    },
    "sens-t250k": {
        "group": "t",
        "title": "$T_0=250K$",
        "kw_plt": {"color": "C4", "marker": "."},
    },
    "sens-t260k": {
        "group": "t",
        "title": "$T_0=260K$",
        "kw_plt": {"color": "C4", "marker": "s"},
    },
    "sens-t270k": {
        "group": "t",
        "title": "$T_0=270K$",
        "kw_plt": {"color": "C4", "marker": "P"},
    },
    "sens-t280k": {
        "group": "t",
        "title": "$T_0=280K$",
        "kw_plt": {"color": "C4", "marker": "X"},
    },
    "sens-t290k": {
        "group": "t",
        "title": "$T_0=290K$",
        "kw_plt": {"color": "C4", "marker": "*"},
    },
}

# Selected variables
VAR_PACK_MAIN = {
    "single_level": [
        "m01s00i493",
        um.t_sfc,
        um.p_sfc,
        um.toa_isr,
        um.toa_olr,
        um.toa_olr_cs,
        um.toa_osr,
        um.toa_osr_cs,
        um.sfc_dn_lw,
        um.sfc_dn_lw_cs,
        um.sfc_dn_sw,
        um.sfc_dn_sw_cs,
        um.sfc_net_down_lw,
        um.sfc_net_down_sw,
        um.sfc_shf,
        um.sfc_lhf,
        um.caf,
        um.caf_h,
        um.caf_m,
        um.caf_l,
        um.caf_vl,
        um.ls_rain,
        um.ls_snow,
        um.cv_rain,
    ],
    "multi_level": [
        um.u,
        um.v,
        um.w,
        um.pres,
        um.thta,
        um.sh,
        um.lw_up,
        um.sw_up,
        um.lw_dn,
        um.sw_dn,
        um.lw_up_cs,
        um.sw_up_cs,
        um.lw_dn_cs,
        um.sw_dn_cs,
        um.temp,
        um.rh,
        um.cld_ice_mf,
        um.cld_liq_mf,
        um.rain_mf,
        um.cld_ice_v,
        um.cld_liq_v,
        um.cld_v,
    ],
}

# HORIZ_WINDS_NAMES = [um.u, um.v]
# HORIZ_WINDS_STASH = ["m01s30i001", "m01s30i002"]

# Common parameters
DT_FMT = "%Y%m%dT%H%MZ"

# Global simulation parameters
GLM_SUITE_ID = "ch111"
GLM_MODEL_TIMESTEP = 86400 / 72
GLM_RUNID = r"umglaa"  # file prefix
GLM_FILE_REGEX = GLM_RUNID + r".p[b,c,d,e]{1}[0]{6}(?P<timestamp>[0-9]{2,6})_00"
GLM_START_DAY = 0

SS_REGION = Region(-5, 5, -5, 5, "substellar_pm05")

# Tidally-locked setups
DAYSIDE = Region(-90, 90, -90, 90, "dayside")
NIGHTSIDE = Region(90, -90, -90, 90, "nightside")

# Various constraints
eq_lat = iris.Constraint(**{um.y: lambda x: x.point == 1})
mid_lat = iris.Constraint(latitude=lambda x: abs(x.point) == 51)
ss_lon = iris.Constraint(**{um.x: lambda x: x.point == 1.25})
as_lon = iris.Constraint(**{um.x: lambda x: x.point == 178.75})
tropics = iris.Constraint(**{um.y: lambda x: abs(x.point) <= 20})
midlatitudes = iris.Constraint(**{um.y: lambda x: 30 <= abs(x.point) <= 65})
extratropics = iris.Constraint(**{um.y: lambda x: abs(x.point) >= 30})
cold_traps = iris.Constraint(
    **{um.x: lambda y: -160 < y.point < -140, um.y: lambda y: 45 < abs(y.point) < 55}
)
troposphere = l_range_constr(0, 17)
free_troposphere = l_range_constr(3, 18)
upper_troposphere = l_range_constr(7, 13)
spinup = iris.Constraint(**{um.fcst_prd: lambda x: x.point <= 500 * 24})
