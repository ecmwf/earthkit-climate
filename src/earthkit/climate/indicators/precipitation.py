# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Precipitation-based climate indices."""

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def daily_precipitation_intensity(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Compute the Daily Precipitation Intensity (SDII) using the xclim indices module.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Daily precipitation flux.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indices.daily_pr_intensity`.

    Returns
    -------
    conversions.EarthkitData
        The computed Daily Precipitation Intensity as an Earthkit-compatible field.
    """
    # Create wrapper inside the function
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_pr_intensity)
    return wrapper(ds, **kwargs)


def maximum_consecutive_wet_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Compute the Maximum Consecutive Wet Days (CWD) using the xclim indices module.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Daily precipitation flux.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indices.maximum_consecutive_wet_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed Maximum Consecutive Wet Days as an Earthkit-compatible field.
    """
    # Create wrapper inside the function
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.maximum_consecutive_wet_days)
    return wrapper(ds, **kwargs)
