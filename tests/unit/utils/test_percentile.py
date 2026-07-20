# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from earthkit.climate.utils.percentile import get_percentile


def test_get_percentile_yearly_expands_to_dayofyear(daily_temperature_ds) -> None:
    """
    Test that yearly percentile calculation expands to a daily (dayofyear) climatology.

    When frequency is None, the percentile is computed over the total timeseries, so
    the resulting array should be filled with a single constant value.
    """
    out = get_percentile(daily_temperature_ds, "tas", percentile=90, frequency=None)

    # Expect only dayofyear dimension (1..365 for non-leap year 2001)
    assert set(out.dims) == {"dayofyear"}
    assert out.sizes["dayofyear"] == 365
    assert "tas" in out

    # Values should be constant per year since YS groups whole time
    q = np.quantile(daily_temperature_ds["tas"].values, 0.9)
    sample_days = [1, 100, 200, 365]
    vals = out["tas"].sel(dayofyear=sample_days).values
    assert np.allclose(vals, q)


def test_get_percentile_monthly_constant_within_months(daily_temperature_ds) -> None:
    """
    Test that monthly percentile results are constant within each month.

    The output keeps a daily dayofyear coordinate, but percentile values are
    constant for all days belonging to the same calendar month.
    """
    out = get_percentile(daily_temperature_ds, "tas", percentile=50, frequency="month")

    # Still daily resolution with dayofyear coordinate
    assert set(out.dims) == {"dayofyear"}

    # For two days within the same month, values should be identical
    jan_days = [1, 15, 31]
    jan_vals = out["tas"].sel(dayofyear=jan_days).values
    assert np.allclose(jan_vals, jan_vals[0])

    # Compare one January day and one February day; likely different
    feb_day = 40  # Feb 9 in non-leap year
    assert not np.isclose(out["tas"].sel(dayofyear=1).item(), out["tas"].sel(dayofyear=feb_day).item())


def test_get_percentile_seasonal_qs_dec(daily_temperature_ds) -> None:
    """
    Test that seasonal percentile is constant within a season.

    For example, January and February belong to DJF, so their percentile
    values should be identical, while other seasons (e.g., April) differ.
    """
    out = get_percentile(daily_temperature_ds, "tas", percentile=75, frequency="season")

    assert set(out.dims) == {"dayofyear"}

    # Identify a few days that belong to the same season (DJF: Jan 15 and Feb 15)
    d1 = 15
    d2 = 46  # approx Feb 15
    assert np.isclose(out["tas"].sel(dayofyear=d1).item(), out["tas"].sel(dayofyear=d2).item())

    # And a day from a different season (e.g., April ~ day 100) should likely differ
    d3 = 100
    assert not np.isclose(out["tas"].sel(dayofyear=d1).item(), out["tas"].sel(dayofyear=d3).item())
