# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0


from earthkit.climate.indicators._xarray import _xclim_atmos, _xclim_land, _xclim_seaice
from earthkit.climate.indicators._xarray._xclim_atmos import *  # noqa
from earthkit.climate.indicators._xarray._xclim_land import *  # noqa
from earthkit.climate.indicators._xarray._xclim_seaice import *  # noqa

__all__ = sorted(
    list({
        name
        for mod in (_xclim_atmos, _xclim_land, _xclim_seaice)
        for name in dir(mod)
        if not name.startswith("_") and name not in {"Any", "Literal", "xr", "xclim", "format_handler"}
    })
)
