# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pytest_mock import MockerFixture


@pytest.fixture
def dummy_precip_ds() -> xr.Dataset:
    """Simple constant precipitation dataset."""
    time = xr.cftime_range(
        start="2001-01-01", end="2001-01-10", freq="D", calendar="noleap"
    ).to_datetimeindex()
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
    time = xr.cftime_range(
        start="2000-01-01", end="2001-12-31", freq="D", calendar="noleap"
    ).to_datetimeindex()
    data = rng.normal(loc=10.0, scale=2.0, size=time.size)
    ds = xr.Dataset({"tas": ("time", data)}, coords={"time": time})
    return ds


@pytest.fixture
def common_mocks(mocker: MockerFixture, dummy_precip_ds: xr.Dataset) -> dict:
    """
    Fixture that sets up common mocks used across indicators tests.

    Parameters
    ----------
    mocker : MockerFixture
        Pytest-mock fixture used to create and manage mocks.
    dummy_precip_ds : xr.Dataset
        The dummy precipitation dataset fixture.

    Returns
    -------
    dict[str, Any]+
        Dictionary with references to key mock objects for assertions.
    """
    object_ek = object()

    mock_to_xr = mocker.patch(
        "earthkit.climate.utils.conversions.to_xarray_dataset",
        return_value=(dummy_precip_ds, {"earthkit_internal": {}}),
    )

    mock_ensure_units = mocker.patch(
        "earthkit.climate.utils.units.ensure_units",
        side_effect=lambda ds, var, units, strict=False: ds.assign_attrs({"ensured": True}),
    )

    mock_add_prov = mocker.patch(
        "earthkit.climate.utils.provenance.add_indicator_provenance",
        side_effect=lambda md, *a, **k: {**md, "prov": True},
    )

    mock_to_ek = mocker.patch(
        "earthkit.climate.utils.conversions.to_earthkit_field",
        return_value=object_ek,
    )

    return {
        "mock_to_xr": mock_to_xr,
        "mock_ensure_units": mock_ensure_units,
        "mock_add_prov": mock_add_prov,
        "mock_to_ek": mock_to_ek,
        "object_ek": object_ek,
    }
