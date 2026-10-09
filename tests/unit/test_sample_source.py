# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest
import xarray as xr

from earthkit.climate.sample_source import SampleSource, generate_sample_dataset


def test_generate_sample_dataset_defaults():
    ds = generate_sample_dataset("2020-12-30", "2021-01-02")

    assert ds.sizes == {"time": 4}
    assert list(ds.data_vars) == ["tas", "hurs", "pr"]
    np.testing.assert_array_equal(
        ds["time"].dt.strftime("%Y-%m-%d"),
        ["2020-12-30", "2020-12-31", "2021-01-01", "2021-01-02"],
    )
    np.testing.assert_array_equal(ds["tas"], np.full(4, 20.0))
    np.testing.assert_array_equal(ds["hurs"], np.full(4, 70.0))
    np.testing.assert_array_equal(ds["pr"], np.full(4, 0.0))

    assert ds["tas"].attrs == {
        "units": "degC",
        "standard_name": "air_temperature",
        "cell_methods": "time: mean within days",
    }
    assert ds["hurs"].attrs == {
        "units": "%",
        "standard_name": "relative_humidity",
        "cell_methods": "time: mean within days",
    }
    assert ds["pr"].attrs == {
        "units": "mm/day",
        "standard_name": "precipitation_flux",
        "cell_methods": "time: mean within days",
    }


def test_generate_sample_dataset_values():
    ds = generate_sample_dataset(
        "2020-01-01",
        "2020-01-02",
        tas_value=18.5,
        hurs_value=82.0,
        pr_value=1.25,
    )

    np.testing.assert_array_equal(ds["tas"], np.full(2, 18.5))
    np.testing.assert_array_equal(ds["hurs"], np.full(2, 82.0))
    np.testing.assert_array_equal(ds["pr"], np.full(2, 1.25))


def test_sample_source_with_valid_name() -> None:
    """
    Test SampleSource initialization with valid remote dataset name.

    Returns
    -------
    None
    """
    with pytest.warns(UserWarning):
        SampleSource("tasmax_ACCESS-CM2_historical_reference")


def test_sample_source_with_invalid_name() -> None:
    """
    Test SampleSource initialization with invalid dataset name raises ValueError.

    Returns
    -------
    None
    """
    with pytest.raises(ValueError):
        SampleSource("foobar")


def test_sample_source_synthetic_daily_temperature() -> None:
    """
    Test SampleSource with synthetic daily temperature dataset.

    Returns
    -------
    None
    """
    src = SampleSource("synthetic-daily-temperature")
    da = src.to_xarray()
    assert isinstance(da, xr.DataArray)
    assert da.name == "tasmax"
    assert da.attrs["units"] == "K"
    assert da.attrs["standard_name"] == "air_temperature"
    assert da.attrs["cell_methods"] == "time: maximum"


def test_sample_source_synthetic_daily_dask_temperature() -> None:
    """
    Test SampleSource with synthetic daily dask-backed temperature dataset.

    Returns
    -------
    None
    """
    src = SampleSource("synthetic-daily-dask-temperature")
    da = src.to_xarray()
    assert isinstance(da, xr.DataArray)
    assert da.name == "tasmax"
    assert da.chunks is not None
    assert da.attrs["units"] == "K"
    assert da.attrs["standard_name"] == "air_temperature"
    assert da.attrs["cell_methods"] == "time: maximum"


def test_sample_source_synthetic_daily_station_temperature() -> None:
    """
    Test SampleSource with synthetic station daily temperature dataset.

    Returns
    -------
    None
    """
    src = SampleSource("synthetic-daily-station-temperature")
    da = src.to_xarray()
    assert isinstance(da, xr.DataArray)
    assert da.name == "tasmax"
    assert "station_id" in da.dims
    assert "time" in da.dims
    assert "lat" in da.coords
    assert "lon" in da.coords
    assert "height" in da.coords
    assert len(da.coords["station_id"]) == 5
    assert da.attrs["units"] == "K"
    assert da.attrs["standard_name"] == "air_temperature"
    assert da.attrs["cell_methods"] == "time: maximum"
