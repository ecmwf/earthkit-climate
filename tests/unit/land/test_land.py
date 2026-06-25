# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Tests for land indicators."""

from typing import Any, Callable

import pytest
import xarray
from pytest_mock import MockerFixture

from earthkit.climate.indicators import land

INDICATORS = [
    (land.flow_index, "flow_index", {"val": "test"}),
    (land.standardized_groundwater_index, "standardized_groundwater_index", {"val": "test"}),
    (land.standardized_streamflow_index, "standardized_streamflow_index", {"val": "test"}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_land_indicator(
    mocker: MockerFixture,
    dummy_discharge_ds: xarray.Dataset,
    earthkit_fn: Callable[..., Any],
    xclim_name: str,
    kwargs: dict[str, Any],
) -> None:
    """Test that the earthkit function wraps the xclim function correctly.

    Parameters
    ----------
    mocker : MockerFixture
        Mocking utility from pytest-mock.
    dummy_discharge_ds : xarray.Dataset
        A dummy dataset containing discharge variables.
    earthkit_fn : Callable[..., Any]
        The earthkit wrapper function being tested.
    xclim_name : str
        The name of the underlying xclim function.
    kwargs : dict[str, Any]
        Arguments to pass to the function call.

    Returns
    -------
    None
    """
    xclim_func_name = xclim_name

    mock_path = f"xclim.indicators.land.{xclim_func_name}"

    mock_fn = mocker.patch(mock_path)

    ds_in = dummy_discharge_ds

    # Call the earthkit function
    earthkit_fn(ds=ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
