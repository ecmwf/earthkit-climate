# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from typing import Callable

import pytest
import xarray
from pytest_mock import MockerFixture

from earthkit.climate.indicators import temperature

INDICATORS = [
    (temperature.australian_hardiness_zones, "australian_hardiness_zones"),
    (temperature.biologically_effective_degree_days, "biologically_effective_degree_days"),
    (temperature.cold_spell_days, "cold_spell_days"),
    (temperature.cold_spell_duration_index, "cold_spell_duration_index"),
    (temperature.cold_spell_frequency, "cold_spell_frequency"),
    (temperature.cold_spell_max_length, "cold_spell_max_length"),
    (temperature.cold_spell_total_length, "cold_spell_total_length"),
    (temperature.consecutive_frost_days, "consecutive_frost_days"),
    (temperature.maximum_consecutive_frost_free_days, "maximum_consecutive_frost_free_days"),
    (temperature.cool_night_index, "cool_night_index"),
    (temperature.cooling_degree_days, "cooling_degree_days"),
    (temperature.cooling_degree_days_approximation, "cooling_degree_days_approximation"),
    (temperature.corn_heat_units, "corn_heat_units"),
    (temperature.chill_portions, "chill_portions"),
    (temperature.chill_units, "chill_units"),
    (temperature.degree_days_exceedance_date, "degree_days_exceedance_date"),
    (temperature.daily_freezethaw_cycles, "daily_freezethaw_cycles"),
    (temperature.daily_temperature_range, "daily_temperature_range"),
    (temperature.max_daily_temperature_range, "max_daily_temperature_range"),
    (temperature.daily_temperature_range_variability, "daily_temperature_range_variability"),
    (temperature.extreme_temperature_range, "extreme_temperature_range"),
    (temperature.fire_season, "fire_season"),
    (temperature.first_day_tg_above, "first_day_tg_above"),
    (temperature.first_day_tg_below, "first_day_tg_below"),
    (temperature.first_day_tn_above, "first_day_tn_above"),
    (temperature.first_day_tn_below, "first_day_tn_below"),
    (temperature.first_day_tx_above, "first_day_tx_above"),
    (temperature.first_day_tx_below, "first_day_tx_below"),
    (temperature.freezethaw_spell_frequency, "freezethaw_spell_frequency"),
    (temperature.freezethaw_spell_max_length, "freezethaw_spell_max_length"),
    (temperature.freezethaw_spell_mean_length, "freezethaw_spell_mean_length"),
    (temperature.freezing_degree_days, "freezing_degree_days"),
    (temperature.freshet_start, "freshet_start"),
    (temperature.frost_days, "frost_days"),
    (temperature.frost_free_season_end, "frost_free_season_end"),
    (temperature.frost_free_season_length, "frost_free_season_length"),
    (temperature.frost_free_season_start, "frost_free_season_start"),
    (temperature.frost_free_spell_max_length, "frost_free_spell_max_length"),
    (temperature.frost_season_length, "frost_season_length"),
    (temperature.growing_degree_days, "growing_degree_days"),
    (temperature.growing_season_end, "growing_season_end"),
    (temperature.growing_season_length, "growing_season_length"),
    (temperature.growing_season_start, "growing_season_start"),
    (temperature.heat_spell_frequency, "heat_spell_frequency"),
    (temperature.heat_spell_max_length, "heat_spell_max_length"),
    (temperature.heat_spell_total_length, "heat_spell_total_length"),
    (temperature.heat_wave_frequency, "heat_wave_frequency"),
    (temperature.heat_wave_index, "heat_wave_index"),
    (temperature.heat_wave_max_length, "heat_wave_max_length"),
    (temperature.heat_wave_total_length, "heat_wave_total_length"),
    (temperature.heating_degree_days, "heating_degree_days"),
    (temperature.heating_degree_days_approximation, "heating_degree_days_approximation"),
    (temperature.hot_days, "hot_days"),
    (temperature.hot_spell_frequency, "hot_spell_frequency"),
    (temperature.hot_spell_max_length, "hot_spell_max_length"),
    (temperature.hot_spell_max_magnitude, "hot_spell_max_magnitude"),
    (temperature.hot_spell_total_length, "hot_spell_total_length"),
    (temperature.huglin_index, "huglin_index"),
    (temperature.ice_days, "ice_days"),
    (temperature.last_spring_frost, "last_spring_frost"),
    (temperature.late_frost_days, "late_frost_days"),
    (temperature.latitude_temperature_index, "latitude_temperature_index"),
    (temperature.maximum_consecutive_warm_days, "maximum_consecutive_warm_days"),
    (temperature.tg10p, "tg10p"),
    (temperature.tg90p, "tg90p"),
    (temperature.tg_days_above, "tg_days_above"),
    (temperature.tg_days_below, "tg_days_below"),
    (temperature.tg_max, "tg_max"),
    (temperature.tg_mean, "tg_mean"),
    (temperature.tg_min, "tg_min"),
    (temperature.thawing_degree_days, "thawing_degree_days"),
    (temperature.tn10p, "tn10p"),
    (temperature.tn90p, "tn90p"),
    (temperature.tn_days_above, "tn_days_above"),
    (temperature.tn_days_below, "tn_days_below"),
    (temperature.tn_max, "tn_max"),
    (temperature.tn_mean, "tn_mean"),
    (temperature.tn_min, "tn_min"),
    (temperature.tropical_nights, "tropical_nights"),
    (temperature.tx10p, "tx10p"),
    (temperature.tx90p, "tx90p"),
    (temperature.tx_days_above, "tx_days_above"),
    (temperature.tx_days_below, "tx_days_below"),
    (temperature.tx_max, "tx_max"),
    (temperature.tx_mean, "tx_mean"),
    (temperature.tx_min, "tx_min"),
    (temperature.tx_tn_days_above, "tx_tn_days_above"),
    (temperature.usda_hardiness_zones, "usda_hardiness_zones"),
    (temperature.warm_spell_duration_index, "warm_spell_duration_index"),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name", INDICATORS)
def test_temperature_indicator(
    mocker: MockerFixture,
    dummy_temp_ds: xarray.Dataset,
    earthkit_fn: Callable,
    xclim_name: str,
):
    """Test that the earthkit function wraps the xclim function correctly."""
    xclim_func_name = xclim_name

    mock_path = f"xclim.indicators.atmos.{xclim_func_name}"

    mock_fn = mocker.patch(mock_path)

    # Use a dummy argument dictionary
    kwargs = {"arg1": "val1", "arg2": 2}

    ds_in = dummy_temp_ds

    # Call the earthkit function
    earthkit_fn(ds=ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    # The dataset might be the same or transformed by the decorator
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
