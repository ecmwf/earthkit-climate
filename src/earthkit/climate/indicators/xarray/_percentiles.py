# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Literal

import xarray as xr
from earthkit.data import FieldList

from earthkit.climate.indicators.xarray import _icclim, _xclim_atmos
from earthkit.climate.utils.decorators import wrap_indicator


@wrap_indicator()
def tx90p(
    tasmax: xr.DataArray | FieldList | str = "tasmax",
    tasmax_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with maximum temperature above the 90th percentile (warm days).

    Computes TX90p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tasmax : xarray.DataArray | earthkit.data.FieldList | str, default="tasmax"
        Daily maximum air temperature.
    tasmax_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 90th percentile of daily maximum temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation (e.g. ['1961-01-01', '1990-12-31']) when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tasmax_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of warm days (TX > 90th percentile).
    """
    selected_backend = ("xclim" if tasmax_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tx90p(
            tasmax=tasmax,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tasmax_per is None:
            raise ValueError(
                "When using backend='xclim', 'tasmax_per' (precomputed percentile) must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tx90p(
            tasmax=tasmax,
            tasmax_per=tasmax_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")


@wrap_indicator()
def tx10p(
    tasmax: xr.DataArray | FieldList | str = "tasmax",
    tasmax_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with maximum temperature below the 10th percentile (cold day-times).

    Computes TX10p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tasmax : xarray.DataArray | earthkit.data.FieldList | str, default="tasmax"
        Daily maximum air temperature.
    tasmax_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 10th percentile of daily maximum temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tasmax_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of cold day-times (TX < 10th percentile).
    """
    selected_backend = ("xclim" if tasmax_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tx10p(
            tasmax=tasmax,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tasmax_per is None:
            raise ValueError(
                "When using backend='xclim', 'tasmax_per' must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tx10p(
            tasmax=tasmax,
            tasmax_per=tasmax_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")


@wrap_indicator()
def tn90p(
    tasmin: xr.DataArray | FieldList | str = "tasmin",
    tasmin_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with minimum temperature above the 90th percentile (warm nights).

    Computes TN90p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tasmin : xarray.DataArray | earthkit.data.FieldList | str, default="tasmin"
        Daily minimum air temperature.
    tasmin_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 90th percentile of daily minimum temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tasmin_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of warm nights (TN > 90th percentile).
    """
    selected_backend = ("xclim" if tasmin_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tn90p(
            tasmin=tasmin,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tasmin_per is None:
            raise ValueError(
                "When using backend='xclim', 'tasmin_per' must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tn90p(
            tasmin=tasmin,
            tasmin_per=tasmin_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")


@wrap_indicator()
def tn10p(
    tasmin: xr.DataArray | FieldList | str = "tasmin",
    tasmin_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with minimum temperature below the 10th percentile (cold nights).

    Computes TN10p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tasmin : xarray.DataArray | earthkit.data.FieldList | str, default="tasmin"
        Daily minimum air temperature.
    tasmin_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 10th percentile of daily minimum temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tasmin_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of cold nights (TN < 10th percentile).
    """
    selected_backend = ("xclim" if tasmin_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tn10p(
            tasmin=tasmin,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tasmin_per is None:
            raise ValueError(
                "When using backend='xclim', 'tasmin_per' must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tn10p(
            tasmin=tasmin,
            tasmin_per=tasmin_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")


@wrap_indicator()
def tg90p(
    tas: xr.DataArray | FieldList | str = "tas",
    tas_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with mean temperature above the 90th percentile.

    Computes TG90p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Daily mean air temperature.
    tas_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 90th percentile of daily mean temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tas_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of days with TG > 90th percentile.
    """
    selected_backend = ("xclim" if tas_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tg90p(
            tas=tas,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tas_per is None:
            raise ValueError(
                "When using backend='xclim', 'tas_per' must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tg90p(
            tas=tas,
            tas_per=tas_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")


@wrap_indicator()
def tg10p(
    tas: xr.DataArray | FieldList | str = "tas",
    tas_per: xr.DataArray | FieldList | str | None = None,
    ds: xr.Dataset | None = None,
    *,
    base_period_time_range: list[str] | tuple[str, str] | None = None,
    freq: str = "YS",
    backend: Literal["auto", "xclim", "icclim"] = "auto",
    **kwargs: Any,
) -> xr.DataArray | FieldList:
    """
    Days with mean temperature below the 10th percentile.

    Computes TG10p using either xclim (with a precalculated percentile)
    or icclim (with automatic in-base/out-of-base percentile and bootstrapping).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Daily mean air temperature.
    tas_per : xarray.DataArray | earthkit.data.FieldList | str | None, default=None
        Precalculated 10th percentile of daily mean temperature (required when backend='xclim').
    ds : xarray.Dataset | None, default=None
        Input dataset containing meteorological variables.
    base_period_time_range : list[str] | tuple[str, str] | None, default=None
        Reference period for percentile calculation when using icclim.
    freq : str, default="YS"
        Resampling frequency / aggregation period.
    backend : Literal["auto", "xclim", "icclim"], default="auto"
        Calculation backend. 'auto' selects 'xclim' if tas_per is provided, otherwise 'icclim'.
    **kwargs : Any
        Additional keyword arguments forwarded to the selected backend.

    Returns
    -------
    xarray.DataArray | earthkit.data.FieldList
        Number of days with TG < 10th percentile.
    """
    selected_backend = ("xclim" if tas_per is not None else "icclim") if backend == "auto" else backend

    if selected_backend == "icclim":
        return _icclim._tg10p(
            tas=tas,
            ds=ds,
            freq=freq,
            base_period_time_range=base_period_time_range,
            **kwargs,
        )
    if selected_backend == "xclim":
        if tas_per is None:
            raise ValueError(
                "When using backend='xclim', 'tas_per' must be provided. "
                "Alternatively, specify 'base_period_time_range' to compute using backend='icclim'."
            )
        return _xclim_atmos._tg10p(
            tas=tas,
            tas_per=tas_per,
            ds=ds,
            freq=freq,
            **kwargs,
        )
    raise ValueError(f"Unknown backend: {backend!r}. Expected 'auto', 'xclim', or 'icclim'.")
