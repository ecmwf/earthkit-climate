# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import re

import numpy as np
import pandas as pd
import xarray as xr

_MM_DD_RE = re.compile(r"^(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")


def _parse_mmdd(value: str, param: str) -> tuple[int, int]:
    """
    Parse and validate a 'mm-dd' string into (month, day).

    Parameters
    ----------
    value : str
        Date string in 'mm-dd' format.
    param : str
        Parameter name for error messages.

    Returns
    -------
    tuple[int, int]
        Tuple of (month, day) as integers.
    """
    m = _MM_DD_RE.match(value)
    if not m:
        raise ValueError(f"Invalid format for {param!r}: {value!r}. Expected 'mm-dd', e.g. '07-01' or '04-30'.")
    return int(m.group(1)), int(m.group(2))


def build_seasons_map(
    time: xr.DataArray | np.ndarray | pd.DatetimeIndex,
    season_start: str = "07-01",
    season_end: str = "06-30",
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Build non-overlapping season intervals and map each time step to a season ID.

    Generates non-overlapping season intervals that may cross calendar-year
    boundaries and returns a mapping from each time step to its season
    identifier. Out-of-season days receive NaN.

    Parameters
    ----------
    time : xarray.DataArray | numpy.ndarray | pandas.DatetimeIndex
        Time coordinate or array of datetime64 values.
    season_start : str, default="07-01"
        First day of the season in 'mm-dd' format.
    season_end : str, default="06-30"
        Last day of the season in 'mm-dd' format.

    Returns
    -------
    tuple[pandas.DataFrame, numpy.ndarray]
        A tuple of (seasons_df, season_ids) where seasons_df contains season metadata
        and season_ids is a float array with season IDs or NaN for out-of-season days.
    """
    if isinstance(time, xr.DataArray):
        dates = pd.DatetimeIndex(time.values)
    elif isinstance(time, np.ndarray):
        dates = pd.DatetimeIndex(time)
    else:
        dates = pd.DatetimeIndex(time)

    if len(dates) == 0:
        empty_df = pd.DataFrame(columns=["start", "end", "season_id", "season_label"])
        return empty_df, np.array([], dtype=float)

    start_month, start_day = _parse_mmdd(season_start, "season_start")
    end_month, end_day = _parse_mmdd(season_end, "season_end")

    crosses = (end_month < start_month) or (end_month == start_month and end_day < start_day)

    y_min = int(dates.year.min()) - 1
    y_max = int(dates.year.max()) + 1
    years = np.arange(y_min, y_max + 1)

    def _make_date_str(year: int, mmdd: str) -> str:
        """
        Format year and month-day string, adjusting leap day for non-leap years.

        Parameters
        ----------
        year : int
            Target calendar year.
        mmdd : str
            Month and day in MM-DD format.

        Returns
        -------
        str
            Date string formatted as YYYY-MM-DD.
        """
        if mmdd == "02-29" and not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            return f"{year}-02-28"
        return f"{year}-{mmdd}"

    starts = pd.to_datetime([_make_date_str(int(y), season_start) for y in years])
    ends = pd.to_datetime([_make_date_str(int(y) + int(crosses), season_end) for y in years])

    valid = starts <= ends
    seasons = pd.DataFrame({"start": starts[valid], "end": ends[valid]}).reset_index(drop=True)
    seasons["season_id"] = seasons.index + 1
    seasons["season_label"] = seasons["start"].dt.strftime("%Y") + "-" + seasons["end"].dt.strftime("%Y")

    start_arr: np.ndarray = np.asarray(seasons["start"].values, dtype="datetime64[ns]")
    end_arr: np.ndarray = np.asarray(seasons["end"].values, dtype="datetime64[ns]")
    sid_arr: np.ndarray = np.asarray(seasons["season_id"].values, dtype=float)
    date_arr: np.ndarray = np.asarray(dates.values, dtype="datetime64[ns]")

    idx = np.searchsorted(start_arr, date_arr, side="right") - 1

    in_bounds = (idx >= 0) & (idx < len(start_arr))
    within_end = np.zeros(len(dates), dtype=bool)
    if in_bounds.any():
        date_days = date_arr[in_bounds].astype("datetime64[D]")
        end_days = end_arr[idx[in_bounds]].astype("datetime64[D]")
        within_end[in_bounds] = date_days <= end_days

    in_season = in_bounds & within_end
    safe_idx = np.where(in_bounds, idx, 0)
    season_ids = np.where(in_season, sid_arr[safe_idx], np.nan)

    return seasons, season_ids
