# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0


"""Tests for land indicators."""

from typing import Any, Callable

import pytest
import xarray as xr
from pytest_mock import MockerFixture

from earthkit.climate.indicators import xarray as indicators

INDICATORS = [
    (indicators.flow_index, "flow_index", {"val": "test"}),
    (indicators.standardized_groundwater_index, "standardized_groundwater_index", {"val": "test"}),
    (indicators.standardized_streamflow_index, "standardized_streamflow_index", {"val": "test"}),
    (indicators.base_flow_index, "base_flow_index", {"val": "test"}),
    (indicators.doy_qmax, "doy_qmax", {"val": "test"}),
    (indicators.doy_qmin, "doy_qmin", {"val": "test"}),
    (indicators.high_flow_frequency, "high_flow_frequency", {"val": "test"}),
    (indicators.low_flow_frequency, "low_flow_frequency", {"val": "test"}),
    (indicators.rb_flashiness_index, "rb_flashiness_index", {"val": "test"}),
    (indicators.blowing_snow, "blowing_snow", {"val": "test"}),
    (indicators.holiday_snow_and_snowfall_days, "holiday_snow_and_snowfall_days", {"val": "test"}),
    (indicators.holiday_snow_days, "holiday_snow_days", {"val": "test"}),
    (indicators.snd_days_above, "snd_days_above", {"val": "test"}),
    (indicators.snd_max_doy, "snd_max_doy", {"val": "test"}),
    (indicators.snd_season_end, "snd_season_end", {"val": "test"}),
    (indicators.snd_season_length, "snd_season_length", {"val": "test"}),
    (indicators.snd_season_start, "snd_season_start", {"val": "test"}),
    (indicators.snd_storm_days, "snd_storm_days", {"val": "test"}),
    (indicators.snow_depth, "snow_depth", {"val": "test"}),
    (indicators.snow_melt_we_max, "snow_melt_we_max", {"val": "test"}),
    (indicators.snw_days_above, "snw_days_above", {"val": "test"}),
    (indicators.snw_max, "snw_max", {"val": "test"}),
    (indicators.snw_max_doy, "snw_max_doy", {"val": "test"}),
    (indicators.snw_season_end, "snw_season_end", {"val": "test"}),
    (indicators.snw_season_length, "snw_season_length", {"val": "test"}),
    (indicators.snw_season_start, "snw_season_start", {"val": "test"}),
    (indicators.snw_storm_days, "snw_storm_days", {"val": "test"}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_land_indicator(
    mocker: MockerFixture,
    dummy_discharge_ds: xr.Dataset,
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
