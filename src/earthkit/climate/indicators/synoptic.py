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

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def jetstream_metric_woollings(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Strength and latitude of jetstream.

    Identify latitude and strength of maximum smoothed zonal wind speed in the region from
    15 to 75°N and -60 to 0°E, using the formula outlined in
    :cite:p:`woollings_variability_2010`. Wind is smoothened using a Lanczos filter
    approach.

    **Units:** ['degrees_north', 'm s-1']

    This function wraps :func:`xclim.indicators.atmos.jetstream_metric_woollings`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.jetstream_metric_woollings`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.jetstream_metric_woollings)
    return wrapper(ds, **kwargs)

