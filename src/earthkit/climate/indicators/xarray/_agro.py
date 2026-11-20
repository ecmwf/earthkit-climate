# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import numpy as np
import xarray as xr
from earthkit.data import FieldList

from earthkit.climate.indicators.xarray.agro.engine.cdi import cdi
from earthkit.climate.indicators.xarray.agro.engine.cei import cei
from earthkit.climate.indicators.xarray.agro.engine.seasons import build_seasons_map
from earthkit.climate.utils.decorators import wrap_indicator


def _resolve_data_array(
    val: xr.DataArray | FieldList | str,
    ds: xr.Dataset | None,
    default_name: str,
) -> xr.DataArray:
    """
    Resolve a DataArray from an input object, Dataset, or variable name.

    Parameters
    ----------
    val : xarray.DataArray | earthkit.data.FieldList | str
        Input DataArray, FieldList, or variable name string.
    ds : xarray.Dataset | None
        Input dataset containing meteorological variables.
    default_name : str
        Default variable name to check within ds.

    Returns
    -------
    xarray.DataArray
        Resolved DataArray object.
    """
    if isinstance(val, xr.DataArray):
        return val
    if ds is not None:
        if isinstance(val, str):
            if val in ds:
                return ds[val]
            if val != default_name:
                raise ValueError(f"Variable {val!r} not found in ds. Available variables: {list(ds.data_vars)}.")
        if default_name in ds:
            return ds[default_name]
    raise ValueError(
        f"Unable to resolve variable {default_name!r}. "
        f"Please pass a DataArray or a Dataset containing {default_name!r}."
    )


