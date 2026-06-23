# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import numpy as np
import xarray as xr
from xclim.core.calendar import percentile_doy

# 365-day calendar
_CLIM_FREQ_AS_DOY = {
    "dayofyear": None,
    "month": np.repeat([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]),
    "season": np.repeat(["DJF", "MAM", "JJA", "SON", "DJF"], [59, 92, 92, 91, 31]),
}


def as_doy_climatology(da, fallback_axis=None):
    for freq, mapping in _CLIM_FREQ_AS_DOY.items():
        if freq in da.coords:
            return (
                da
                .sel({freq: mapping})
                .assign_coords({"dayofyear": (freq, np.arange(1, 366))})
                .swap_dims({freq: "dayofyear"})
                .drop_vars(freq)
            )
    # Insert day of year dimension where time dimension was before aggregation
    return da.expand_dims({"dayofyear": np.arange(1, 366)}, axis=fallback_axis)


def get_percentile(
    baseline_dataset: xr.Dataset,
    varname: str,
    percentile: float,
    freq: str = "YS",
) -> xr.Dataset:
    """
    Compute a regular percentile (e.g. 90th) of a variable over time,
    grouped by a temporal component (month, season, or year),
    and expand the result to have one value per day of the input period.
    The final dataset uses 'dayofyear' as the main temporal dimension.

    Parameters
    ----------
    baseline_dataset : xr.Dataset
        Dataset containing the variable to analyze.
    varname : str
        Name of the variable within the dataset.
    percentile : float
        Percentile value (e.g., 90 for 90th percentile).
    freq : str, optional
        Frequency for grouping (e.g. 'YS', 'MS', 'QS'). Default is yearly.

    Returns
    -------
    xr.Dataset
        Dataset with the computed percentile values expanded to daily resolution,
        using 'dayofyear' (1–365) as the main coordinate.
    """
    da = baseline_dataset[varname]
    q = percentile / 100.0

    time_axis = da.get_axis_num("time")
    time_component = pandas_offset2time_component(freq)

    if time_component is not None:
        da = da.groupby(f"time.{time_component}")

    out = da.quantile(q=q, dim="time")
    out = as_doy_climatology(out, fallback_axis=time_axis)
    return out.to_dataset(name=varname)


def pandas_offset2time_component(aggregation: str) -> str:
    """
    Map a pandas-style frequency string to a corresponding time component.

    Parameters
    ----------
    aggregation : str
        Frequency alias following pandas conventions (e.g., 'YS', 'QS-DEC', 'MS').

    Returns
    -------
    str
        Time component corresponding to the given frequency:
        - 'YS' → 'year'
        - 'QS-DEC' → 'season'
        - 'MS' → 'month'

    Raises
    ------
    NotImplementedError
        If the provided frequency alias is not supported.
    """
    if aggregation == "YS":
        resolution = None
    elif aggregation == "QS-DEC":
        resolution = "season"
    elif aggregation == "MS":
        resolution = "month"
    else:
        raise NotImplementedError(f"Unsupported aggregation: {aggregation}")
    return resolution


def calculate_percentile_doy(
    reference_dataset: xr.Dataset,
    variable: str,
    percentile: float,
    window: int = 5,
) -> xr.Dataset:
    """
    Calculate the daily percentile (doy) for a given variable in a reference dataset.
    Wraps xclim.core.calendar.percentile_doy.

    Parameters
    ----------
    reference_dataset : xr.Dataset
        The reference dataset containing the variable.
    variable : str
        The name of the variable to calculate the percentile for.
    percentile : float
        The percentile value (e.g., 90 for 90th percentile).
    window : int, optional
        The window size for the rolling percentile calculation, by default 5.

    Returns
    -------
    xr.Dataset
        A dataset containing the calculated percentile, renamed to '{variable}_per'.
    """
    if variable not in reference_dataset:
        raise ValueError(f"Variable '{variable}' not found in reference dataset.")

    # Calculate percentile
    per = percentile_doy(reference_dataset[variable], window=window, per=percentile)

    # Rename variable
    per_name = f"{variable}_per"
    per = per.rename(per_name)

    # If the percentile is a singleton, squeeze the dimension to avoid downstream plotting issues
    if "percentiles" in per.dims and per.sizes["percentiles"] == 1:
        per = per.squeeze("percentiles", drop=True)

    return per.to_dataset()
