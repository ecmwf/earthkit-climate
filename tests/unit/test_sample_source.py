# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import pytest
import xarray as xr

from earthkit.climate.sample_source import SampleSource


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
