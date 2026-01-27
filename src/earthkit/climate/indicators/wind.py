# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Wind indices."""

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def calm_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Calm days.

    Number of days with surface wind speed below threshold.

    **Units:** days

    This function wraps :func:`xclim.indicators.atmos.calm_days`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.calm_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.calm_days)
    return wrapper(ds, **kwargs)

def sfcWind_max(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum near-surface mean wind speed.

    Maximum of daily mean near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWind_max`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWind_max`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWind_max)
    return wrapper(ds, **kwargs)

def sfcWind_mean(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean near-surface wind speed.

    Mean of daily near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWind_mean`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWind_mean`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWind_mean)
    return wrapper(ds, **kwargs)

def sfcWind_min(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Minimum near-surface mean wind speed.

    Minimum of daily mean near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWind_min`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWind_min`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWind_min)
    return wrapper(ds, **kwargs)

def sfcWindmax_max(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum near-surface maximum wind speed.

    Maximum of daily maximum near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWindmax_max`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWindmax_max`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWindmax_max)
    return wrapper(ds, **kwargs)

def sfcWindmax_mean(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean near-surface maximum wind speed.

    Mean of daily maximum near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWindmax_mean`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWindmax_mean`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWindmax_mean)
    return wrapper(ds, **kwargs)

def sfcWindmax_min(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Minimum near-surface maximum wind speed.

    Minimum of daily maximum near-surface wind speed.

    **Units:** m s-1

    This function wraps :func:`xclim.indicators.atmos.sfcWindmax_min`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.sfcWindmax_min`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.sfcWindmax_min)
    return wrapper(ds, **kwargs)

def windy_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Windy days.

    Number of days with surface wind speed at or above threshold.

    **Units:** days

    This function wraps :func:`xclim.indicators.atmos.windy_days`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.windy_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.windy_days)
    return wrapper(ds, **kwargs)

