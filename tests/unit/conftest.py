# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr


@pytest.fixture
def dummy_precip_ds() -> xr.Dataset:
    """Simple constant precipitation dataset."""
    time = xr.date_range(start="2001-01-01", end="2001-01-10", freq="D", use_cftime=True).to_datetimeindex(
        time_unit="us"
    )
    ds = xr.Dataset(
        {"pr": ("time", [1.0] * len(time))},
        coords={"time": time},
    )
    ds["pr"].attrs["units"] = "kg m-2 s-1"
    return ds


@pytest.fixture
def dummy_temp_ds() -> xr.Dataset:
    """Return a simple temperature dataset with time coordinate and degC units."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {
            "tasmax": ("time", [20.0, 21.0, 19.0]),
            "tasmin": ("time", [10.0, 9.0, 11.0]),
            "tas": ("time", [15.0, 15.0, 15.0]),
        },
        coords={"time": time},
    )
    for var in ds.data_vars:
        ds[var].attrs["units"] = "degC"
    return ds


@pytest.fixture
def daily_temperature_ds() -> xr.Dataset:
    """Synthetic daily temperature dataset for percentile and grouping tests."""
    rng = np.random.default_rng(0)
    time = xr.date_range(start="2000-01-01", end="2001-12-31", freq="D", use_cftime=True).to_datetimeindex(
        time_unit="us"
    )
    data = rng.normal(loc=10.0, scale=2.0, size=time.size)
    ds = xr.Dataset({"tas": ("time", data)}, coords={"time": time})
    return ds


@pytest.fixture
def dummy_wind_ds() -> xr.Dataset:
    """Simple wind dataset."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {
            "sfcWind": ("time", [2.0, 5.0, 3.0]),
            "sfcWindmax": ("time", [4.0, 8.0, 6.0]),
        },
        coords={"time": time},
    )
    for var in ds.data_vars:
        ds[var].attrs["units"] = "m s-1"
    return ds


@pytest.fixture
def dummy_synoptic_ds() -> xr.Dataset:
    """Simple synoptic dataset."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {"ua": (("time", "lat", "lon"), np.ones((len(time), 2, 2)))},
        coords={"time": time, "lat": [45, 46], "lon": [5, 6]},
    )
    ds["ua"].attrs["units"] = "m s-1"
    return ds


@pytest.fixture
def dummy_snow_ds() -> xr.Dataset:
    """Simple snow dataset."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {
            "snw": ("time", [10.0, 15.0, 12.0]),
            "snd": ("time", [0.1, 0.15, 0.12]),
        },
        coords={"time": time},
    )
    ds["snw"].attrs["units"] = "kg m-2"
    ds["snd"].attrs["units"] = "m"
    return ds


@pytest.fixture
def dummy_discharge_ds() -> xr.Dataset:
    """Simple discharge dataset."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {"q": ("time", [100.0, 120.0, 110.0])},
        coords={"time": time},
    )
    ds["q"].attrs["units"] = "m3 s-1"
    return ds


@pytest.fixture
def dummy_sea_ice_ds() -> xr.Dataset:
    """Simple sea ice dataset."""
    time = pd.date_range("2000-01-01", periods=3)
    ds = xr.Dataset(
        {"sic": ("time", [0.8, 0.75, 0.85])},
        coords={"time": time},
    )
    ds["sic"].attrs["units"] = "1"
    return ds
