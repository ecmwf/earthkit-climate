# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Tests for synoptic indicators."""

from typing import Any, Callable

import pytest
import xarray
from pytest_mock import MockerFixture

from earthkit.climate.atmos import synoptic

INDICATORS = [
    (synoptic.jetstream_metric_woollings, "jetstream_metric_woollings"),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name", INDICATORS)
def test_synoptic_indicator(
    mocker: MockerFixture,
    dummy_synoptic_ds: xarray.Dataset,
    earthkit_fn: Callable[..., Any],
    xclim_name: str,
) -> None:
    """Test that the earthkit function wraps the xclim function correctly.

    Parameters
    ----------
    mocker : MockerFixture
        Mocking utility from pytest-mock.
    dummy_synoptic_ds : xarray.Dataset
        A dummy dataset containing synoptic variables.
    earthkit_fn : Callable[..., Any]
        The earthkit wrapper function being tested.
    xclim_name : str
        The name of the underlying xclim function.

    Returns
    -------
    None
    """
    xclim_func_name = xclim_name

    mock_path = f"xclim.indicators.atmos.{xclim_func_name}"

    mock_fn = mocker.patch(mock_path)

    # Use a dummy argument dictionary
    kwargs = {"arg1": "val1", "arg2": 2}

    ds_in = dummy_synoptic_ds

    # Call the earthkit function
    earthkit_fn(ds=ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
