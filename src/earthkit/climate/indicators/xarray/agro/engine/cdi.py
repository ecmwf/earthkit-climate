# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Literal

import numpy as np
import pandas as pd
import xarray as xr

from earthkit.climate.indicators.xarray.agro.engine.cei import (
    _is_subdaily,
    _resample_to_daily,
    _run_length_2d,
    _run_length_skip_nan_1d,
)
from earthkit.climate.indicators.xarray.agro.engine.seasons import build_seasons_map

_BOUNDS_DEFAULTS: dict[str, Any] = {
    "lower": -np.inf,
    "upper": np.inf,
    "inc_lower": True,
    "inc_upper": True,
}


def _normalise_bounds(
    bounds: pd.DataFrame | list[dict[str, Any]],
) -> pd.DataFrame:
    """
    Normalise the bounds argument to a tidy DataFrame.

    Parameters
    ----------
    bounds : pandas.DataFrame | list[dict[str, Any]]
        DataFrame with at least a 'var' column, or list of dicts.

    Returns
    -------
    pandas.DataFrame
        Normalised DataFrame with columns var, lower, upper, inc_lower, inc_upper.
    """
    bounds_df = pd.DataFrame(bounds) if isinstance(bounds, list) else bounds.copy()

    if "var" not in bounds_df.columns:
        raise ValueError("bounds must contain a 'var' column with variable names.")

    for col, default in _BOUNDS_DEFAULTS.items():
        if col not in bounds_df.columns:
            bounds_df[col] = default

    bounds_df = bounds_df.fillna(_BOUNDS_DEFAULTS)
    return bounds_df.reset_index(drop=True)


def _consecutive_true_2d(cond: np.ndarray) -> np.ndarray:
    """
    Count consecutive True elements along the last axis.

    Parameters
    ----------
    cond : numpy.ndarray
        Boolean array with time as the last axis.

    Returns
    -------
    numpy.ndarray
        Array containing 1-based consecutive True counts or 0 for False.
    """
    cum_true = np.cumsum(cond, axis=-1)
    false_cum = np.where(~cond, cum_true, 0)
    false_cum_propagated = np.maximum.accumulate(false_cum, axis=-1)
    return np.where(cond, cum_true - false_cum_propagated, 0)


