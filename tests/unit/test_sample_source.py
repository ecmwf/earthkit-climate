# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import earthkit.data as ekd
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from earthkit.climate._sample_source import SampleSource, generate_sample_dataset


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


def test_sample_source_fusarium_input_timeseries() -> None:
    """
    Test SampleSource with fusarium-input-timeseries dataset and to_dataframe.

    Returns
    -------
    None
    """
    src = SampleSource("fusarium-input-timeseries")
    ds = src.to_xarray()
    assert isinstance(ds, xr.Dataset)
    assert set(ds.data_vars) == {"tas", "hurs", "pr"}
    assert ds.sizes == {"time": 731}
    assert float(ds["hurs"].sel(time="2020-06-10")) == 95.0
    assert float(ds["pr"].sel(time="2020-06-10")) == 1.0
    assert float(ds["tas"].sel(time="2020-06-25")) == 31.0
    assert float(ds["hurs"].sel(time="2021-06-01")) == 85.0
    assert float(ds["pr"].sel(time="2021-06-02")) == 0.0

    df = src.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["tas", "hurs", "pr"]
    assert len(df) == 731

    # Verify through earthkit-data from_source plugin
    src_plugin = ekd.from_source("earthkit-climate-sample", "fusarium-input-timeseries")
    df_plugin = src_plugin.to_pandas()
    assert isinstance(df_plugin, pd.DataFrame)
    assert len(df_plugin) == 731
