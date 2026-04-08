# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Synoptic indices."""

from typing import Any

import xarray
import xclim.indicators.atmos
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.atmos.jetstream_metric_woollings)
def jetstream_metric_woollings(
    ua: xarray.DataArray | str = "ua",
    ds: xarray.Dataset | Any = None,
    **kwargs: Any,
) -> Any:
    """
    Strength and latitude of jetstream.

    Identify latitude and strength of maximum smoothed zonal wind speed in the region from
    15 to 75°N and -60 to 0°E, using the formula outlined in
    :cite:p:`woollings_variability_2010`. Wind is smoothened using a Lanczos filter
    approach.

    **Units:**

    - jetlat: degrees_north
    - jetstr: m s-1

    This function wraps `xclim.indicators.atmos.jetstream_metric_woollings <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.jetstream_metric_woollings>`_.

    Parameters
    ----------
    ua : xarray.DataArray | str
        Eastward wind component (u) at between 750 and 950 hPa.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.jetstream_metric_woollings(ua=ua, ds=ds, **kwargs)
