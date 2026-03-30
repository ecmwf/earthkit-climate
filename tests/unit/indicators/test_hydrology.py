# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from typing import Any, Callable, Dict

import pytest
import xarray
from pytest_mock import MockerFixture

from earthkit.climate.indicators.land import hydrology

INDICATORS = [
    (hydrology.base_flow_index, "base_flow_index", {"val": "test"}),
    (hydrology.doy_qmax, "doy_qmax", {"val": "test"}),
    (hydrology.doy_qmin, "doy_qmin", {"val": "test"}),
    (hydrology.high_flow_frequency, "high_flow_frequency", {"val": "test"}),
    (hydrology.low_flow_frequency, "low_flow_frequency", {"val": "test"}),
    (hydrology.rb_flashiness_index, "rb_flashiness_index", {"val": "test"}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_hydrology_indicator(
    mocker: MockerFixture,
    dummy_discharge_ds: xarray.Dataset,
    earthkit_fn: Callable,
    xclim_name: str,
    kwargs: Dict[str, Any],
):
    """Test that the earthkit function wraps the xclim function correctly."""
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
