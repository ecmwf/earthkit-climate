# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import numpy as np
import pytest
import xarray as xr
from pytest_mock import MockerFixture

from earthkit.climate.api.wrapper import wrap_xclim_indicator


class MockEarthkitData:
    """Mock object for Earthkit input."""

    pass


@pytest.fixture
def mock_xclim_indicator(mocker: MockerFixture):
    """Creates a mock xclim indicator function."""
    mock_fn = mocker.MagicMock()
    # Setup return value as an xarray Dataset
    ds_out = xr.Dataset(
        {"out_var": (("time", "lat", "lon"), np.random.rand(10, 10, 10))},
        coords={"time": np.arange(10), "lat": np.arange(10), "lon": np.arange(10)},
    )
    mock_fn.return_value = ds_out
    mock_fn.__name__ = "mock_indicator"
    return mock_fn


def test_wrapper_call(mock_xclim_indicator, common_mocks):
    """Test that the wrapper calls the underlying xclim function."""
    wrapped_fn = wrap_xclim_indicator(mock_xclim_indicator)
    input_data = MockEarthkitData()

    mock_to_xr = common_mocks["mock_to_xr"]
    mock_ensure_units = common_mocks["mock_ensure_units"]
    mock_add_prov = common_mocks["mock_add_prov"]
    mock_to_ek = common_mocks["mock_to_ek"]
    object_ek = common_mocks["object_ek"]

    result = wrapped_fn(input_data, arg1="value1")

    # Check conversions called
    mock_to_xr.assert_called_once()

    # Check units called (dummy_precip_ds has 'pr', so ensure_units should be called)
    mock_ensure_units.assert_called()

    # Check xclim function called
    mock_xclim_indicator.assert_called_once()

    # Check provenance called
    mock_add_prov.assert_called_once()

    # Check output conversion
    mock_to_ek.assert_called_once()
    assert result is object_ek


def test_wrapper_units_conversion(mock_xclim_indicator, common_mocks):
    """Test that units are ensured for specific variables."""
    wrapped_fn = wrap_xclim_indicator(mock_xclim_indicator)
    input_data = MockEarthkitData()

    mock_to_xr = common_mocks["mock_to_xr"]
    mock_ensure_units = common_mocks["mock_ensure_units"]

    # Setup mock dataset with 'tas' and 'pr'
    ds_in = xr.Dataset({"tas": (("x"), [1]), "pr": (("x"), [1])})
    mock_to_xr.return_value = (ds_in, {})

    wrapped_fn(input_data)

    # Verify ensure_units called for both
    assert mock_ensure_units.call_count >= 2
