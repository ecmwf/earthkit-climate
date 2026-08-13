# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest
import xarray as xr

import earthkit.climate as ekc


@pytest.mark.parametrize("frequency", ["season", "month", "dayofyear"])
def test_upsample_scalar_fails_without_fallback_axis(frequency) -> None:
    da = xr.DataArray(5.0, name="tas")
    with pytest.raises(ValueError, match="fallback_axis"):
        ekc.utils.climatology.upsample(da, frequency=frequency)


def test_upsample_scalar_to_dayofyear_with_fallback_axis() -> None:
    da = xr.DataArray(5.0, name="tas")
    out = ekc.utils.climatology.upsample(da, frequency="dayofyear", fallback_axis=0)
    assert out.name == "tas"
    assert set(out.dims) == {"dayofyear"}
    assert out.sizes["dayofyear"] == 366
    # Values should be constant over the whole year
    np.testing.assert_allclose(out.values, da.values)


def test_upsample_scalar_to_month_with_fallback_axis() -> None:
    da = xr.DataArray(5.0, name="tas")
    out = ekc.utils.climatology.upsample(da, frequency="month", fallback_axis=0)
    assert out.name == "tas"
    assert set(out.dims) == {"month"}
    assert out.sizes["month"] == 12
    # Values should be constant over the whole year
    np.testing.assert_allclose(out.values, da.values)


def test_upsample_scalar_to_season_with_fallback_axis() -> None:
    da = xr.DataArray(5.0, name="tas")
    out = ekc.utils.climatology.upsample(da, frequency="season", fallback_axis=0)
    assert out.name == "tas"
    assert set(out.dims) == {"season"}
    assert out.sizes["season"] == 4
    # Values should be constant over the whole year
    np.testing.assert_allclose(out.values, da.values)


def test_upsample_month_to_dayofyear_constant_within_months(daily_temperature_ds) -> None:
    """
    Test that monthly percentile results are constant within each month.

    The output keeps a daily dayofyear coordinate, but percentile values are
    constant for all days belonging to the same calendar month.
    """
    ekt = pytest.importorskip("earthkit.transforms")
    per = ekt.climatology.percentiles(daily_temperature_ds["tas"], p=50, frequency="month")
    out = ekc.utils.climatology.upsample(per, frequency="dayofyear").compute()
    assert out.name == "tas"
    assert set(out.dims) == {"dayofyear", "percentile"}
    assert out.sizes["dayofyear"] == 366
    # For two days within the same month, values should be identical
    jan_days = [1, 15, 31]
    jan_vals = out.sel(dayofyear=jan_days).values
    assert np.allclose(jan_vals, jan_vals[0])
    # Compare one January day and one February day; likely different
    feb_day = 40  # Feb 9 in non-leap year
    assert not np.isclose(out.sel(dayofyear=1).item(), out.sel(dayofyear=feb_day).item())


def test_upsample_season_to_dayofyear_constant_within_season(daily_temperature_ds) -> None:
    """
    Test that seasonal percentile is constant within a season.

    For example, January and February belong to DJF, so their percentile
    values should be identical, while other seasons (e.g., April) differ.
    """
    ekt = pytest.importorskip("earthkit.transforms")
    per = ekt.climatology.percentiles(daily_temperature_ds["tas"], p=75, frequency="season")
    out = ekc.utils.climatology.upsample(per, frequency="dayofyear").compute()
    assert out.name == "tas"
    assert set(out.dims) == {"dayofyear", "percentile"}
    assert out.sizes["dayofyear"] == 366
    # Identify a few days that belong to the same season (DJF: Jan 15 and Feb 15)
    d1 = 15
    d2 = 46  # approx Feb 15
    assert np.isclose(out.sel(dayofyear=d1).item(), out.sel(dayofyear=d2).item())
    # And a day from a different season (e.g., April ~ day 100) should likely differ
    d3 = 100
    assert not np.isclose(out.sel(dayofyear=d1).item(), out.sel(dayofyear=d3).item())


def test_rolling_percentiles_dayofyear_quacks_like_ekt_percentiles(daily_temperature_ds) -> None:
    ekt = pytest.importorskip("earthkit.transforms")
    ref = ekt.climatology.percentiles(daily_temperature_ds["tas"], p=50.0, frequency="dayofyear")
    out = ekc.utils.climatology.rolling_percentiles(daily_temperature_ds["tas"], p=50.0, frequency="dayofyear")
    assert out.name == ref.name
    # Same dimension names, no requirement on order (for now)
    assert set(out.dims) == set(ref.dims)
    # Same calendar
    np.testing.assert_array_equal(out.coords["dayofyear"].values, ref.coords["dayofyear"].values)
    # Not the same values
    assert not np.allclose(out.values, ref.values)
