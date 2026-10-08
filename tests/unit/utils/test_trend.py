# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from earthkit.climate.utils import linear_trend


def test_linear_trend_detects_datetime_time_and_sets_metadata():
    time = pd.date_range("2000-01-01", periods=4, freq="YS")
    data = xr.DataArray([0.0, 2.0, 4.0, 6.0], dims="time", coords={"time": time}, name="tas")
    data.attrs = {"units": "degC", "standard_name": "air_temperature"}

    result = linear_trend(data)

    assert result.name == "tas_linear_trend"
    assert result.ndim == 0
    assert result.attrs["units"] == "degC yr-1"
    assert result.attrs["long_name"] == "Linear trend of tas"
    assert "standard_name" not in result.attrs
    assert result.item() == pytest.approx(2.0, abs=0.002)


def test_linear_trend_handles_dataset_and_named_time_axis():
    data = xr.Dataset(
        {"tas": ("forecast", [1.0, 3.0, 5.0])},
        coords={
            "valid_time": (
                "forecast",
                pd.date_range("2000-01-01", periods=3, freq="2YS"),
                {"standard_name": "time"},
            )
        },
    )
    data["tas"].attrs["units"] = "K"

    result = linear_trend(data)

    assert list(result.data_vars) == ["tas_linear_trend"]
    assert result["tas_linear_trend"].attrs["units"] == "K yr-1"
    assert result["tas_linear_trend"].item() == pytest.approx(1.0, abs=0.002)


def test_linear_trend_ignores_missing_values_and_handles_spatial_dims():
    data = xr.DataArray(
        [[0.0, 1.0], [2.0, np.nan], [4.0, np.nan]],
        dims=("time", "location"),
        coords={"time": pd.date_range("2000-01-01", periods=3, freq="YS")},
        name="value",
    )

    result = linear_trend(data, dim="time")

    np.testing.assert_allclose(result.values, [2.0, np.nan], equal_nan=True)


def test_linear_trend_requires_unambiguous_time_axis():
    data = xr.DataArray(np.ones((2, 2)), dims=("first", "second"))

    with pytest.raises(ValueError, match="unable to detect"):
        linear_trend(data)


def test_linear_trend_can_return_p_values():
    data = xr.DataArray(
        [1.0, 2.0, 1.0, 4.0, 5.0],
        dims="time",
        coords={"time": pd.date_range("2000-01-01", periods=5, freq="YS")},
        name="tas",
    )

    result = linear_trend(data)
    trend, p_values = linear_trend(data, return_p_values=True)

    assert isinstance(result, xr.DataArray)
    assert isinstance(trend, xr.DataArray)
    assert isinstance(p_values, xr.DataArray)
    assert trend.name == "tas_linear_trend"
    assert p_values.name == "tas_p_value"
    assert p_values.attrs["units"] == "1"
    assert trend.item() == pytest.approx(1.0)
    assert p_values.item() == pytest.approx(0.054913, rel=1e-4)


def test_dataset_linear_trend_returns_dataset_p_values():
    data = xr.Dataset(
        {"tas": ("time", [1.0, 2.0, 3.0, 4.0])},
        coords={"time": pd.date_range("2000-01-01", periods=4, freq="YS")},
    )

    trends, p_values = linear_trend(data, return_p_values=True)

    assert list(trends.data_vars) == ["tas_linear_trend"]
    assert list(p_values.data_vars) == ["tas_p_value"]
    assert p_values["tas_p_value"].item() == pytest.approx(0.0, abs=1e-12)


def test_linear_trend_requires_decoded_datetime_coordinate():
    numeric_time = xr.DataArray([1.0, 2.0, 3.0], dims="time", coords={"time": [0.0, 1.0, 2.0]})
    missing_time = xr.DataArray([1.0, 2.0, 3.0], dims="time")

    with pytest.raises(ValueError, match="decoded datetime"):
        linear_trend(numeric_time, dim="time")
    with pytest.raises(ValueError, match="decoded datetime"):
        linear_trend(missing_time, dim="time")
