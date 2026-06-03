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
from earthkit.utils.decorators import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.atmos.calm_days)
def calm_days(
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "2 m s-1",
    freq: str = "MS",
    **kwargs: Any,
) -> Any:
    """
    Calm days.

    Number of days with surface wind speed below threshold.

    **Units:**

    - calm_days: days

    This function wraps `xclim.indicators.atmos.calm_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.calm_days>`_.

    Parameters
    ----------
    sfcWind : xarray.DataArray | str
        Daily windspeed.
    thresh : Any
        Threshold average near-surface wind speed on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.calm_days(
        sfcWind=sfcWind,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWind_max)
def sfcWind_max(
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum near-surface mean wind speed.

    Maximum of daily mean near-surface wind speed.

    **Units:**

    - sfcWind_max: m s-1

    This function wraps `xclim.indicators.atmos.sfcWind_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWind_max>`_.

    Parameters
    ----------
    sfcWind : xarray.DataArray | str
        Mean daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWind_max(
        sfcWind=sfcWind,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWind_mean)
def sfcWind_mean(
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean near-surface wind speed.

    Mean of daily near-surface wind speed.

    **Units:**

    - sfcWind_mean: m s-1

    This function wraps `xclim.indicators.atmos.sfcWind_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWind_mean>`_.

    Parameters
    ----------
    sfcWind : xarray.DataArray | str
        Mean daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWind_mean(
        sfcWind=sfcWind,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWind_min)
def sfcWind_min(
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Minimum near-surface mean wind speed.

    Minimum of daily mean near-surface wind speed.

    **Units:**

    - sfcWind_min: m s-1

    This function wraps `xclim.indicators.atmos.sfcWind_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWind_min>`_.

    Parameters
    ----------
    sfcWind : xarray.DataArray | str
        Mean daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWind_min(
        sfcWind=sfcWind,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWindmax_max)
def sfcWindmax_max(
    sfcWindmax: xarray.DataArray | str = "sfcWindmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum near-surface maximum wind speed.

    Maximum of daily maximum near-surface wind speed.

    **Units:**

    - sfcWindmax_max: m s-1

    This function wraps `xclim.indicators.atmos.sfcWindmax_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWindmax_max>`_.

    Parameters
    ----------
    sfcWindmax : xarray.DataArray | str
        Maximum daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWindmax_max(
        sfcWindmax=sfcWindmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWindmax_mean)
def sfcWindmax_mean(
    sfcWindmax: xarray.DataArray | str = "sfcWindmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean near-surface maximum wind speed.

    Mean of daily maximum near-surface wind speed.

    **Units:**

    - sfcWindmax_mean: m s-1

    This function wraps `xclim.indicators.atmos.sfcWindmax_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWindmax_mean>`_.

    Parameters
    ----------
    sfcWindmax : xarray.DataArray | str
        Maximum daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWindmax_mean(
        sfcWindmax=sfcWindmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.sfcWindmax_min)
def sfcWindmax_min(
    sfcWindmax: xarray.DataArray | str = "sfcWindmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Minimum near-surface maximum wind speed.

    Minimum of daily maximum near-surface wind speed.

    **Units:**

    - sfcWindmax_min: m s-1

    This function wraps `xclim.indicators.atmos.sfcWindmax_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.sfcWindmax_min>`_.

    Parameters
    ----------
    sfcWindmax : xarray.DataArray | str
        Maximum daily wind speed.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.sfcWindmax_min(
        sfcWindmax=sfcWindmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.windy_days)
def windy_days(
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "10.8 m s-1",
    freq: str = "MS",
    **kwargs: Any,
) -> Any:
    """
    Windy days.

    Number of days with surface wind speed at or above threshold.

    **Units:**

    - windy_days: days

    This function wraps `xclim.indicators.atmos.windy_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.windy_days>`_.

    Parameters
    ----------
    sfcWind : xarray.DataArray | str
        Daily average near-surface wind speed.
    thresh : Any
        Threshold average near-surface wind speed on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.windy_days(
        sfcWind=sfcWind,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )
