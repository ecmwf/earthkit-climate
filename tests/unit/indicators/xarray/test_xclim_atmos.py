# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0


"""Tests for precipitation indicators."""

from typing import Any, Callable

import pytest
import xarray as xr
from pytest_mock import MockerFixture

from earthkit.climate.indicators import xarray as indicators

INDICATORS = [
    # Precipitation
    (indicators.antecedent_precipitation_index, "antecedent_precipitation_index", {"val": "test"}),
    (indicators.maximum_consecutive_dry_days, "maximum_consecutive_dry_days", {"val": "test"}),
    (
        indicators.maximum_consecutive_wet_days,
        "maximum_consecutive_wet_days",
        {"thresh": "2 mm/day", "freq": "MS"},
    ),
    (indicators.daily_pr_intensity, "daily_pr_intensity", {"thresh": "2 mm/day", "freq": "MS"}),
    (indicators.cffwis_indices, "cffwis_indices", {"arg1": "val1"}),
    (indicators.cold_and_dry_days, "cold_and_dry_days", {"arg1": "val1"}),
    (indicators.cold_and_wet_days, "cold_and_wet_days", {"arg1": "val1"}),
    (indicators.days_over_precip_doy_thresh, "days_over_precip_doy_thresh", {"arg1": "val1"}),
    (indicators.days_over_precip_thresh, "days_over_precip_thresh", {"arg1": "val1"}),
    (indicators.days_with_snow, "days_with_snow", {"arg1": "val1"}),
    (indicators.drought_code, "drought_code", {"arg1": "val1"}),
    (indicators.griffiths_drought_factor, "griffiths_drought_factor", {"arg1": "val1"}),
    (indicators.duff_moisture_code, "duff_moisture_code", {"arg1": "val1"}),
    (indicators.dry_days, "dry_days", {"arg1": "val1"}),
    (indicators.dry_spell_frequency, "dry_spell_frequency", {"arg1": "val1"}),
    (indicators.dry_spell_max_length, "dry_spell_max_length", {"arg1": "val1"}),
    (indicators.dry_spell_total_length, "dry_spell_total_length", {"arg1": "val1"}),
    (indicators.dryness_index, "dryness_index", {"arg1": "val1"}),
    (indicators.mcarthur_forest_fire_danger_index, "mcarthur_forest_fire_danger_index", {"arg1": "val1"}),
    (indicators.first_snowfall, "first_snowfall", {"arg1": "val1"}),
    (indicators.fraction_over_precip_doy_thresh, "fraction_over_precip_doy_thresh", {"arg1": "val1"}),
    (indicators.fraction_over_precip_thresh, "fraction_over_precip_thresh", {"arg1": "val1"}),
    (indicators.high_precip_low_temp, "high_precip_low_temp", {"arg1": "val1"}),
    (indicators.keetch_byram_drought_index, "keetch_byram_drought_index", {"arg1": "val1"}),
    (indicators.last_snowfall, "last_snowfall", {"arg1": "val1"}),
    (indicators.liquid_precip_ratio, "liquid_precip_ratio", {"arg1": "val1"}),
    (indicators.liquid_precip_average, "liquid_precip_average", {"arg1": "val1"}),
    (indicators.liquid_precip_accumulation, "liquid_precip_accumulation", {"arg1": "val1"}),
    (indicators.max_n_day_precipitation_amount, "max_n_day_precipitation_amount", {"arg1": "val1"}),
    (indicators.max_pr_intensity, "max_pr_intensity", {"arg1": "val1"}),
    (indicators.precip_average, "precip_average", {"arg1": "val1"}),
    (indicators.precip_accumulation, "precip_accumulation", {"arg1": "val1"}),
    (indicators.rain_on_frozen_ground_days, "rain_on_frozen_ground_days", {"arg1": "val1"}),
    (indicators.rain_season, "rain_season", {"arg1": "val1"}),
    (indicators.rprctot, "rprctot", {"arg1": "val1"}),
    (indicators.max_1day_precipitation_amount, "max_1day_precipitation_amount", {"arg1": "val1"}),
    (indicators.snowfall_frequency, "snowfall_frequency", {"arg1": "val1"}),
    (indicators.snowfall_intensity, "snowfall_intensity", {"arg1": "val1"}),
    (indicators.solid_precip_average, "solid_precip_average", {"arg1": "val1"}),
    (indicators.solid_precip_accumulation, "solid_precip_accumulation", {"arg1": "val1"}),
    (indicators.warm_and_dry_days, "warm_and_dry_days", {"arg1": "val1"}),
    (indicators.warm_and_wet_days, "warm_and_wet_days", {"arg1": "val1"}),
    (indicators.water_cycle_intensity, "water_cycle_intensity", {"arg1": "val1"}),
    (indicators.wet_precip_accumulation, "wet_precip_accumulation", {"arg1": "val1"}),
    (indicators.wet_spell_frequency, "wet_spell_frequency", {"arg1": "val1"}),
    (indicators.wet_spell_max_length, "wet_spell_max_length", {"arg1": "val1"}),
    (indicators.wet_spell_total_length, "wet_spell_total_length", {"arg1": "val1"}),
    (indicators.wetdays, "wetdays", {"arg1": "val1"}),
    (indicators.wetdays_prop, "wetdays_prop", {"arg1": "val1"}),
    (indicators.standardized_precipitation_index, "standardized_precipitation_index", {"arg1": "val1"}),
    (
        indicators.standardized_precipitation_evapotranspiration_index,
        "standardized_precipitation_evapotranspiration_index",
        {"arg1": "val1"},
    ),
    # Temperature
    (indicators.australian_hardiness_zones, "australian_hardiness_zones", {}),
    (indicators.biologically_effective_degree_days, "biologically_effective_degree_days", {}),
    (indicators.cold_spell_days, "cold_spell_days", {}),
    (indicators.cold_spell_duration_index, "cold_spell_duration_index", {}),
    (indicators.cold_spell_frequency, "cold_spell_frequency", {}),
    (indicators.cold_spell_max_length, "cold_spell_max_length", {}),
    (indicators.cold_spell_total_length, "cold_spell_total_length", {}),
    (indicators.consecutive_frost_days, "consecutive_frost_days", {}),
    (indicators.maximum_consecutive_frost_free_days, "maximum_consecutive_frost_free_days", {}),
    (indicators.cool_night_index, "cool_night_index", {}),
    (indicators.cooling_degree_days, "cooling_degree_days", {}),
    (indicators.cooling_degree_days_approximation, "cooling_degree_days_approximation", {}),
    (indicators.corn_heat_units, "corn_heat_units", {}),
    (indicators.chill_portions, "chill_portions", {}),
    (indicators.chill_units, "chill_units", {}),
    (indicators.degree_days_exceedance_date, "degree_days_exceedance_date", {}),
    (indicators.daily_freezethaw_cycles, "daily_freezethaw_cycles", {}),
    (indicators.daily_temperature_range, "daily_temperature_range", {}),
    (indicators.max_daily_temperature_range, "max_daily_temperature_range", {}),
    (indicators.daily_temperature_range_variability, "daily_temperature_range_variability", {}),
    (indicators.extreme_temperature_range, "extreme_temperature_range", {}),
    (indicators.fire_season, "fire_season", {}),
    (indicators.first_day_tg_above, "first_day_tg_above", {}),
    (indicators.first_day_tg_below, "first_day_tg_below", {}),
    (indicators.first_day_tn_above, "first_day_tn_above", {}),
    (indicators.first_day_tn_below, "first_day_tn_below", {}),
    (indicators.first_day_tx_above, "first_day_tx_above", {}),
    (indicators.first_day_tx_below, "first_day_tx_below", {}),
    (indicators.freezethaw_spell_frequency, "freezethaw_spell_frequency", {}),
    (indicators.freezethaw_spell_max_length, "freezethaw_spell_max_length", {}),
    (indicators.freezethaw_spell_mean_length, "freezethaw_spell_mean_length", {}),
    (indicators.freezing_degree_days, "freezing_degree_days", {}),
    (indicators.freshet_start, "freshet_start", {}),
    (indicators.frost_days, "frost_days", {}),
    (indicators.frost_free_season_end, "frost_free_season_end", {}),
    (indicators.frost_free_season_length, "frost_free_season_length", {}),
    (indicators.frost_free_season_start, "frost_free_season_start", {}),
    (indicators.frost_free_spell_max_length, "frost_free_spell_max_length", {}),
    (indicators.frost_season_length, "frost_season_length", {}),
    (indicators.growing_degree_days, "growing_degree_days", {}),
    (indicators.growing_season_end, "growing_season_end", {}),
    (indicators.growing_season_length, "growing_season_length", {}),
    (indicators.growing_season_start, "growing_season_start", {}),
    (indicators.heat_spell_frequency, "heat_spell_frequency", {}),
    (indicators.heat_spell_max_length, "heat_spell_max_length", {}),
    (indicators.heat_spell_total_length, "heat_spell_total_length", {}),
    (indicators.heat_wave_frequency, "heat_wave_frequency", {}),
    (indicators.heat_wave_index, "heat_wave_index", {}),
    (indicators.heat_wave_max_length, "heat_wave_max_length", {}),
    (indicators.heat_wave_total_length, "heat_wave_total_length", {}),
    (indicators.heating_degree_days, "heating_degree_days", {}),
    (indicators.heating_degree_days_approximation, "heating_degree_days_approximation", {}),
    (indicators.hot_days, "hot_days", {}),
    (indicators.hot_spell_frequency, "hot_spell_frequency", {}),
    (indicators.hot_spell_max_length, "hot_spell_max_length", {}),
    (indicators.hot_spell_max_magnitude, "hot_spell_max_magnitude", {}),
    (indicators.hot_spell_total_length, "hot_spell_total_length", {}),
    (indicators.huglin_index, "huglin_index", {}),
    (indicators.ice_days, "ice_days", {}),
    (indicators.last_spring_frost, "last_spring_frost", {}),
    (indicators.late_frost_days, "late_frost_days", {}),
    (indicators.latitude_temperature_index, "latitude_temperature_index", {}),
    (indicators.maximum_consecutive_warm_days, "maximum_consecutive_warm_days", {}),
    (indicators.tg10p, "tg10p", {}),
    (indicators.tg90p, "tg90p", {}),
    (indicators.tg_days_above, "tg_days_above", {}),
    (indicators.tg_days_below, "tg_days_below", {}),
    (indicators.tg_max, "tg_max", {}),
    (indicators.tg_mean, "tg_mean", {}),
    (indicators.tg_min, "tg_min", {}),
    (indicators.thawing_degree_days, "thawing_degree_days", {}),
    (indicators.tn10p, "tn10p", {}),
    (indicators.tn90p, "tn90p", {}),
    (indicators.tn_days_above, "tn_days_above", {}),
    (indicators.tn_days_below, "tn_days_below", {}),
    (indicators.tn_max, "tn_max", {}),
    (indicators.tn_mean, "tn_mean", {}),
    (indicators.tn_min, "tn_min", {}),
    (indicators.tropical_nights, "tropical_nights", {}),
    (indicators.tx10p, "tx10p", {}),
    (indicators.tx90p, "tx90p", {}),
    (indicators.tx_days_above, "tx_days_above", {}),
    (indicators.tx_days_below, "tx_days_below", {}),
    (indicators.tx_max, "tx_max", {}),
    (indicators.tx_mean, "tx_mean", {}),
    (indicators.tx_min, "tx_min", {}),
    (indicators.tx_tn_days_above, "tx_tn_days_above", {}),
    (indicators.usda_hardiness_zones, "usda_hardiness_zones", {}),
    (indicators.warm_spell_duration_index, "warm_spell_duration_index", {}),
    # Synoptic
    (indicators.jetstream_metric_woollings, "jetstream_metric_woollings", {}),
    # Wind
    (indicators.calm_days, "calm_days", {}),
    (indicators.sfcWind_max, "sfcWind_max", {}),
    (indicators.sfcWind_mean, "sfcWind_mean", {}),
    (indicators.sfcWind_min, "sfcWind_min", {}),
    (indicators.sfcWindmax_max, "sfcWindmax_max", {}),
    (indicators.sfcWindmax_mean, "sfcWindmax_mean", {}),
    (indicators.sfcWindmax_min, "sfcWindmax_min", {}),
    (indicators.windy_days, "windy_days", {}),
]


@pytest.mark.parametrize("earthkit_fn, xclim_name, kwargs", INDICATORS)
def test_precipitation_indicator(
    mocker: MockerFixture,
    dummy_precip_ds: xr.Dataset,
    earthkit_fn: Callable[..., Any],
    xclim_name: str,
    kwargs: dict[str, Any],
) -> None:
    """Test that the earthkit function wraps the xclim function correctly.

    Parameters
    ----------
    mocker : MockerFixture
        Mocking utility from pytest-mock.
    dummy_precip_ds : xarray.Dataset
        A dummy dataset containing precipitation variables.
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

    mock_path = f"xclim.indicators.atmos.{xclim_func_name}"

    mock_fn = mocker.patch(mock_path)

    ds_in = dummy_precip_ds

    # Call the earthkit function
    earthkit_fn(ds=ds_in, **kwargs)

    # Verify wrapped function called with the dataset and arguments
    mock_fn.assert_called_once()
    assert mock_fn.call_args.kwargs["ds"] is not None
    for k, v in kwargs.items():
        assert mock_fn.call_args.kwargs[k] == v
