# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0


from earthkit.climate.indicators.xarray import (
    _icclim,
    _percentiles,
    _xclim_atmos,
    _xclim_land,
    _xclim_seaice,
)
from earthkit.climate.indicators.xarray._icclim import *  # noqa
from earthkit.climate.indicators.xarray._xclim_atmos import *  # noqa
from earthkit.climate.indicators.xarray._xclim_land import *  # noqa
from earthkit.climate.indicators.xarray._xclim_seaice import *  # noqa

# isort: split
# Percentile indicators with unified backend dispatch override base implementations:
from earthkit.climate.indicators.xarray._percentiles import *  # noqa

__all__ = sorted(
    list({
        name
        for mod in (_icclim, _xclim_atmos, _xclim_land, _xclim_seaice, _percentiles)
        for name in dir(mod)
        if not name.startswith("_")
        and name
        not in {
            "Any",
            "Callable",
            "FieldList",
            "Literal",
            "xr",
            "xclim",
            "format_handler",
            "wrap_indicator",
        }
    })
)