def _cdi_numpy(
    *arrays: np.ndarray,
    season_ids: np.ndarray,
    bounds_lower: np.ndarray,
    bounds_upper: np.ndarray,
    bounds_inc_lower: np.ndarray,
    bounds_inc_upper: np.ndarray,
    combiner: str,
    k: int,
    min_duration: int,
    na_action: str,
    max_run: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Execute core CDI numerical calculation over a NumPy chunk.

    Parameters
    ----------
    *arrays : numpy.ndarray
        Variable data arrays with time as the last dimension.
    season_ids : numpy.ndarray
        Season IDs for each time step.
    bounds_lower : numpy.ndarray
        Lower bound thresholds per variable.
    bounds_upper : numpy.ndarray
        Upper bound thresholds per variable.
    bounds_inc_lower : numpy.ndarray
        Inclusivity flags for lower bounds.
    bounds_inc_upper : numpy.ndarray
        Inclusivity flags for upper bounds.
    combiner : str
        Combination logic ('all', 'any', 'k_of_n').
    k : int
        Minimum passing variable count for 'k_of_n'.
    min_duration : int
        Minimum consecutive qualifying days.
    na_action : str
        NaN handling policy ('false', 'skip_vars', 'skip_days').
    max_run : bool, default=False
        If True, reports running maximum spell length.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
        Tuple of (cond, valid, cum_days).
    """
    n_vars = len(arrays)
    sp_shape = arrays[0].shape[:-1]
    n_time = arrays[0].shape[-1]

    x_all = np.stack([a.reshape(-1, n_time).astype(float) for a in arrays])
    n_sp = x_all.shape[1]

    is_nan_all = np.isnan(x_all)

    per_var_cond = np.zeros((n_vars, n_sp, n_time), dtype=bool)
    for i in range(n_vars):
        x = x_all[i]
        lo_ok = (x >= bounds_lower[i]) if bounds_inc_lower[i] else (x > bounds_lower[i])
        hi_ok = (x <= bounds_upper[i]) if bounds_inc_upper[i] else (x < bounds_upper[i])
        per_var_cond[i] = lo_ok & hi_ok & ~is_nan_all[i]

    if na_action == "skip_vars":
        n_true = per_var_cond.sum(axis=0)
        n_avail = (~is_nan_all).sum(axis=0).astype(float)
        if combiner == "all":
            cond = (n_true == n_avail) & (n_avail > 0)
        elif combiner == "any":
            cond = n_true >= 1
        else:
            cond = n_true >= k
    else:
        if na_action == "skip_days":
            any_nan = is_nan_all.any(axis=0)
            per_var_cond = np.where(any_nan, False, per_var_cond)

        n_true = per_var_cond.sum(axis=0)
        n_avail = n_vars
        if combiner == "all":
            cond = n_true == n_avail
        elif combiner == "any":
            cond = n_true >= 1
        else:
            cond = n_true >= k

    in_season = ~np.isnan(season_ids)
    cond = np.where(in_season, cond, False)

    out_valid = np.zeros((n_sp, n_time), dtype=float)
    out_cum_days = np.zeros((n_sp, n_time), dtype=float)

    m = max(min_duration - 1, 0)
    unique_seasons = np.unique(season_ids[in_season])

    skip_nan_mask = is_nan_all.any(axis=0) if na_action == "skip_days" else np.zeros((n_sp, n_time), dtype=bool)

    for sid in unique_seasons:
        smask = season_ids == sid
        c = cond[:, smask]

        if na_action == "skip_days":
            is_nan_seas = skip_nan_mask[:, smask]
            run_len = np.stack([_run_length_skip_nan_1d(c[sp], is_nan_seas[sp]) for sp in range(n_sp)])
        else:
            run_len = _run_length_2d(c)

        v = c & (run_len >= min_duration)

        if max_run:
            if na_action == "skip_days":
                cons_days = np.zeros_like(v, dtype=int)
                for sp in range(n_sp):
                    valid_steps = np.where(~is_nan_seas[sp])[0]
                    if len(valid_steps) > 0:
                        v_sub = v[sp, valid_steps].astype(bool)
                        cons_sub = _consecutive_true_2d(v_sub.reshape(1, -1))[0]
                        cons_days[sp, valid_steps] = cons_sub
            else:
                cons_days = _consecutive_true_2d(v.astype(bool))
            true_run_len = np.where(v, cons_days + m, 0)
            season_cum = np.maximum.accumulate(true_run_len, axis=1).astype(float)
        else:
            bonus = np.where(run_len == min_duration, m, 0)
            season_cum = np.cumsum(v.astype(int) + bonus, axis=1).astype(float)

        out_valid[:, smask] = v.astype(float)
        out_cum_days[:, smask] = season_cum

    return (
        cond.astype(float).reshape((*sp_shape, n_time)),
        out_valid.reshape((*sp_shape, n_time)),
        out_cum_days.reshape((*sp_shape, n_time)),
    )


def cdi(
    ds: xr.Dataset,
    bounds: pd.DataFrame | list[dict[str, Any]],
    season_start: str = "07-01",
    season_end: str = "06-30",
    combiner: Literal["all", "any", "k_of_n"] = "all",
    k: int | None = None,
    min_duration: int = 1,
    na_action: Literal["false", "skip_vars", "skip_days"] = "false",
    daily_agg: str | dict[str, str] = "mean",
    max_run: bool = False,
) -> xr.Dataset:
    """
    Compute Condition Duration Index (CDI) across one or more climate variables.

    Evaluates conditions across multiple variables using boolean combination
    and counts cumulative qualifying days or spell lengths with bias correction
    according to Begueria et al. (2026).

    Parameters
    ----------
    ds : xarray.Dataset
        Input dataset containing all required variables.
    bounds : pandas.DataFrame | list[dict[str, Any]]
        Per-variable thresholds table with column 'var' and optional bounds.
    season_start : str, default="07-01"
        First day of accumulation season in 'mm-dd' format.
    season_end : str, default="06-30"
        Last day of accumulation season in 'mm-dd' format.
    combiner : Literal['all', 'any', 'k_of_n'], default='all'
        Combination logic for variables.
    k : int | None, default=None
        Minimum number of passing variables when combiner='k_of_n'.
    min_duration : int, default=1
        Minimum consecutive days for a run.
    na_action : Literal['false', 'skip_vars', 'skip_days'], default='false'
        Handling of NaN values across variables.
    daily_agg : str | dict[str, str], default='mean'
        Resampling method when sub-daily data is provided.
    max_run : bool, default=False
        If True, reports running maximum spell length instead of total count.

    Returns
    -------
    xarray.Dataset
        Dataset containing 'cond', 'valid', and 'cum_days'.
    """
    combiner_clean = combiner.lower()
    if combiner_clean not in ("all", "any", "k_of_n"):
        raise ValueError(f"combiner must be 'all', 'any', or 'k_of_n', got {combiner!r}.")
    if combiner_clean == "k_of_n":
        if k is None:
            raise ValueError("Provide k (int) when combiner='k_of_n'.")
        k_val = int(k)
    else:
        k_val = 0

    na_action_clean = na_action.lower()
    if na_action_clean not in ("false", "skip_vars", "skip_days"):
        raise ValueError(f"na_action must be 'false', 'skip_vars', or 'skip_days', got {na_action!r}.")
    if min_duration < 1:
        raise ValueError(f"min_duration must be >= 1, got {min_duration}.")

    bounds_df = _normalise_bounds(bounds)
    var_names = list(bounds_df["var"])
    missing = [v for v in var_names if v not in ds.data_vars]
    if missing:
        raise ValueError(f"Variable(s) {missing} not found in ds. Available: {list(ds.data_vars)}.")

    das: list[xr.DataArray] = []
    for var in var_names:
        da = ds[var]
        if _is_subdaily(da):
            method = daily_agg.get(var, "mean") if isinstance(daily_agg, dict) else daily_agg
            da = _resample_to_daily(da, method=method)
        das.append(da)

    ref_time = das[0].time

    _, season_ids = build_seasons_map(ref_time, season_start, season_end)
    if np.all(np.isnan(season_ids)):
        raise ValueError(f"No time steps fall within the season window {season_start!r} -> {season_end!r}.")

    bounds_lower = bounds_df["lower"].values.astype(float)
    bounds_upper = bounds_df["upper"].values.astype(float)
    bounds_inc_lower = bounds_df["inc_lower"].values.astype(bool)
    bounds_inc_upper = bounds_df["inc_upper"].values.astype(bool)

    orig_dims = das[0].dims
    n_vars = len(das)

    raw_outputs = xr.apply_ufunc(
        _cdi_numpy,
        *das,
        input_core_dims=[["time"]] * n_vars,
        output_core_dims=[["time"], ["time"], ["time"]],
        kwargs=dict(
            season_ids=season_ids,
            bounds_lower=bounds_lower,
            bounds_upper=bounds_upper,
            bounds_inc_lower=bounds_inc_lower,
            bounds_inc_upper=bounds_inc_upper,
            combiner=combiner_clean,
            k=k_val,
            min_duration=int(min_duration),
            na_action=na_action_clean,
            max_run=bool(max_run),
        ),
        dask="parallelized",
        output_dtypes=[float, float, float],
    )

    cond_raw, valid_raw, cum_days_raw = raw_outputs

    def _finalise(arr: xr.DataArray, name: str, description: str) -> xr.DataArray:
        arr = arr.assign_coords(time=ref_time)
        if set(arr.dims) == set(orig_dims):
            arr = arr.transpose(*orig_dims)
        arr.name = name
        arr.attrs["long_name"] = description
        return arr

    ds_out = xr.Dataset({
        "cond": _finalise(cond_raw, "cond", "Combined qualifying day flag (1 = condition met, 0 otherwise)"),
        "valid": _finalise(valid_raw, "valid", "Contributing day flag (1 = run >= min_duration, 0 otherwise)"),
        "cum_days": _finalise(cum_days_raw, "cum_days", "Seasonal cumulative qualifying day count (CDI)"),
    })

    ds_out = ds_out.assign_coords(season_id=("time", season_ids))
    ds_out.attrs.update({
        "index": "CDI",
        "season_start": season_start,
        "season_end": season_end,
        "combiner": combiner_clean,
        "k": str(k_val) if combiner_clean == "k_of_n" else "N/A",
        "min_duration": min_duration,
        "na_action": na_action_clean,
        "variables": ", ".join(var_names),
        "reference": "Begueria et al. (2026)",
    })

    return ds_out
