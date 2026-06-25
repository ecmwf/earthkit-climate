# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Tests for snow indicators."""

from typing import Any, Callable

import pytest
import xarray
from pytest_mock import MockerFixture

from earthkit.climate.indicators import snow

INDICATORS = [
    (snow.blowing_snow, "blowing_snow", {"val": "test"}),
    (snow.holiday_snow_and_snowfall_days, "holiday_snow_and_snowfall_days", {"val": "test"}),
    (snow.holiday_snow_days, "holiday_snow_days", {"val": "test"}),
    (snow.snd_days_above, "snd_days_above", {"val": "test"}),
    (snow.snd_max_doy, "snd_max_doy", {"val": "test"}),
    (snow.snd_season_end, "snd_season_end", {"val": "test"}),
    (snow.snd_season_length, "snd_season_length", {"val": "test"}),
    (snow.snd_season_start, "snd_season_start", {"val": "test"}),
    (snow.snd_storm_days, "snd_storm_days", {"val": "test"}),
    (snow.snow_depth, "snow_depth", {"val": "test"}),
    (snow.snow_melt_we_max, "snow_melt_we_max", {"val": "test"}),
    (snow.snw_days_above, "snw_days_above", {"val": "test"}),
    (snow.snw_max, "snw_max", {"val": "test"}),
    (snow.snw_max_doy, "snw_max_doy", {"val": "test"}),
    (snow.snw_season_end, "snw_season_end", {"val": "test"}),
    (snow.snw_season_length, "snw_season_length", {"val": "test"}),
    (snow.snw_season_start, "snw_season_start", {"val": "test"}),
    (snow.snw_storm_days, "snw_storm_days", {"val": "test"}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_snow_indicator(
    mocker: MockerFixture,
    dummy_snow_ds: xarray.Dataset,
    earthkit_fn: Callable[..., Any],
    xclim_name: str,
    kwargs: dict[str, Any],
) -> None:
    """Test that the earthkit function wraps the xclim function correctly.

    Parameters
    ----------
    mocker : MockerFixture
        Mocking utility from pytest-mock.
    dummy_snow_ds : xarray.Dataset
        A dummy dataset containing snow variables.
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

    ds_in = dummy_snow_ds

    # Call the earthkit function
    earthkit_fn(ds=ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
