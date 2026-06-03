# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Hydrology indices."""

from typing import Any

import xarray
import xclim.indicators.land
from earthkit.utils.decorators import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.land.base_flow_index)
def base_flow_index(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Base flow index.

    Minimum of the 7-day moving average flow divided by the mean flow.

    **Units:**

    - base_flow_index: dimensionless

    This function wraps `xclim.indicators.land.base_flow_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.base_flow_index>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Rate of river discharge.
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
    return xclim.indicators.land.base_flow_index(
        q=q,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.doy_qmax)
def doy_qmax(
    da: xarray.DataArray | str = "da",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Day of year of the maximum streamflow.

    Day of the year of the maximum streamflow over {indexer}.

    **Units:**

    - q{indexer}_doy_qmax: dimensionless

    This function wraps `xclim.indicators.land.doy_qmax <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.doy_qmax>`_.

    Parameters
    ----------
    da : xarray.DataArray | str
        Input data.
    freq : str
        Resampling frequency defining the periods as defined in
        :ref:`timeseries.resampling`.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.doy_qmax(
        da=da,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.doy_qmin)
def doy_qmin(
    da: xarray.DataArray | str = "da",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Day of year of the minimum streamflow.

    Day of the year of the minimum streamflow over {indexer}.

    **Units:**

    - q{indexer}_doy_qmin: dimensionless

    This function wraps `xclim.indicators.land.doy_qmin <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.doy_qmin>`_.

    Parameters
    ----------
    da : xarray.DataArray | str
        Input data.
    freq : str
        Resampling frequency defining the periods as defined in
        :ref:`timeseries.resampling`.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.doy_qmin(
        da=da,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.high_flow_frequency)
def high_flow_frequency(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    threshold_factor: int = 9,
    freq: str = "YS-OCT",
    **kwargs: Any,
) -> Any:
    """
    High flow frequency.

    Calculate the number of days in a given period with flows greater than a specified
    threshold, given as a multiple of the median flow. By default, the period is the water
    year starting on 1st October and ending on 30th September, as commonly defined in North
    America.

    **Units:**

    - q_high_flow_frequency: days

    This function wraps `xclim.indicators.land.high_flow_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.high_flow_frequency>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Daily streamflow data.
    threshold_factor : int
        Factor by which the median flow is multiplied to set the high flow threshold,
        default is 9.
    freq : str
        Resampling frequency, default is 'YS-OCT' for water year starting in October and
        ending in September.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.high_flow_frequency(
        q=q,
        threshold_factor=threshold_factor,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.low_flow_frequency)
def low_flow_frequency(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    threshold_factor: float = 0.2,
    freq: str = "YS-OCT",
    **kwargs: Any,
) -> Any:
    """
    Low flow frequency.

    Calculate the number of days in a given period with flows lower than a specified
    threshold, given by a fraction of the mean flow. By default, the period is the water
    year starting on 1st October and ending on 30th September, as commonly defined in North
    America.

    **Units:**

    - q_low_flow_frequency: days

    This function wraps `xclim.indicators.land.low_flow_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.low_flow_frequency>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Daily streamflow data.
    threshold_factor : float
        Factor by which the mean flow is multiplied to set the low flow threshold, default
        is 0.2.
    freq : str
        Resampling frequency, default is 'YS-OCT' for water year starting in October and
        ending in September.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.low_flow_frequency(
        q=q,
        threshold_factor=threshold_factor,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.rb_flashiness_index)
def rb_flashiness_index(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Richards-baker flashiness index.

    Measurement of flow oscillations relative to average flow, quantifying the frequency and
    speed of flow changes.

    **Units:**

    - rbi: dimensionless

    This function wraps `xclim.indicators.land.rb_flashiness_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.rb_flashiness_index>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Rate of river discharge.
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
    return xclim.indicators.land.rb_flashiness_index(
        q=q,
        freq=freq,
        ds=ds,
        **kwargs,
    )
