# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Callable
from typing import Any, Literal

import numpy as np
import xarray as xr

from earthkit.climate.indicators.xarray.agro.engine.seasons import build_seasons_map

_DAILY_AGG_METHODS = frozenset({"mean", "sum", "max", "min", "median"})


def _resample_to_daily(da: xr.DataArray, method: str) -> xr.DataArray:
    """
    Resample a sub-daily DataArray to daily resolution using a specified method.

    Parameters
    ----------
    da : xarray.DataArray
        Input DataArray with a datetime time dimension.
    method : str
        Aggregation method ('mean', 'sum', 'max', 'min', 'median').

    Returns
    -------
    xarray.DataArray
        Daily resampled DataArray.
    """
    if method not in _DAILY_AGG_METHODS:
        raise ValueError(f"Unknown daily aggregation method {method!r}. Choose from {sorted(_DAILY_AGG_METHODS)}.")
    result = getattr(da.resample(time="1D"), method)()
    if result.chunks:
        result = result.chunk({"time": -1})
    return result


def _is_subdaily(da: xr.DataArray) -> bool:
    """
    Check if a DataArray has a sub-daily temporal resolution.

    Parameters
    ----------
    da : xarray.DataArray
        Input DataArray with a time dimension.

    Returns
    -------
    bool
        True if the DataArray is sub-daily, False otherwise.
    """
    freq = xr.infer_freq(da.time)
    if freq is None:
        return False
    subdaily_prefixes = ("h", "H", "T", "min", "S", "L", "ms", "U", "us", "N", "ns")
    return any(freq.lstrip("0123456789").startswith(p) for p in subdaily_prefixes)


def _run_length_2d(cond: np.ndarray) -> np.ndarray:
    """
    Calculate run length of consecutive True elements along the last axis.

    Vectorised run-length counter matching R CEI reference semantics.
    For True elements, computes the position within each cumsum(~cond) group.

    Parameters
    ----------
    cond : numpy.ndarray
        Boolean array with time as the last axis.

    Returns
    -------
    numpy.ndarray
        Array of the same shape containing 1-based run lengths or 0 for False.
    """
    cum_true = np.cumsum(cond, axis=-1)
    false_cum = np.where(~cond, cum_true, 0)
    false_cum_propagated = np.maximum.accumulate(false_cum, axis=-1)
    return np.where(cond, cum_true - false_cum_propagated, 0)


def _run_length_skip_nan_1d(cond_1d: np.ndarray, is_nan_1d: np.ndarray) -> np.ndarray:
    """
    Calculate 1-D run length where NaN positions are treated as transparent.

    Parameters
    ----------
    cond_1d : numpy.ndarray
        Boolean array of length n_time.
    is_nan_1d : numpy.ndarray
        Boolean mask of length n_time, True where data is NaN.

    Returns
    -------
    numpy.ndarray
        Integer array of shape (n_time,) with run lengths.
    """
    n = len(cond_1d)
    non_nan_idx = np.where(~is_nan_1d)[0]
    if len(non_nan_idx) == 0:
        return np.zeros(n, dtype=int)

    cond_compressed = cond_1d[non_nan_idx]
    rl_compressed = _run_length_2d(cond_compressed.reshape(1, -1))[0]

    run_len = np.zeros(n, dtype=int)
    run_len[non_nan_idx] = rl_compressed
    return run_len


