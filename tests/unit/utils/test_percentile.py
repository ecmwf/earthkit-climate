# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import numpy as np
import pytest

from earthkit.climate.utils.percentile import get_percentile, pandas_offset2time_component


@pytest.mark.parametrize(
    "alias,component",
    [
        ("YS", "year"),
        ("MS", "month"),
        ("QS-DEC", "season"),
    ],
)
def test_pandas_offset2time_component_supported(alias: str, component: str) -> None:
    """Test that supported pandas offset aliases map to the expected time components."""
    assert pandas_offset2time_component(alias) == component


def test_get_percentile_yearly_expands_to_dayofyear(daily_temperature_ds) -> None:
    """
    Test that yearly percentile calculation expands to a daily (dayofyear) climatology.

    When frequency is 'YS', the percentile is computed over each full year, so
    the resulting array should have one value per day of the year that is constant
    within that year.
    """
    out = get_percentile(daily_temperature_ds, "tas", percentile=90, freq="YS")

    # Expect only dayofyear dimension (1..365 for non-leap year 2001)
    assert set(out.dims) == {"dayofyear"}
    assert out.dims["dayofyear"] == 365
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
    out = get_percentile(daily_temperature_ds, "tas", percentile=50, freq="MS")

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
    Test that seasonal percentile (QS-DEC) is constant within a season.

    For example, January and February belong to DJF, so their percentile
    values should be identical, while other seasons (e.g., April) differ.
    """
    out = get_percentile(daily_temperature_ds, "tas", percentile=75, freq="QS-DEC")

    assert set(out.dims) == {"dayofyear"}

    # Identify a few days that belong to the same season (DJF: Jan 15 and Feb 15)
    d1 = 15
    d2 = 46  # approx Feb 15
    assert np.isclose(out["tas"].sel(dayofyear=d1).item(), out["tas"].sel(dayofyear=d2).item())

    # And a day from a different season (e.g., April ~ day 100) should likely differ
    d3 = 100
    assert not np.isclose(out["tas"].sel(dayofyear=d1).item(), out["tas"].sel(dayofyear=d3).item())