@wrap_indicator()
def chilling_hours(
    tas: xr.DataArray | FieldList | str = "tas",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "10-01",
    season_end: str = "03-31",
    lower: float = 0.0,
    upper: float = 7.2,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate Chilling Hours for deciduous fruit trees using the 0 to 7.2 degC model.

    Accumulates qualifying time steps within the winter dormant season [lower, upper]
    (default 0 to 7.2 degC) according to Begueria et al. (2026).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Air temperature data.
    ds : xarray.Dataset | None, default=None
        Input dataset containing temperature data.
    season_start : str, default="10-01"
        First day of dormancy season in 'mm-dd' format.
    season_end : str, default="03-31"
        Last day of dormancy season in 'mm-dd' format.
    lower : float, default=0.0
        Lower temperature threshold in degC.
    upper : float, default=7.2
        Upper temperature threshold in degC.
    return_dataset : bool, default=False
        If True, returns the full CEI Dataset (cond, valid, excess, cum_excess).
    **kwargs : Any
        Additional keyword arguments forwarded to the CEI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative chilling hours (or full dataset if return_dataset=True).
    """
    da = _resolve_data_array(tas, ds, "tas")
    result = cei(
        da,
        season_start=season_start,
        season_end=season_end,
        lower=lower,
        upper=upper,
        direction="above",
        unit_contribution=True,
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_excess"]
    out.attrs["long_name"] = "Chilling Hours (0 to 7.2 degC model)"
    out.attrs["units"] = "h"
    return out


@wrap_indicator()
def vernalisation_days(
    tas: xr.DataArray | FieldList | str = "tas",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "10-01",
    season_end: str = "03-31",
    lower: float = -1.0,
    upper: float = 7.0,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate Vernalisation Requirement days for winter crops.

    Counts days within the optimal vernalisation range (-1 to 7 degC)
    over the winter season according to Begueria et al. (2026).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Mean daily air temperature data.
    ds : xarray.Dataset | None, default=None
        Input dataset containing temperature data.
    season_start : str, default="10-01"
        First day of winter season in 'mm-dd' format.
    season_end : str, default="03-31"
        Last day of winter season in 'mm-dd' format.
    lower : float, default=-1.0
        Lower vernalisation temperature threshold in degC.
    upper : float, default=7.0
        Upper vernalisation temperature threshold in degC.
    return_dataset : bool, default=False
        If True, returns the full CEI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CEI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative vernalisation days.
    """
    da = _resolve_data_array(tas, ds, "tas")
    result = cei(
        da,
        season_start=season_start,
        season_end=season_end,
        lower=lower,
        upper=upper,
        direction="above",
        unit_contribution=True,
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_excess"]
    out.attrs["long_name"] = "Vernalisation Requirement Days"
    out.attrs["units"] = "d"
    return out


@wrap_indicator()
def pest_degree_days(
    tas: xr.DataArray | FieldList | str = "tas",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "04-01",
    season_end: str = "10-31",
    tbase: float = 10.0,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate Degree-Days for Pests (DDP) accumulated over a growing season.

    Accumulates temperature excess above a base threshold (default 10 degC)
    over the active season according to Begueria et al. (2026).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Daily mean air temperature data.
    ds : xarray.Dataset | None, default=None
        Input dataset containing temperature data.
    season_start : str, default="04-01"
        First day of growing season in 'mm-dd' format.
    season_end : str, default="10-31"
        Last day of growing season in 'mm-dd' format.
    tbase : float, default=10.0
        Base temperature threshold in degC.
    return_dataset : bool, default=False
        If True, returns the full CEI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CEI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative degree-days for pests.
    """
    da = _resolve_data_array(tas, ds, "tas")
    result = cei(
        da,
        season_start=season_start,
        season_end=season_end,
        lower=tbase,
        upper=np.inf,
        direction="above",
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_excess"]
    out.attrs["long_name"] = f"Degree-Days for Pests (Tbase = {tbase} degC)"
    out.attrs["units"] = "degC d"
    return out


@wrap_indicator()
def growing_degree_days_season(
    tas: xr.DataArray | FieldList | str = "tas",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "04-01",
    season_end: str = "10-31",
    tbase: float = 0.0,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate Growing Degree Days (GDD) accumulated within a defined crop season.

    Accumulates daily temperature excess above base temperature across custom
    crop seasonal windows with bias correction according to Begueria et al. (2026).

    Parameters
    ----------
    tas : xarray.DataArray | earthkit.data.FieldList | str, default="tas"
        Daily mean air temperature data.
    ds : xarray.Dataset | None, default=None
        Input dataset containing temperature data.
    season_start : str, default="04-01"
        First day of crop season in 'mm-dd' format.
    season_end : str, default="10-31"
        Last day of crop season in 'mm-dd' format.
    tbase : float, default=0.0
        Base temperature threshold in degC.
    return_dataset : bool, default=False
        If True, returns the full CEI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CEI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative growing degree days over the specified season.
    """
    da = _resolve_data_array(tas, ds, "tas")
    result = cei(
        da,
        season_start=season_start,
        season_end=season_end,
        lower=tbase,
        upper=np.inf,
        direction="above",
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_excess"]
    out.attrs["long_name"] = f"Growing Degree Days (Season {season_start} to {season_end}, Tbase = {tbase} degC)"
    out.attrs["units"] = "degC d"
    return out


@wrap_indicator()
def heat_stress_days(
    tasmax: xr.DataArray | FieldList | str = "tasmax",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "04-01",
    season_end: str = "10-31",
    thresh: float = 35.0,
    min_duration: int = 1,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate the number of heat-stress days for crops within a growing season.

    Counts days where maximum temperature equals or exceeds the critical stress
    threshold (default 35 degC) according to Begueria et al. (2026).

    Parameters
    ----------
    tasmax : xarray.DataArray | earthkit.data.FieldList | str, default="tasmax"
        Daily maximum air temperature.
    ds : xarray.Dataset | None, default=None
        Input dataset containing maximum temperature data.
    season_start : str, default="04-01"
        First day of growing season in 'mm-dd' format.
    season_end : str, default="10-31"
        Last day of growing season in 'mm-dd' format.
    thresh : float, default=35.0
        Critical heat-stress threshold in degC.
    min_duration : int, default=1
        Minimum duration of consecutive stress days to contribute.
    return_dataset : bool, default=False
        If True, returns the full CDI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CDI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative number of heat stress days.
    """
    da = _resolve_data_array(tasmax, ds, "tasmax")
    input_ds = xr.Dataset({"tasmax": da})
    bounds = [{"var": "tasmax", "lower": thresh, "upper": np.inf}]
    result = cdi(
        input_ds,
        bounds=bounds,
        season_start=season_start,
        season_end=season_end,
        min_duration=min_duration,
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_days"]
    out.attrs["long_name"] = f"Heat-Stress Days (Tmax >= {thresh} degC)"
    out.attrs["units"] = "d"
    return out


@wrap_indicator()
def heatwave_duration_season(
    tasmax: xr.DataArray | FieldList | str = "tasmax",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "04-01",
    season_end: str = "10-31",
    thresh: float = 35.0,
    min_duration: int = 3,
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate the cumulative days in heatwaves during the growing season.

    Counts days belonging to heatwaves lasting at least min_duration consecutive
    days (default 3 days with Tmax >= 35 degC) with bias correction according to
    Begueria et al. (2026).

    Parameters
    ----------
    tasmax : xarray.DataArray | earthkit.data.FieldList | str, default="tasmax"
        Daily maximum air temperature.
    ds : xarray.Dataset | None, default=None
        Input dataset containing maximum temperature data.
    season_start : str, default="04-01"
        First day of growing season in 'mm-dd' format.
    season_end : str, default="10-31"
        Last day of growing season in 'mm-dd' format.
    thresh : float, default=35.0
        Critical heatwave threshold in degC.
    min_duration : int, default=3
        Minimum heatwave duration in consecutive days.
    return_dataset : bool, default=False
        If True, returns the full CDI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CDI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative heatwave days in the season.
    """
    da = _resolve_data_array(tasmax, ds, "tasmax")
    input_ds = xr.Dataset({"tasmax": da})
    bounds = [{"var": "tasmax", "lower": thresh, "upper": np.inf}]
    result = cdi(
        input_ds,
        bounds=bounds,
        season_start=season_start,
        season_end=season_end,
        min_duration=min_duration,
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_days"]
    out.attrs["long_name"] = f"Heatwave Duration (Tmax >= {thresh} degC, min_duration >= {min_duration} d)"
    out.attrs["units"] = "d"
    return out


@wrap_indicator()
def cumulative_shortwave_radiation(
    rsds: xr.DataArray | FieldList | str = "rsds",
    ds: xr.Dataset | None = None,
    *,
    season_start: str = "04-01",
    season_end: str = "10-31",
    return_dataset: bool = False,
    **kwargs: Any,
) -> xr.DataArray | xr.Dataset | FieldList:
    """
    Calculate cumulative surface downwelling shortwave radiation over a season.

    Accumulates solar radiation during the active growing season according to
    Begueria et al. (2026).

    Parameters
    ----------
    rsds : xarray.DataArray | earthkit.data.FieldList | str, default="rsds"
        Surface solar radiation downwards data.
    ds : xarray.Dataset | None, default=None
        Input dataset containing radiation data.
    season_start : str, default="04-01"
        First day of growing season in 'mm-dd' format.
    season_end : str, default="10-31"
        Last day of growing season in 'mm-dd' format.
    return_dataset : bool, default=False
        If True, returns the full CEI Dataset.
    **kwargs : Any
        Additional keyword arguments forwarded to the CEI engine.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | earthkit.data.FieldList
        Cumulative shortwave radiation over the season.
    """
    da = _resolve_data_array(rsds, ds, "rsds")
    result = cei(
        da,
        season_start=season_start,
        season_end=season_end,
        lower=0.0,
        upper=np.inf,
        direction="above",
        **kwargs,
    )
    if return_dataset:
        return result
    out = result["cum_excess"]
    out.attrs["long_name"] = "Cumulative Shortwave Radiation"
    out.attrs["units"] = "W m-2 d"
    return out


__all__ = [
    "build_seasons_map",
    "cdi",
    "cei",
    "chilling_hours",
    "cumulative_shortwave_radiation",
    "growing_degree_days_season",
    "heat_stress_days",
    "heatwave_duration_season",
    "pest_degree_days",
    "vernalisation_days",
]
