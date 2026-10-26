# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

"""Utilities to work with climatologies.

.. seealso:: :py:mod:`earthkit.transforms.climatology`
"""

from dataclasses import dataclass
from typing import Literal, Optional

import numpy as np
import xarray as xr


@dataclass
class _UpsamplerParameters:
    coords: list | np.ndarray
    repeats: dict


_UPSAMPLER_PARAMS = {
    "dayofyear": _UpsamplerParameters(
        coords=np.arange(1, 366 + 1),
        repeats={
            "season": (["DJF", "MAM", "JJA", "SON", "DJF"], [60, 92, 92, 91, 31]),
            "month": ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]),
        },
    ),
    "month": _UpsamplerParameters(
        coords=np.arange(1, 12 + 1),
        repeats={
            "season": (["DJF", "MAM", "JJA", "SON", "DJF"], [2, 3, 3, 3, 1]),
        },
    ),
    "season": _UpsamplerParameters(coords=["DJF", "MAM", "JJA", "SON"], repeats={}),
}


def upsample(
    da: xr.DataArray,
    frequency: Literal["dayofyear", "month", "season"] = "dayofyear",
    fallback_axis: Optional[int] = None,
) -> xr.DataArray:
    """Upsample a climatology by repetition of values.

    .. warning:: Experimental API. This function may change or be removed without notice.

    Parameters
    ----------
    da : xarray.DataArray
        Input climatology.
    frequency : "dayofyear" | "month" | "season"
        Frequency of upsampled climatology.
    fallback_axis : int, optional
        When no suitable temporal axis is recognised on the input climatology,
        upsampling fails unless the position to insert a new climatology
        dimension is explicitly specified with this parameter.

    Returns
    -------
    xarray.DataArray
        Upsampled climatology.
    """
    if frequency in da.dims:
        return da
    # Load upsample parameters for the given target frequency
    try:
        upsampler = _UPSAMPLER_PARAMS[frequency]
    except KeyError:
        raise NotImplementedError(f"unable to upsample to frequency {frequency!r}")
    # Find a compatible climatology time dim in the input climatology
    for source_frequency, repeat_args in upsampler.repeats.items():
        if source_frequency in da.dims:
            return (
                da
                .sel({source_frequency: np.repeat(*repeat_args)})
                .assign_coords({frequency: (source_frequency, upsampler.coords)})
                .swap_dims({source_frequency: frequency})
            )
    # Insert new climatology time dim if no suitable input (also catches downsampling attempts)
    if fallback_axis is None:
        raise ValueError(
            f"no suitable time dimension found for upsampling to frequency {frequency!r}, supply fallback_axis"
        )
    return da.expand_dims({frequency: upsampler.coords}, axis=fallback_axis)


def rolling_percentiles(
    dataarray: xr.DataArray,
    p: float | list,
    frequency: Literal["dayofyear"] = "dayofyear",
    window_width: int = 5,
    **reduce_kwargs,
) -> xr.DataArray:
    """Calculate a set of climatological percentiles in a rolling window.

    .. warning:: Experimental API. This function may change or be removed without notice.

    Parameters
    ----------
    dataarray : xarray.DataArray
        The DataArray over which to calculate the climatological percentiles.
        Must contain a time dimension.
    p : float | list
        The percentile, or list of percentiles, to calculate the climatology.
    frequency : "dayofyear"
        Only `dayofyear` is currently supported.
    window_width : int
        The window size for the rolling percentile calculation, by default 5.
    **reduce_kwargs
        Any other kwargs accepted by the reduction function.

    Returns
    -------
    xarray.DataArray

    See Also
    --------
    earthkit.transforms.climatology.percentiles

    Notes
    -----
    Uses `xclim.core.calendar.percentile_doy` to compute rolling day-of-year
    percentiles.
    """
    if frequency == "dayofyear":
        from xclim.core.calendar import percentile_doy

        return (
            percentile_doy(dataarray, window=window_width, per=p, **reduce_kwargs)
            # Adopt conventions of earthkit-transforms (except dim-order)
            .rename({"percentiles": "percentile"})
            .rename(dataarray.name)
        )
    raise NotImplementedError(f"frequency {frequency!r} not accepted, only 'dayofyear'")