def _cei_numpy(
    x: np.ndarray,
    *,
    season_ids: np.ndarray,
    lower: float,
    upper: float,
    inc_lower: bool,
    inc_upper: bool,
    min_duration: int,
    na_action: str,
    direction: str,
    weight_fn: Callable[..., Any] | None,
    unit_contribution: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Execute core CEI numerical calculation over a NumPy chunk.

    Parameters
    ----------
    x : numpy.ndarray
        Input values array of shape (..., n_time).
    season_ids : numpy.ndarray
        1-D float array of length n_time with season IDs or NaN.
    lower : float
        Lower threshold bound.
    upper : float
        Upper threshold bound.
    inc_lower : bool
        Whether lower bound is inclusive.
    inc_upper : bool
        Whether upper bound is inclusive.
    min_duration : int
        Minimum consecutive days for a qualifying run.
    na_action : str
        NaN handling policy ('false' or 'skip_days').
    direction : str
        Direction of excess ('above' or 'below').
    weight_fn : collections.abc.Callable | None
        Optional weighting function f(x) -> y.
    unit_contribution : bool, default=False
        If True, each qualifying step contributes 1 unit regardless of value.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]
        Tuple of (cond, valid, excess, cum_excess).
    """
    sp_shape = x.shape[:-1]
    n_time = x.shape[-1]
    x2d = x.reshape(-1, n_time).astype(float)
    n_sp = x2d.shape[0]

    is_nan_2d = np.isnan(x2d)

    lo_ok = (x2d >= lower) if inc_lower else (x2d > lower)
    hi_ok = (x2d <= upper) if inc_upper else (x2d < upper)
    cond = lo_ok & hi_ok & ~is_nan_2d

    if unit_contribution:
        excess = np.where(cond, 1.0, 0.0)
    elif weight_fn is not None:
        scored = np.asarray(weight_fn(x2d), dtype=float)
        excess = np.where(cond, scored, 0.0)
    elif direction == "below":
        excess = np.where(cond, np.maximum(upper - x2d, 0.0), 0.0)
    else:
        excess = np.where(cond, np.maximum(x2d - lower, 0.0), 0.0)

    in_season = ~np.isnan(season_ids)
    cond = np.where(in_season, cond, False)
    excess = np.where(in_season, excess, 0.0)

    out_valid = np.zeros((n_sp, n_time), dtype=float)
    out_cum_excess = np.zeros((n_sp, n_time), dtype=float)

    k = max(min_duration - 1, 0)
    unique_seasons = np.unique(season_ids[in_season])

    for sid in unique_seasons:
        smask = season_ids == sid
        c = cond[:, smask]
        e = excess[:, smask]
        n_seas = c.shape[1]

        if na_action == "skip_days":
            is_nan_seas = is_nan_2d[:, smask]
            run_len = np.stack([_run_length_skip_nan_1d(c[sp], is_nan_seas[sp]) for sp in range(n_sp)])
        else:
            run_len = _run_length_2d(c)

        v = c & (run_len >= min_duration)

        if k > 0:
            if na_action == "skip_days":
                bonus = np.zeros((n_sp, n_seas), dtype=float)
                for sp in range(n_sp):
                    valid_steps = np.where(~is_nan_seas[sp])[0]
                    if len(valid_steps) >= min_duration:
                        rl_sub = run_len[sp, valid_steps]
                        e_sub = e[sp, valid_steps]
                        c_sub = np.cumsum(e_sub)
                        pc_sub = np.concatenate([[0.0], c_sub[:-1]])
                        pk_sub = np.concatenate([np.zeros(k), pc_sub[:-k]])
                        b_sub = np.where(rl_sub == min_duration, pc_sub - pk_sub, 0.0)
                        bonus[sp, valid_steps] = b_sub
            else:
                cum_exc = np.cumsum(e, axis=1)
                prev_cum = np.concatenate([np.zeros((n_sp, 1)), cum_exc[:, :-1]], axis=1)
                prev_k = np.concatenate([np.zeros((n_sp, k)), prev_cum[:, :-k]], axis=1)
                bonus = np.where(run_len == min_duration, prev_cum - prev_k, 0.0)
        else:
            bonus = np.zeros((n_sp, n_seas), dtype=float)

        season_cum = np.cumsum(v * e + bonus, axis=1)

        out_valid[:, smask] = v
        out_cum_excess[:, smask] = season_cum

    return (
        cond.reshape((*sp_shape, n_time)).astype(float),
        out_valid.reshape((*sp_shape, n_time)),
        excess.reshape((*sp_shape, n_time)),
        out_cum_excess.reshape((*sp_shape, n_time)),
    )


def cei(
    da: xr.DataArray,
    season_start: str = "07-01",
    season_end: str = "06-30",
    lower: float = -np.inf,
    upper: float = np.inf,
    inc_lower: bool = True,
    inc_upper: bool = True,
    min_duration: int = 1,
    na_action: Literal["false", "skip_days"] = "false",
    direction: Literal["above", "below"] = "above",
    weight_fn: Callable[..., Any] | None = None,
    daily_agg: str = "mean",
    native_freq: bool = False,
    unit_contribution: bool = False,
) -> xr.Dataset:
    """
    Compute Condition Excess Index (CEI) for a single climate variable.

    Accumulates seasonal excess or deficit values above or below a threshold
    across defined season windows with optional minimum duration and bias correction
    according to Begueria et al. (2026).

    Parameters
    ----------
    da : xarray.DataArray
        Input meteorological variable array with a time dimension.
    season_start : str, default="07-01"
        First day of accumulation season in 'mm-dd' format.
    season_end : str, default="06-30"
        Last day of accumulation season in 'mm-dd' format.
    lower : float, default=-inf
        Lower qualifying threshold bound.
    upper : float, default=inf
        Upper qualifying threshold bound.
    inc_lower : bool, default=True
        Whether the lower bound is inclusive.
    inc_upper : bool, default=True
        Whether the upper bound is inclusive.
    min_duration : int, default=1
        Minimum consecutive days for a run before contributing to excess.
    na_action : Literal['false', 'skip_days'], default='false'
        Handling of NaN values.
    direction : Literal['above', 'below'], default='above'
        Direction of excess calculation.
    weight_fn : collections.abc.Callable | None, default=None
        Custom weighting function f(x) -> y.
    daily_agg : str, default='mean'
        Resampling method when sub-daily data is provided.
    native_freq : bool, default=False
        If True, skips sub-daily to daily resampling.
    unit_contribution : bool, default=False
        If True, each qualifying step contributes 1 unit regardless of value.

    Returns
    -------
    xarray.Dataset
        Dataset containing 'cond', 'valid', 'excess', and 'cum_excess'.
    """
    if direction not in ("above", "below"):
        raise ValueError(f"direction must be 'above' or 'below', got {direction!r}.")
    if not unit_contribution and weight_fn is None:
        if direction == "below" and not np.isfinite(upper):
            raise ValueError("direction='below' requires a finite upper bound.")
        if direction == "above" and not np.isfinite(lower):
            raise ValueError("direction='above' requires a finite lower bound when calculating excess.")
    if weight_fn is not None and not callable(weight_fn):
        raise TypeError("weight_fn must be callable or None.")
    if min_duration < 1:
        raise ValueError(f"min_duration must be >= 1, got {min_duration}.")
    if na_action not in ("false", "skip_days"):
        raise ValueError(f"na_action must be 'false' or 'skip_days', got {na_action!r}.")
    if daily_agg not in _DAILY_AGG_METHODS:
        raise ValueError(f"daily_agg must be one of {sorted(_DAILY_AGG_METHODS)}, got {daily_agg!r}.")

    if native_freq:
        da_daily = da
    elif _is_subdaily(da):
        da_daily = _resample_to_daily(da, method=daily_agg)
    else:
        da_daily = da

    _, season_ids = build_seasons_map(da_daily.time, season_start, season_end)

    if np.all(np.isnan(season_ids)):
        raise ValueError(f"No time steps fall within the season window {season_start!r} -> {season_end!r}.")

    orig_dims = da_daily.dims

    raw_outputs = xr.apply_ufunc(
        _cei_numpy,
        da_daily,
        input_core_dims=[["time"]],
        output_core_dims=[["time"], ["time"], ["time"], ["time"]],
        kwargs=dict(
            season_ids=season_ids,
            lower=float(lower),
            upper=float(upper),
            inc_lower=bool(inc_lower),
            inc_upper=bool(inc_upper),
            min_duration=int(min_duration),
            na_action=na_action,
            direction=direction,
            weight_fn=weight_fn,
            unit_contribution=bool(unit_contribution),
        ),
        dask="parallelized",
        output_dtypes=[float, float, float, float],
    )

    cond_raw, valid_raw, excess_raw, cum_excess_raw = raw_outputs

    def _finalise(arr: xr.DataArray, name: str, description: str) -> xr.DataArray:
        arr = arr.assign_coords(time=da_daily.time)
        if set(arr.dims) == set(orig_dims):
            arr = arr.transpose(*orig_dims)
        arr.name = name
        arr.attrs["long_name"] = description
        return arr

    ds = xr.Dataset({
        "cond": _finalise(cond_raw, "cond", "Qualifying day flag (1 = within bounds, 0 otherwise)"),
        "valid": _finalise(valid_raw, "valid", "Contributing day flag (1 = run >= min_duration, 0 otherwise)"),
        "excess": _finalise(excess_raw, "excess", "Per-day excess/deficit contribution"),
        "cum_excess": _finalise(cum_excess_raw, "cum_excess", "Seasonal cumulative excess index (CEI)"),
    })

    ds = ds.assign_coords(season_id=("time", season_ids))
    ds.attrs.update({
        "index": "CEI",
        "season_start": season_start,
        "season_end": season_end,
        "lower": str(lower),
        "upper": str(upper),
        "direction": direction,
        "min_duration": min_duration,
        "na_action": na_action,
        "reference": "Begueria et al. (2026)",
    })

    return ds
