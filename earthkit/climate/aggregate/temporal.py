import typing as T
import logging
import numpy as np
import xarray as xr

from earthkit.climate.aggregate import tools, resample

# These are included here for legacy purposes, but the code is abstract so not part of temporal namespace
from earthkit.climate.aggregate import reduce as _reduce
from earthkit.climate.aggregate import reduce as _rolling_reduce

logger = logging.getLogger(__name__)


def reduce(*args, **kwargs):
    """
    Deprecated method location, please see `earthkit.climate.aggregate.reduce`
    """
    logger.warn(
        "`earthkit.climate.aggregate.temporal.reduce` is a deprecated location for this method, "
        "please use `earthkit.climate.aggregate.reduce` instead."
    )
    return _reduce(*args, **kwargs)


def rolling_reduce(*args, **kwargs):
    """
    Deprecated method location, please see `earthkit.climate.aggregate.rolling_reduce`
    """
    logger.warn(
        "`earthkit.climate.aggregate.temporal.rolling_reduce` is a deprecated location for this method, "
        "please use `earthkit.climate.aggregate.rolling_reduce` instead."
    )
    return _rolling_reduce(*args, **kwargs)

@tools.time_dim_decorator
def daily_mean(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the daily mean.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    time_dim : str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="D", dim=time_dim, how="mean", **kwargs)


@tools.time_dim_decorator
def daily_max(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the daily maximum.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    time_dim : str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="D", dim=time_dim, how="max", **kwargs)


@tools.time_dim_decorator
def daily_min(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the daily minimum.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a time dimension.
    time_dim : (optional) str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="D", dim=time_dim, how="min", **kwargs)


@tools.time_dim_decorator
def daily_std(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the daily standard deviation.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a time dimension.
    time_dim : (optional) str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="D", dim=time_dim, how="std", **kwargs)


@tools.time_dim_decorator
def daily_sum(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the daily sum (accumulation).

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a time dimension.
    time_dim : (optional) str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="D", dim=time_dim, how="sum", **kwargs)


@tools.time_dim_decorator
def monthly_mean(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the monthly mean.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    time_dim : str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="M", dim=time_dim, how="mean", **kwargs)


@tools.time_dim_decorator
def monthly_max(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the monthly max.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    time_dim : str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="M", dim=time_dim, how="max", **kwargs)


@tools.time_dim_decorator
def monthly_min(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    time_dim: T.Union[str, None] = None,
    **kwargs,
):
    """
    Calculate the monthly min.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    time_dim : str
        Name of the time dimension in the xarray object, default is `"time"`.
    time_shift : (optional) timedelta or dict
        A time shift to apply to the data prior to calculation, e.g. to change the local time zone.
        It can be provided as any object that can be understood by `pandas.Timedelta`, a dictonary is passed
        as kwargs to `pandas.Timedelta`
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(dataarray, frequency="M", dim=time_dim, how="min", **kwargs)

