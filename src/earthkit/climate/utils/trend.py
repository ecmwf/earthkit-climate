# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

"""Utilities for fitting trends to time series."""

from collections.abc import Hashable
from typing import Any

import numpy as np
import xarray as xr
from earthkit.utils.decorators import format_handler
from scipy.stats import linregress


def _is_datetime_coordinate(coord: xr.DataArray) -> bool:
    """Return whether a coordinate contains NumPy or cftime datetimes."""
    if np.issubdtype(coord.dtype, np.datetime64):
        return True
    if coord.dtype.kind == "O" and coord.size:
        value = coord.values.flat[0]
        return all(hasattr(value, attr) for attr in ("year", "month", "day"))
    return False


def _is_time_coordinate(name: Hashable, coord: xr.DataArray) -> bool:
    """Identify time coordinates from their name, CF metadata, or dtype."""
    return (
        name == "time"
        or coord.attrs.get("standard_name") == "time"
        or coord.attrs.get("axis") == "T"
        or _is_datetime_coordinate(coord)
    )


def _time_coordinate(data: xr.DataArray | xr.Dataset, dim: Hashable) -> xr.DataArray | None:
    """Return the time coordinate associated with a dimension, if present."""
    for name, coord in data.coords.items():
        if coord.dims == (dim,) and _is_time_coordinate(name, coord):
            return coord
    # A dimension coordinate may be explicitly selected even without time metadata.
    return data.coords[dim] if dim in data.coords else None


def _time_dimension(data: xr.DataArray | xr.Dataset, dim: Hashable | None) -> tuple[Hashable, xr.DataArray | None]:
    """Resolve the time dimension and coordinate, raising if detection is ambiguous."""
    if dim is not None:
        if dim not in data.dims:
            raise ValueError(f"time dimension {dim!r} is not present in the input")
        return dim, _time_coordinate(data, dim)

    candidates = {}
    for name, coord in data.coords.items():
        # Ignore scalar, multidimensional, and unrelated coordinates.
        if coord.ndim != 1 or coord.dims[0] not in data.dims:
            continue
        if _is_time_coordinate(name, coord):
            candidates.setdefault(coord.dims[0], coord)
    if not candidates and "time" in data.dims:
        return "time", _time_coordinate(data, "time")

    if len(candidates) != 1:
        if not candidates:
            raise ValueError("unable to detect a time coordinate; specify the time dimension with dim")
        raise ValueError(f"multiple time dimensions detected: {sorted(map(str, candidates))}; specify dim")
    time_dim, time_coord = candidates.popitem()
    return time_dim, time_coord


def _numeric_time(dim: Hashable, coord: xr.DataArray | None) -> np.ndarray:
    """Convert a decoded datetime coordinate to elapsed years."""
    if coord is None or not _is_datetime_coordinate(coord):
        raise ValueError(f"time coordinate {dim!r} must contain decoded datetime values")

    elapsed = coord - coord.isel({dim: 0})
    elapsed_years = elapsed.dt.total_seconds() / (86400 * 365.2425)
    return np.asarray(elapsed_years, dtype=float)


def _linregress(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Fit one series, ignoring missing pairs, and return slope and p-value."""
    valid = np.isfinite(x) & np.isfinite(y)
    if valid.sum() < 2:
        return np.nan, np.nan
    x_valid = x[valid]
    y_valid = y[valid]
    regression = linregress(x_valid, y_valid)
    return float(regression.slope), float(regression.pvalue)


def _linear_trend_array(
    data: xr.DataArray, dim: Hashable, time_coord: xr.DataArray | None
) -> tuple[xr.DataArray, xr.DataArray]:
    """Fit a trend along one DataArray dimension and prepare output metadata."""
    if dim not in data.dims:
        raise ValueError(f"input data does not contain time dimension {dim!r}")
    if not np.issubdtype(data.dtype, np.number):
        raise TypeError(f"input data must be numeric, got {data.dtype}")

    x = _numeric_time(dim, time_coord)
    if x.ndim != 1 or x.size != data.sizes[dim]:
        raise ValueError(f"time coordinate {dim!r} must be one-dimensional")

    # Vectorize the scalar SciPy regression over all remaining dimensions while
    # retaining xarray's coordinate handling and support for chunked arrays.
    result, p_values = xr.apply_ufunc(
        _linregress,
        xr.DataArray(x, dims=(dim,)),
        data,
        input_core_dims=[[dim], [dim]],
        output_core_dims=[[], []],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float],
        dask_gufunc_kwargs={"allow_rechunk": True},
    )

    name = f"{data.name}_linear_trend" if data.name else "linear_trend"
    result = result.rename(name)
    attrs = dict(data.attrs)
    attrs.pop("standard_name", None)
    attrs.pop("cell_methods", None)
    attrs["long_name"] = f"Linear trend of {data.name}" if data.name else "Linear trend"
    if data.attrs.get("units"):
        attrs["units"] = f"{data.attrs['units']} year-1"
    else:
        attrs.pop("units", None)
    result.attrs = attrs

    p_value_name = f"{data.name}_p_value" if data.name else "p_value"
    p_values = p_values.rename(p_value_name)
    p_values.attrs = {
        "long_name": f"P-value for linear trend of {data.name}" if data.name else "P-value for linear trend",
        "units": "1",
    }
    return result, p_values


@format_handler()
def linear_trend(
    data: xr.DataArray | xr.Dataset | Any,
    dim: Hashable | None = None,
    return_p_values: bool = False,
) -> xr.DataArray | xr.Dataset | tuple[xr.DataArray | xr.Dataset, xr.DataArray | xr.Dataset] | Any:
    """Calculate the linear trend along a time dimension.

    The slope is calculated independently for each series along the detected
    time dimension. The time coordinate must contain decoded datetime values;
    slopes are expressed per year. Missing values are ignored, and series with
    fewer than two valid samples or no time variation produce NaN.

    For a Dataset, each data variable must be numeric; variables are fitted
    independently and returned as separate trend variables. The p-value is
    SciPy's two-sided test for a zero slope; it is NaN when regression cannot
    be fitted.

    Parameters
    ----------
    data : xarray.DataArray | xarray.Dataset | Any
        Input time series. Other supported formats are handled by
        :func:`earthkit.utils.decorators.format_handler`.
    dim : hashable, optional
        Time dimension. If omitted, the time coordinate is detected from its
        name, CF ``standard_name`` or ``axis`` attribute, or datetime values.
        The selected coordinate must contain decoded datetime values.
    return_p_values : bool, default=False
        Whether to also return p-values from the linear regression. When true,
        the result is a ``(trend, p_values)`` tuple.

    Returns
    -------
    xarray.DataArray | xarray.Dataset | tuple
        The slope along the time dimension, with that dimension removed. If
        ``return_p_values`` is true, also returns a p-value result. For xarray
        inputs, output names and attributes describe the trend and units are
        expressed per year when input units are available.
    """
    time_dim, time_coord = _time_dimension(data, dim)
    if isinstance(data, xr.DataArray):
        trend, p_values = _linear_trend_array(data, time_dim, time_coord)
    elif isinstance(data, xr.Dataset):
        pairs = [_linear_trend_array(array, time_dim, time_coord) for array in data.data_vars.values()]
        trend = xr.Dataset({item.name: item for item, _ in pairs}, attrs=data.attrs)
        p_values = xr.Dataset({item.name: item for _, item in pairs}, attrs=data.attrs)
    else:
        raise TypeError(f"unsupported input type: {type(data).__name__}")
    return (trend, p_values) if return_p_values else trend
