# -*- coding: utf-8 -*-
"""Calculations of zonal momentum budget."""
from datetime import timedelta
from cached_property import cached_property
import iris
from iris.analysis.maths import apply_ufunc
import numpy as np

from aeolus.calc import deriv, spatial_mean, time_mean, zonal_mean
from aeolus.coord import coord_to_cube, isel
from aeolus.core import AtmoSim
from aeolus.meta import update_metadata
from aeolus.plot import tex2cf_units

from pouch.clim_diag import d_dphi

__all__ = ("AngularMomentumBudget",)


class AngularMomentumBudget(AtmoSim):
    """
    Zonal mean angular momentum budget in spherical coordinates.

    See Sec. 2.2.7 in Vallis (2017).
    """

    term_labels = [
        "mean_horiz",
        "mean_vert",
        "stat_horiz",
        "stat_vert",
        "trans_horiz",
        "trans_vert",
    ]
    term_group_labels = ["mean", "stat", "trans"]
    tex_units = r"$J$ $m^{-3}$"
    _units = tex2cf_units(tex_units)

    @cached_property
    def sigma_p_tsm(self):  # TODO: move to AtmoSim
        return spatial_mean(time_mean(self.sigma_p))

    @cached_property
    def u_tzm(self):  # TODO: move to AtmoSim
        return zonal_mean(time_mean(self.u))

    @cached_property
    def datetimes(self):
        return self.coord.t.units.num2date(self.coord.t.points)

    @cached_property
    @update_metadata(name="axial_angular_momentum", units="m2 s-1")
    def ang_mom(self):
        """Calculate axial component of specific absolute angular momentum."""
        # Radius of the planet
        r = self.const.radius
        # Rotation rate
        omega = self.const.planet_rotation_rate
        r_coslat = r * self.lat_cos
        # inner_sum = add(the_run.u, omega * r_coslat, dim=lat_dim)
        # return multiply(inner_sum, r_coslat, dim=lat_dim)
        inner_sum = self.u + omega * r_coslat
        return inner_sum * r_coslat

    @cached_property
    @update_metadata(name="planet_radius", units="m")
    def radius(self):
        return (
            coord_to_cube(
                self._cubes.extract(self.dim_constr.relax.z)[0],
                self.model.z,
                broadcast=False,
            )
            + self.const.radius
        )

    @cached_property
    @update_metadata(name="cos(lat)", units="1")
    def lat_cos(self):
        lat_cube = coord_to_cube(
            self._cubes.extract(self.dim_constr.relax.y)[0],
            self.model.y,
            broadcast=False,
        )
        lat_cos_cube = apply_ufunc(np.cos, apply_ufunc(np.deg2rad, lat_cube))
        return lat_cos_cube

    @cached_property
    @update_metadata(name="sin(lat)", units="1")
    def lat_sin(self):
        lat_cube = coord_to_cube(
            self._cubes.extract(self.dim_constr.relax.y)[0],
            self.model.y,
            broadcast=False,
        )
        lat_sin_cube = apply_ufunc(np.sin, apply_ufunc(np.deg2rad, lat_cube))
        return lat_sin_cube

    @cached_property
    @update_metadata(name="coriolis_parameter", units="s-1")
    def coriolis(self):
        return 2 * self.const.planet_rotation_rate * self.lat_sin

    @cached_property
    @update_metadata(name="cos(lat)**2", units="1")
    def lat_cos_sq(self):
        return self.lat_cos ** 2

    @cached_property
    def rho_u(self):
        return self.dens * self.u

    @cached_property
    def rho_v(self):
        return self.dens * self.v

    @cached_property
    def rho_w(self):
        return self.dens * self.w

    @cached_property
    def ang_mom_tzm(self):
        return time_mean(zonal_mean(self.ang_mom))

    @cached_property
    def rho_u_tzm(self):  # TODO: move to AtmoSim
        return zonal_mean(time_mean(self.rho_u))

    @cached_property
    def rho_v_tzm(self):
        return time_mean(zonal_mean(self.rho_v))

    @cached_property
    def rho_w_tzm(self):
        return time_mean(zonal_mean(self.rho_w))

    @cached_property
    def cov_mean_horiz(self):
        """Covariance of the horizontal mean components."""
        return self.rho_v_tzm * self.ang_mom_tzm

    @cached_property
    def cov_mean_vert(self):
        """Covariance of the vertical mean components."""
        return self.rho_w_tzm * self.ang_mom_tzm

    @cached_property
    def rho_ang_mom_zm(self):
        return zonal_mean(self.dens * self.ang_mom)

    @cached_property
    def ang_mom_zm(self):
        return zonal_mean(self.ang_mom)

    @cached_property
    def rho_v_zm(self):
        return zonal_mean(self.rho_v)

    @cached_property
    def rho_w_zm(self):
        return zonal_mean(self.rho_w)

    @cached_property
    def rho_v_tm_zdev(self):
        return time_mean(self.rho_v - self.rho_v_zm)

    @cached_property
    def rho_w_tm_zdev(self):
        return time_mean(self.rho_w - self.rho_w_zm)

    @cached_property
    def ang_mom_tm_zdev(self):
        return time_mean(self.ang_mom - self.ang_mom_zm)

    @cached_property
    def cov_stat_horiz(self):
        """Zonal mean covariance of the horizontal stationary components."""
        return zonal_mean(self.rho_v_tm_zdev * self.ang_mom_tm_zdev)

    @cached_property
    def cov_stat_vert(self):
        """Zonal mean covariance of the vertical stationary components."""
        return zonal_mean(self.rho_w_tm_zdev * self.ang_mom_tm_zdev)

    @cached_property
    def ang_mom_tm(self):
        return time_mean(self.ang_mom)

    @cached_property
    def rho_v_tm(self):
        return time_mean(self.rho_v)

    @cached_property
    def rho_w_tm(self):
        return time_mean(self.rho_w)

    @cached_property
    def ang_mom_tdev(self):
        return self.ang_mom - self.ang_mom_tm

    @cached_property
    def rho_v_tdev(self):
        return self.rho_v - self.rho_v_tm

    @cached_property
    def rho_w_tdev(self):
        return self.rho_w - self.rho_w_tm

    @cached_property
    def cov_trans_horiz(self):
        """Time and zonal mean covariance of the horizontal stationary components."""
        return time_mean(zonal_mean(self.rho_v_tdev * self.ang_mom_tdev))

    @cached_property
    def cov_trans_vert(self):
        """Time and zonal mean covariance of the vertical stationary components."""
        return time_mean(zonal_mean(self.rho_w_tdev * self.ang_mom_tdev))

    @cached_property
    @update_metadata(
        units=_units,
        name="stat_horiz",
        attrs={
            "title": "Stationary horizontal",
            "tex": (
                r"-\frac{1}{r \cos \vartheta} \frac{\partial}{\partial \vartheta}"
                r"\left(\left[\bar{V}^{*} \bar{m}^{*}\right] \cos \vartheta\right)"
            ),
            "color": "tab:blue",
        },
    )
    def stat_horiz(self):
        numerator = -1 * d_dphi(self.cov_stat_horiz * self.lat_cos)
        denominator = self.lat_cos
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="stat_vert",
        attrs={
            "title": "Stationary vertical",
            "tex": (
                r"-\frac{1}{r^{2}} \frac{\partial}{\partial r}"
                r"\left(\left[\bar{W}^{*} \bar{m}^{*}\right] r^{2}\right)"
            ),
            "color": "tab:cyan",
        },
    )
    def stat_vert(self):
        numerator = -1 * deriv(self.cov_stat_vert * self.radius ** 2, self.model.z)
        denominator = self.radius ** 2
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="trans_horiz",
        attrs={
            "title": "Transient horizontal",
            "tex": (
                r"-\frac{1}{r \cos \vartheta} \frac{\partial}{\partial \vartheta}"
                r"\left(\left[\overline{V\prime m\prime}\right] \cos \vartheta\right)"
            ),
            "color": "tab:purple",
        },
    )
    def trans_horiz(self):
        numerator = -1 * d_dphi(self.cov_trans_horiz * self.lat_cos)
        denominator = self.lat_cos
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="trans_vert",
        attrs={
            "title": "Transient vertical",
            "tex": (
                r"-\frac{1}{r^{2}} \frac{\partial}{\partial r}"
                r"\left(\left[\overline{W\prime m\prime}\right] r^{2}\right)"
            ),
            "color": "tab:pink",
        },
    )
    def trans_vert(self):
        numerator = -1 * deriv(self.cov_trans_vert * self.radius ** 2, self.model.z)
        denominator = self.radius ** 2
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_horiz",
        attrs={
            "title": "Mean horizontal",
            "tex": (
                r"\frac{1}{r \cos \vartheta} \frac{\partial}{\partial \vartheta}"
                r"([\bar{V}][\bar{m}] \cos \vartheta)"
            ),
            "color": "tab:brown",
        },
    )
    def mean_horiz(self):
        numerator = -1 * d_dphi(self.cov_mean_horiz * self.lat_cos)
        denominator = self.lat_cos
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_vert",
        attrs={
            "title": "Mean vertical",
            "tex": (
                r"\frac{1}{r^{2}} \frac{\partial}{\partial r}([\bar{W}][\bar{m}] r^{2})"
            ),
            "color": "tab:orange",
        },
    )
    def mean_vert(self):
        numerator = -1 * deriv(self.cov_mean_vert * self.radius ** 2, self.model.z)
        denominator = self.radius ** 2
        return numerator / denominator

    @cached_property
    @update_metadata(
        units=_units,
        name="mean",
        attrs={
            "title": "Mean",
            "color": "tab:orange",
        },
    )
    def mean(self):
        return self.mean_horiz + self.mean_vert

    @cached_property
    @update_metadata(
        units=_units,
        name="stat",
        attrs={
            "title": "Stationary",
            "color": "tab:blue",
        },
    )
    def stat(self):
        return self.stat_horiz + self.stat_vert

    @cached_property
    @update_metadata(
        units=_units,
        name="trans",
        attrs={
            "title": "Transient",
            "color": "tab:purple",
        },
    )
    def trans(self):
        return self.trans_horiz + self.trans_vert

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_adv_horiz",
        attrs={
            "title": "Mean horizontal (advection form)",
            "tex": r"-\frac{[\bar{V}]}{r} \frac{\partial[\bar{m}]}{\partial \vartheta}",
            "color": "tab:green",
        },
    )
    def mean_adv_horiz(self):
        return -1 * self.rho_v_tzm * d_dphi(self.ang_mom_tzm)

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_adv_vert",
        attrs={
            "title": "Mean vertical (advection form)",
            "tex": r"-[\bar{W}] \frac{\partial[\bar{m}]}{\partial r}",
            "color": "tab:olive",
        },
    )
    def mean_adv_vert(self):
        return -1 * self.rho_w_tzm * deriv(self.ang_mom_tzm, self.model.z)

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_adv",
        attrs={
            "title": "Mean advection",
            "color": "tab:green",
        },
    )
    def mean_adv(self):
        return self.mean_adv_horiz + self.mean_adv_vert

    @cached_property
    @update_metadata(
        units=_units,
        name="sum",
        attrs={
            "title": "Sum",
            "color": "tab:grey",
        },
    )
    def sum_all(self):
        return self.mean + self.stat + self.trans

    @cached_property
    @update_metadata(
        units=_units,
        name="total_change_in_mass_angular_momentum_with_time",
        attrs={
            "title": "Total change in mass angular momentum with time",
            "tex": r"\frac{\Delta[\rho m]}{\Delta T}",
            "color": "tab:grey",
        },
    )
    def rho_ang_mom_time_change(self):
        rho_ang_mom_start = isel(self.rho_ang_mom_zm, self.model.t, 0)
        rho_ang_mom_end = isel(self.rho_ang_mom_zm, self.model.t, -1)

        delta_t = (self.datetimes[-1] - self.datetimes[0]) / timedelta(seconds=1)
        delta_t_cube = iris.cube.Cube(data=delta_t, units="s")
        return (rho_ang_mom_end - rho_ang_mom_start) / delta_t_cube
