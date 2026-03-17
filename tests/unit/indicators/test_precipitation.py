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

from earthkit.climate.indicators import precipitation

INDICATORS = [
    (precipitation.antecedent_precipitation_index, "antecedent_precipitation_index", {"val": "test"}),
    (precipitation.maximum_consecutive_dry_days, "maximum_consecutive_dry_days", {"val": "test"}),
    (
        precipitation.maximum_consecutive_wet_days,
        "maximum_consecutive_wet_days",
        {"thresh": "2 mm/day", "freq": "MS"},
    ),
    (precipitation.daily_pr_intensity, "daily_pr_intensity", {"thresh": "2 mm/day", "freq": "MS"}),
    (precipitation.cffwis_indices, "cffwis_indices", {"arg1": "val1"}),
    (precipitation.cold_and_dry_days, "cold_and_dry_days", {"arg1": "val1"}),
    (precipitation.cold_and_wet_days, "cold_and_wet_days", {"arg1": "val1"}),
    (precipitation.days_over_precip_doy_thresh, "days_over_precip_doy_thresh", {"arg1": "val1"}),
    (precipitation.days_over_precip_thresh, "days_over_precip_thresh", {"arg1": "val1"}),
    (precipitation.days_with_snow, "days_with_snow", {"arg1": "val1"}),
    (precipitation.drought_code, "drought_code", {"arg1": "val1"}),
    (precipitation.griffiths_drought_factor, "griffiths_drought_factor", {"arg1": "val1"}),
    (precipitation.duff_moisture_code, "duff_moisture_code", {"arg1": "val1"}),
    (precipitation.dry_days, "dry_days", {"arg1": "val1"}),
    (precipitation.dry_spell_frequency, "dry_spell_frequency", {"arg1": "val1"}),
    (precipitation.dry_spell_max_length, "dry_spell_max_length", {"arg1": "val1"}),
    (precipitation.dry_spell_total_length, "dry_spell_total_length", {"arg1": "val1"}),
    (precipitation.dryness_index, "dryness_index", {"arg1": "val1"}),
    (precipitation.mcarthur_forest_fire_danger_index, "mcarthur_forest_fire_danger_index", {"arg1": "val1"}),
    (precipitation.first_snowfall, "first_snowfall", {"arg1": "val1"}),
    (precipitation.fraction_over_precip_doy_thresh, "fraction_over_precip_doy_thresh", {"arg1": "val1"}),
    (precipitation.fraction_over_precip_thresh, "fraction_over_precip_thresh", {"arg1": "val1"}),
    (precipitation.high_precip_low_temp, "high_precip_low_temp", {"arg1": "val1"}),
    (precipitation.keetch_byram_drought_index, "keetch_byram_drought_index", {"arg1": "val1"}),
    (precipitation.last_snowfall, "last_snowfall", {"arg1": "val1"}),
    (precipitation.liquid_precip_ratio, "liquid_precip_ratio", {"arg1": "val1"}),
    (precipitation.liquid_precip_average, "liquid_precip_average", {"arg1": "val1"}),
    (precipitation.liquid_precip_accumulation, "liquid_precip_accumulation", {"arg1": "val1"}),
    (precipitation.max_n_day_precipitation_amount, "max_n_day_precipitation_amount", {"arg1": "val1"}),
    (precipitation.max_pr_intensity, "max_pr_intensity", {"arg1": "val1"}),
    (precipitation.precip_average, "precip_average", {"arg1": "val1"}),
    (precipitation.precip_accumulation, "precip_accumulation", {"arg1": "val1"}),
    (precipitation.rain_on_frozen_ground_days, "rain_on_frozen_ground_days", {"arg1": "val1"}),
    (precipitation.rain_season, "rain_season", {"arg1": "val1"}),
    (precipitation.rprctot, "rprctot", {"arg1": "val1"}),
    (precipitation.max_1day_precipitation_amount, "max_1day_precipitation_amount", {"arg1": "val1"}),
    (precipitation.snowfall_frequency, "snowfall_frequency", {"arg1": "val1"}),
    (precipitation.snowfall_intensity, "snowfall_intensity", {"arg1": "val1"}),
    (precipitation.solid_precip_average, "solid_precip_average", {"arg1": "val1"}),
    (precipitation.solid_precip_accumulation, "solid_precip_accumulation", {"arg1": "val1"}),
    (precipitation.warm_and_dry_days, "warm_and_dry_days", {"arg1": "val1"}),
    (precipitation.warm_and_wet_days, "warm_and_wet_days", {"arg1": "val1"}),
    (precipitation.water_cycle_intensity, "water_cycle_intensity", {"arg1": "val1"}),
    (precipitation.wet_precip_accumulation, "wet_precip_accumulation", {"arg1": "val1"}),
    (precipitation.wet_spell_frequency, "wet_spell_frequency", {"arg1": "val1"}),
    (precipitation.wet_spell_max_length, "wet_spell_max_length", {"arg1": "val1"}),
    (precipitation.wet_spell_total_length, "wet_spell_total_length", {"arg1": "val1"}),
    (precipitation.wetdays, "wetdays", {"arg1": "val1"}),
    (precipitation.wetdays_prop, "wetdays_prop", {"arg1": "val1"}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_precipitation_indicator(
    mocker: MockerFixture,
    dummy_precip_ds: xarray.Dataset,
    earthkit_fn: Callable,
    xclim_name: str,
    kwargs: Dict[str, Any],
):
    """Test that the earthkit function wraps the xclim function correctly."""
    xclim_func_name = xclim_name

    mock_path = f"xclim.indicators.atmos.{xclim_func_name}"

    mock_fn = mocker.patch(mock_path)

    ds_in = dummy_precip_ds

    # Call the earthkit function
    earthkit_fn(ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
