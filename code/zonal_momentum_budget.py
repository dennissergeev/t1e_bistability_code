# -*- coding: utf-8 -*-
"""Calculations of zonal momentum budget."""
from cached_property import cached_property
import iris
from iris.analysis.maths import apply_ufunc, divide
import numpy as np

from aeolus.calc import deriv, zonal_mean
from aeolus.coord import coord_to_cube
from aeolus.core import AtmoSim
from aeolus.meta import update_metadata
from aeolus.plot import tex2cf_units

from pouch.clim_diag import d_dphi

__all__ = ("ZonalMomBudgetFluxForm",)


class ZonalMomBudgetFluxForm(AtmoSim):
    """
    Class to calculate terms of the zonal momentum budget.

    Uses Eq. 3 from Mayne+ (2017), which is equivalent to Eq. 6 in Hardiman+ (2010),
    the general nonhydrostatic form.

    """

    term_labels = [
        "mean_horiz",
        "mean_vert",
        "eddy_horiz",
        "eddy_vert",
        "coriolis_horiz",
        "coriolis_vert",
    ]
    tex_units = "$kg$ $m^{-2}$ $s^{-2}$"
    _units = tex2cf_units(tex_units)

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
    @update_metadata(name="cos(lat)**2", units="1")
    def lat_cos_sq(self):
        return self.lat_cos ** 2

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
    @update_metadata(name="sin(lat)**2", units="1")
    def lat_sin_sq(self):
        return self.lat_sin ** 2

    @cached_property
    @update_metadata(units="m s-2")
    def mom_flx_div_eddy_stat(self):

        _lat_cos = self.lat_cos.copy()
        out = zonal_mean(self.u_prime * self.v_prime)
        out *= _lat_cos
        out = d_dphi(out, const=self.const, model=self.model)
        out.replace_coord(_lat_cos.coord(self.model.y).copy())
        out = -1 * out / _lat_cos
        out = out.interpolate(
            [(self.model.y, _lat_cos.coord(self.model.y).points)],
            iris.analysis.Linear(),
        )
        return out

    @cached_property
    def u_zm(self):
        return zonal_mean(self.u)

    @cached_property
    def u_prime(self):
        return self.u - self.u_zm

    @cached_property
    def v_zm(self):
        return zonal_mean(self.v)

    @cached_property
    def rho_zm(self):
        return zonal_mean(self.dens)

    @cached_property
    def v_prime(self):
        return self.v - self.v_zm

    @cached_property
    def w_zm(self):
        return zonal_mean(self.w)

    @cached_property
    def w_prime(self):
        return self.w - self.w_zm

    @cached_property
    def rho_v_zm(self):
        rho_v = self.dens * self.v
        return zonal_mean(rho_v)

    @cached_property
    def rho_w_zm(self):
        rho_w = self.dens * self.w
        return zonal_mean(rho_w)

    @cached_property
    def temp_zm(self):
        return zonal_mean(self.temp)

    @cached_property
    def temp_prime(self):
        return self.temp - self.temp_zm

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_horiz",
        attrs={
            "tex": r"-\frac{(\overline{\rho v}\bar{u}\cos^{2}\phi)_{,\phi}}{r\cos^{2}\phi}",
            "color": "tab:brown",
        },
    )
    def mean_horiz(self):
        deriv_arg = self.rho_v_zm * self.u_zm * self.lat_cos_sq
        numerator = -1 * d_dphi(deriv_arg)
        denominator = self.lat_cos_sq
        numerator.coord(self.model.y).points = denominator.coord(
            self.model.y
        ).points.copy()
        numerator.coord(self.model.y).bounds = denominator.coord(
            self.model.y
        ).bounds.copy()
        return divide(numerator, denominator)

    @cached_property
    @update_metadata(
        units=_units,
        name="mean_vert",
        attrs={
            "tex": r"-\frac{(\overline{\rho w}\bar{u}r^{3})_{,r}}{r^{3}}",
            "color": "tab:orange",
        },
    )
    def mean_vert(self):
        deriv_arg = self.rho_w_zm * self.u_zm * self.radius ** 3
        numerator = -1 * deriv(deriv_arg, self.model.z)
        numerator.coord(self.model.z).bounds = deriv_arg.coord(
            self.model.z
        ).bounds.copy()
        return divide(numerator, self.radius ** 3)

    @cached_property
    @update_metadata(
        units=_units,
        name="coriolis_horiz",
        attrs={
            "tex": r"2 \Omega \overline{\rho v} \sin \phi",
            "color": "tab:green",
        },
    )
    def coriolis_horiz(self):
        return 2 * self.const.planet_rotation_rate * self.rho_v_zm * self.lat_sin

    @cached_property
    @update_metadata(
        units=_units,
        name="coriolis_vert",
        attrs={
            "tex": r"-2 \Omega \overline{\rho w} \cos \phi",
            "color": "tab:olive",
        },
    )
    def coriolis_vert(self):
        return -2 * self.const.planet_rotation_rate * self.rho_w_zm * self.lat_cos

    @cached_property
    @update_metadata(
        units=_units,
        name="eddy_horiz",
        attrs={
            "tex": (
                r"-\frac{\left[\overline{(\rho v)^{\prime}u^{\prime}}"
                r"\cos^{2}\phi\right]_{,\phi}}{r\cos^{2}\phi}"
            ),
            "color": "tab:blue",
        },
    )
    def eddy_horiz(self):
        rho_v = self.dens * self.v
        rho_v_prime = rho_v - self.rho_v_zm
        deriv_arg = zonal_mean(rho_v_prime * self.u_prime) * self.lat_cos_sq
        numerator = -1 * d_dphi(deriv_arg)
        denominator = self.lat_cos_sq
        numerator.coord(self.model.y).points = denominator.coord(
            self.model.y
        ).points.copy()
        numerator.coord(self.model.y).bounds = denominator.coord(
            self.model.y
        ).bounds.copy()
        return divide(numerator, denominator)

    @cached_property
    @update_metadata(
        units=_units,
        name="eddy_vert",
        attrs={
            "tex": (
                r"-\frac{\left[\overline{(\rho w)^{\prime} u^{\prime}}"
                r"r^{3}\right]_{, r}}{r^{3}}"
            ),
            "color": "tab:cyan",
        },
    )
    def eddy_vert(self):
        rho_w = self.dens * self.w
        rho_w_prime = rho_w - self.rho_w_zm
        deriv_arg = zonal_mean(rho_w_prime * self.u_prime) * (self.radius ** 3)
        numerator = -1 * deriv(deriv_arg, self.model.z)
        numerator.coord(self.model.z).bounds = deriv_arg.coord(
            self.model.z
        ).bounds.copy()
        return divide(numerator, self.radius ** 3)
