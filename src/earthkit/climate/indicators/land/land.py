# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Land indices."""

from typing import Any

import xarray
import xclim.indicators.land
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.land.flow_index)
def flow_index(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    p: float = 0.95,
    **kwargs: Any,
) -> Any:
    """
    Flow index.

    Calculate the pth percentile of daily streamflow normalized by the median flow.

    **Units:**

    - q_flow_index: 1

    This function wraps `xclim.indicators.land.flow_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.flow_index>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Daily streamflow data.
    p : float
        Percentile for calculating the flow index, between 0 and 1. Default of 0.95 is for
        high flows.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.flow_index(
        q=q,
        p=p,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.standardized_groundwater_index)
def standardized_groundwater_index(
    gwl: xarray.DataArray | str = "gwl",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str | None = "MS",
    window: int = 1,
    dist: str | Any = "genextreme",
    method: str = "ML",
    fitkwargs: dict | None = None,
    cal_start: str | None = None,
    cal_end: str | None = None,
    params: Any | None = None,
    **kwargs: Any,
) -> Any:
    """
    Standardized groundwater index (sgi).

    Groundwater over a moving window, normalized such that SGI averages to 0 for the
    calibration data. The window unit `X` is the minimal time period defined by the
    resampling frequency.

    **Units:**

    - sgi: dimensionless

    This function wraps `xclim.indicators.land.standardized_groundwater_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.standardized_groundwater_index>`_.

    Parameters
    ----------
    gwl : xarray.DataArray | str
        Groundwater head level.
    freq : str | None
        Resampling frequency. A monthly or daily frequency is expected. Option `None`
        assumes that the desired resampling has already been applied input dataset and will
        skip the resampling step.
    window : int
        Averaging window length relative to the resampling frequency. For example, if
        `freq="MS"`, i.e. a monthly resampling, the window is an integer number of months.
    dist : str | Any
        Name of the univariate distribution, or a callable `rv_continuous` (see
        :py:mod:`scipy.stats`).
    method : str
        Name of the fitting method, such as `ML` (maximum likelihood), `APP` (approximate).
        The approximate method uses a deterministic function that does not involve any
        optimization. `PWM` should be used with a `lmoments3` distribution.
    fitkwargs : dict | None
        Kwargs passed to ``xclim.indices.stats.fit`` used to impose values of certain
        parameters (`floc`, `fscale`).
    cal_start : str | None
        Start date of the calibration period. A `DateStr` is expected, that is a `str` in
        format `"YYYY-MM-DD"`. Default option `None` means that the calibration period
        begins at the start of the input dataset.
    cal_end : str | None
        End date of the calibration period. A `DateStr` is expected, that is a `str` in
        format `"YYYY-MM-DD"`. Default option `None` means that the calibration period
        finishes at the end of the input dataset.
    params : Any | None
        Fit parameters. The `params` can be computed using
        ``xclim.indices.stats.standardized_index_fit_params`` in advance. The output can be
        given here as input, and it overrides other options.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.standardized_groundwater_index(
        gwl=gwl,
        freq=freq,
        window=window,
        dist=dist,
        method=method,
        fitkwargs=fitkwargs,
        cal_start=cal_start,
        cal_end=cal_end,
        params=params,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.standardized_streamflow_index)
def standardized_streamflow_index(
    q: xarray.DataArray | str = "q",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str | None = "MS",
    window: int = 1,
    dist: str | Any = "genextreme",
    method: str = "ML",
    fitkwargs: dict | None = None,
    cal_start: str | None = None,
    cal_end: str | None = None,
    params: Any | None = None,
    **kwargs: Any,
) -> Any:
    """
    Standardized streamflow index (ssi).

    Streamflow over a moving window, normalized such that SSI averages to 0 for the
    calibration data. The window unit `X` is the minimal time period defined by the
    resampling frequency.

    **Units:**

    - ssi: dimensionless

    This function wraps `xclim.indicators.land.standardized_streamflow_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.standardized_streamflow_index>`_.

    Parameters
    ----------
    q : xarray.DataArray | str
        Rate of river discharge.
    freq : str | None
        Resampling frequency. A monthly or daily frequency is expected. Option `None`
        assumes that the desired resampling has already been applied input dataset and will
        skip the resampling step.
    window : int
        Averaging window length relative to the resampling frequency. For example, if
        `freq="MS"`, i.e. a monthly resampling, the window is an integer number of months.
    dist : str | Any
        Name of the univariate distribution, or a callable `rv_continuous` (see
        :py:mod:`scipy.stats`).
    method : str
        Name of the fitting method, such as `ML` (maximum likelihood), `APP` (approximate).
        The approximate method uses a deterministic function that does not involve any
        optimization. `PWM` should be used with a `lmoments3` distribution.
    fitkwargs : dict | None
        Kwargs passed to ``xclim.indices.stats.fit`` used to impose values of certain
        parameters (`floc`, `fscale`).
    cal_start : str | None
        Start date of the calibration period. A `DateStr` is expected, that is a `str` in
        format `"YYYY-MM-DD"`. Default option `None` means that the calibration period
        begins at the start of the input dataset.
    cal_end : str | None
        End date of the calibration period. A `DateStr` is expected, that is a `str` in
        format `"YYYY-MM-DD"`. Default option `None` means that the calibration period
        finishes at the end of the input dataset.
    params : Any | None
        Fit parameters. The `params` can be computed using
        ``xclim.indices.stats.standardized_index_fit_params`` in advance. The output can be
        given here as input, and it overrides other options.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.standardized_streamflow_index(
        q=q,
        freq=freq,
        window=window,
        dist=dist,
        method=method,
        fitkwargs=fitkwargs,
        cal_start=cal_start,
        cal_end=cal_end,
        params=params,
        ds=ds,
        **kwargs,
    )
