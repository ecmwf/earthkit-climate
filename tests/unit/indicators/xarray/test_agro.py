# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr
import xclim

from earthkit.climate import indicators
from earthkit.climate.indicators.xarray import _agro
from earthkit.climate.indicators.xarray.agro.engine.cdi import cdi
from earthkit.climate.indicators.xarray.agro.engine.cei import cei
from earthkit.climate.indicators.xarray.agro.engine.seasons import build_seasons_map


@pytest.fixture
def synthetic_agro_ds() -> xr.Dataset:
    """
    Create a synthetic daily dataset with meteorological variables across 2 years.

    Returns
    -------
    xarray.Dataset
        Synthetic dataset with tas, tasmax, and rsds.
    """
    dates = pd.date_range("2020-01-01", "2021-12-31", freq="D")
    n = len(dates)

    tas_vals = 15.0 + 10.0 * np.sin(2 * np.pi * np.arange(n) / 365.25 - np.pi / 2)
    tasmax_vals = tas_vals + 5.0
    rsds_vals = np.maximum(200.0 + 100.0 * np.sin(2 * np.pi * np.arange(n) / 365.25 - np.pi / 2), 0.0)

    return xr.Dataset(
        {
            "tas": (["time"], tas_vals, {"units": "degC"}),
            "tasmax": (["time"], tasmax_vals, {"units": "degC"}),
            "rsds": (["time"], rsds_vals, {"units": "W m-2"}),
        },
        coords={"time": dates},
    )


def test_build_seasons_map_within_year() -> None:
    """
    Test build_seasons_map for growing season contained within calendar years.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")
    seasons_df, season_ids = build_seasons_map(dates, season_start="04-01", season_end="10-31")

    assert len(seasons_df) > 0
    in_season_mask = ~np.isnan(season_ids)

    # April 1st should be in season
    apr1_idx = dates.get_loc("2020-04-01")
    assert in_season_mask[apr1_idx]

    # January 15th should be out of season
    jan15_idx = dates.get_loc("2020-01-15")
    assert not in_season_mask[jan15_idx]


def test_build_seasons_map_cross_year() -> None:
    """
    Test build_seasons_map for winter season crossing calendar year boundaries.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-06-01", "2021-06-01", freq="D")
    seasons_df, season_ids = build_seasons_map(dates, season_start="10-01", season_end="03-31")

    assert len(seasons_df) > 0

    # November should be in season
    nov_idx = dates.get_loc("2020-11-15")
    assert not np.isnan(season_ids[nov_idx])

    # January should be in the same season
    jan_idx = dates.get_loc("2021-01-15")
    assert not np.isnan(season_ids[jan_idx])
    assert season_ids[nov_idx] == season_ids[jan_idx]

    # July should be out of season
    jul_idx = dates.get_loc("2020-07-15")
    assert np.isnan(season_ids[jul_idx])


def test_cei_engine(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test CEI engine directly with synthetic temperature data.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    res = cei(
        synthetic_agro_ds["tas"],
        season_start="04-01",
        season_end="10-31",
        lower=10.0,
        upper=np.inf,
        direction="above",
    )
    assert isinstance(res, xr.Dataset)
    assert "cum_excess" in res
    assert "cond" in res
    assert "valid" in res
    assert res["cum_excess"].max() > 0.0


def test_cdi_engine(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test CDI engine directly with compound conditions.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    bounds = [{"var": "tasmax", "lower": 25.0, "upper": np.inf}]
    res = cdi(
        synthetic_agro_ds,
        bounds=bounds,
        season_start="04-01",
        season_end="10-31",
        min_duration=1,
    )
    assert isinstance(res, xr.Dataset)
    assert "cum_days" in res
    assert res["cum_days"].max() > 0.0


def test_chilling_hours_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test chilling_hours indicator wrapper and CF metadata.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    ch = indicators.chilling_hours(tas=synthetic_agro_ds["tas"])
    assert isinstance(ch, xr.DataArray)
    assert ch.attrs["units"] == "h"
    assert "Chilling Hours" in ch.attrs["long_name"]


def test_vernalisation_days_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test vernalisation_days indicator wrapper.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    vcr = indicators.vernalisation_days(ds=synthetic_agro_ds)
    assert isinstance(vcr, xr.DataArray)
    assert vcr.attrs["units"] == "d"


def test_pest_degree_days_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test pest_degree_days indicator with custom base temperature.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    ddp = indicators.pest_degree_days(ds=synthetic_agro_ds, tbase=12.0)
    assert isinstance(ddp, xr.DataArray)
    assert "degC d" in ddp.attrs["units"]


def test_growing_degree_days_season_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test growing_degree_days_season with custom crop seasons.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    gdd = indicators.growing_degree_days_season(
        ds=synthetic_agro_ds,
        season_start="05-01",
        season_end="09-30",
        tbase=5.0,
    )
    assert isinstance(gdd, xr.DataArray)
    assert "degC d" in gdd.attrs["units"]


def test_heat_stress_days_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test heat_stress_days indicator wrapper.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    hsd = indicators.heat_stress_days(ds=synthetic_agro_ds, thresh=25.0)
    assert isinstance(hsd, xr.DataArray)
    assert hsd.attrs["units"] == "d"


def test_heatwave_duration_season_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test heatwave_duration_season with min_duration requirement.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    hwd = indicators.heatwave_duration_season(
        ds=synthetic_agro_ds,
        thresh=20.0,
        min_duration=3,
    )
    assert isinstance(hwd, xr.DataArray)
    assert hwd.attrs["units"] == "d"


def test_cumulative_shortwave_radiation_indicator(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test cumulative_shortwave_radiation indicator wrapper.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    srad = indicators.cumulative_shortwave_radiation(ds=synthetic_agro_ds)
    assert isinstance(srad, xr.DataArray)
    assert "W m-2 d" in srad.attrs["units"]


def test_indicator_return_dataset_option(synthetic_agro_ds: xr.Dataset) -> None:
    """
    Test return_dataset=True returns the full Dataset structure.

    Parameters
    ----------
    synthetic_agro_ds : xarray.Dataset
        Synthetic agro dataset.

    Returns
    -------
    None
    """
    res_ds = indicators.chilling_hours(ds=synthetic_agro_ds, return_dataset=True)
    assert isinstance(res_ds, xr.Dataset)
    assert "cum_excess" in res_ds
    assert "cond" in res_ds
    assert "valid" in res_ds


def test_agro_indicators_in_indicators_all() -> None:
    """
    Test that agro indicators and engine functions are exported in indicators.__all__.

    Returns
    -------
    None
    """
    expected = [
        "chilling_hours",
        "vernalisation_days",
        "pest_degree_days",
        "growing_degree_days_season",
        "heat_stress_days",
        "heatwave_duration_season",
        "cumulative_shortwave_radiation",
        "cei",
        "cdi",
        "build_seasons_map",
    ]
    for name in expected:
        assert hasattr(indicators, name)
        assert hasattr(_agro, name)


def test_regression_seasons_map_non_midnight_timestamps() -> None:
    """
    Verify that timestamps on the last day of the season (e.g. 12:00 UTC) are included.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    dates = pd.date_range("2021-03-30 12:00", "2021-04-02 12:00", freq="D")
    _, sids = build_seasons_map(dates, "10-01", "03-31")
    assert not np.isnan(sids[1])
    assert np.isnan(sids[2])


def test_regression_seasons_map_leap_day() -> None:
    """
    Verify that seasons defined with 02-29 do not crash on non-leap years.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", "2022-01-01", freq="D")
    seasons_df, sids = build_seasons_map(dates, "01-01", "02-29")
    assert len(seasons_df) > 0
    assert not np.isnan(sids).all()


def test_regression_seasons_map_empty_time() -> None:
    """
    Verify that an empty time array returns an empty seasons DataFrame and empty IDs array.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    seasons_df, sids = build_seasons_map(np.array([], dtype="datetime64[ns]"))
    assert len(seasons_df) == 0
    assert len(sids) == 0


def test_regression_cei_skip_days_with_min_duration() -> None:
    """
    Verify that qualifying days prior to a NaN are not lost during excess accumulation.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    from earthkit.climate.indicators.xarray.agro.engine.cei import _cei_numpy

    x = np.array([5.0, np.nan, 5.0, 5.0])
    sids = np.array([1.0, 1.0, 1.0, 1.0])
    _, _, _, cum_excess = _cei_numpy(
        x,
        season_ids=sids,
        lower=0.0,
        upper=10.0,
        inc_lower=True,
        inc_upper=True,
        min_duration=3,
        na_action="skip_days",
        direction="above",
        weight_fn=None,
    )
    assert np.isclose(cum_excess[-1], 15.0)


def test_regression_cei_direction_above_requires_finite_lower() -> None:
    """
    Verify that direction='above' raises ValueError when lower bound is infinite.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    t = pd.date_range("2020-04-01", periods=5, freq="D")
    da = xr.DataArray([10.0, 15.0, 20.0, 25.0, 30.0], coords={"time": t}, dims=["time"])
    with pytest.raises(ValueError, match="direction='above' requires a finite lower bound"):
        cei(da, season_start="04-01", season_end="10-31", direction="above")


def test_regression_cdi_max_run_skip_days() -> None:
    """
    Verify that max_run with skip_days handles transparent NaNs correctly.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    t = pd.date_range("2020-04-01", periods=5, freq="D")
    ds = xr.Dataset({"tasmax": (["time"], [36.0, np.nan, 36.0, 36.0, 36.0])}, coords={"time": t})
    res = cdi(
        ds,
        bounds=[{"var": "tasmax", "lower": 35.0}],
        season_start="04-01",
        season_end="10-31",
        min_duration=2,
        na_action="skip_days",
        max_run=True,
    )
    assert np.isclose(res["cum_days"].values[-1], 4.0)


def test_regression_resolve_data_array_strict_name_validation() -> None:
    """
    Verify that requesting a nonexistent variable raises ValueError instead of silent fallback.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    ds = xr.Dataset({"tasmax": xr.DataArray([30.0])})
    with pytest.raises(ValueError, match="Variable 'tas_max_typo' not found in ds"):
        indicators.heat_stress_days(tasmax="tas_max_typo", ds=ds)


def test_cdi_compound_multivariable_combiners() -> None:
    """
    Test CDI with compound multi-variable conditions and combiners.

    Evaluates 'all', 'any', and 'k_of_n' boolean logic across multiple variables
    with heterogeneous bounds.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=10, freq="D")
    tasmax = np.array([36.0, 37.0, 38.0, 36.0, 36.0, 36.0, 20.0, 20.0, 20.0, 20.0])
    pr = np.array([0.0, 0.0, 0.0, 10.0, 10.0, 10.0, 0.0, 0.0, 0.0, 0.0])
    wind = np.array([12.0] * 10)

    ds = xr.Dataset(
        {
            "tasmax": (["time"], tasmax),
            "pr": (["time"], pr),
            "sfcWind": (["time"], wind),
        },
        coords={"time": dates},
    )

    bounds = [
        {"var": "tasmax", "lower": 35.0},
        {"var": "pr", "upper": 1.0},
    ]

    res_all = cdi(ds, bounds=bounds, season_start="04-01", season_end="10-31", combiner="all")
    assert np.isclose(res_all["cum_days"].values[-1], 3.0)
    assert np.all(res_all["cond"].values[:3] == 1.0)
    assert np.all(res_all["cond"].values[3:] == 0.0)

    res_any = cdi(ds, bounds=bounds, season_start="04-01", season_end="10-31", combiner="any")
    assert np.isclose(res_any["cum_days"].values[-1], 10.0)
    assert np.all(res_any["cond"].values == 1.0)

    bounds_3 = [
        {"var": "tasmax", "lower": 35.0},
        {"var": "pr", "upper": 1.0},
        {"var": "sfcWind", "lower": 15.0},
    ]
    res_k2 = cdi(ds, bounds=bounds_3, season_start="04-01", season_end="10-31", combiner="k_of_n", k=2)
    assert np.isclose(res_k2["cum_days"].values[-1], 3.0)


def test_agro_multidimensional_spatial_grid() -> None:
    """
    Test agro indicators on multi-dimensional spatial grid (time, lat, lon).

    Verifies coordinate preservation, dimension alignment, and spatial variation
    in cumulative output arrays across different geographic cells.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=60, freq="D")
    lats = [40.0, 50.0]
    lons = [0.0, 10.0]

    tas_arr = np.zeros((len(dates), len(lats), len(lons)))
    tasmax_arr = np.zeros((len(dates), len(lats), len(lons)))

    tas_arr[:, 0, :] = 25.0
    tas_arr[:, 1, :] = 12.0
    tasmax_arr[:, 0, :] = 36.0
    tasmax_arr[:, 1, :] = 22.0

    ds = xr.Dataset(
        {
            "tas": (["time", "lat", "lon"], tas_arr, {"units": "degC"}),
            "tasmax": (["time", "lat", "lon"], tasmax_arr, {"units": "degC"}),
        },
        coords={"time": dates, "lat": lats, "lon": lons},
    )

    gdd = indicators.growing_degree_days_season(
        ds=ds,
        season_start="04-01",
        season_end="10-31",
        tbase=10.0,
    )
    assert gdd.dims == ("time", "lat", "lon")
    assert gdd.shape == (60, 2, 2)
    np.testing.assert_allclose(gdd.isel(lat=0, lon=0).values[-1], 900.0)
    np.testing.assert_allclose(gdd.isel(lat=1, lon=0).values[-1], 120.0)

    hsd = indicators.heat_stress_days(
        ds=ds,
        season_start="04-01",
        season_end="10-31",
        thresh=35.0,
    )
    assert hsd.dims == ("time", "lat", "lon")
    np.testing.assert_allclose(hsd.isel(lat=0, lon=0).values[-1], 60.0)
    np.testing.assert_allclose(hsd.isel(lat=1, lon=0).values[-1], 0.0)


def test_agro_dask_lazy_evaluation() -> None:
    """
    Test agro indicators on Dask chunked datasets for lazy evaluation and accuracy.

    Verifies that dask computations remain delayed when passed through the wrapper
    and that computed results match in-memory NumPy execution.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=50, freq="D")
    lats = [35.0, 45.0]
    lons = [-5.0, 5.0]

    arr = np.full((len(dates), len(lats), len(lons)), 22.0)
    da = xr.DataArray(
        arr,
        coords={"time": dates, "lat": lats, "lon": lons},
        dims=["time", "lat", "lon"],
        name="tas",
        attrs={"units": "degC"},
    )

    gdd_numpy = indicators.growing_degree_days_season(
        da,
        season_start="04-01",
        season_end="10-31",
        tbase=10.0,
    )

    da_chunked = da.chunk({"time": -1, "lat": 1, "lon": 1})
    gdd_dask = indicators.growing_degree_days_season(
        da_chunked,
        season_start="04-01",
        season_end="10-31",
        tbase=10.0,
    )

    assert hasattr(gdd_dask.data, "dask")
    computed = gdd_dask.compute()
    assert not hasattr(computed.data, "dask")
    np.testing.assert_allclose(computed.values, gdd_numpy.values)


def test_analytical_growing_degree_days() -> None:
    """
    Verify exact analytical calculation for growing degree days.

    Uses a constant temperature time series to verify mathematical exactness
    of the cumulative excess calculation.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    tas = xr.DataArray(
        np.full(len(dates), 18.0),
        coords={"time": dates},
        dims=["time"],
        name="tas",
        attrs={"units": "degC"},
    )
    res = indicators.growing_degree_days_season(
        tas,
        season_start="01-01",
        season_end="12-31",
        tbase=8.0,
    )
    expected_daily = np.arange(1, 101) * 10.0
    np.testing.assert_allclose(res.values, expected_daily)


def test_analytical_chilling_hours_and_vernalisation() -> None:
    """
    Verify exact analytical calculation for chilling hours and vernalisation days.

    Tests boundary conditions and unit accumulation against known synthetic daily temperatures.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-10-01", periods=30, freq="D")
    vals = np.array([4.0] * 10 + [-3.0] * 10 + [10.0] * 10)
    tas = xr.DataArray(
        vals,
        coords={"time": dates},
        dims=["time"],
        name="tas",
        attrs={"units": "degC"},
    )

    ch = indicators.chilling_hours(tas, season_start="10-01", season_end="03-31")
    assert np.isclose(ch.values[-1], 10.0)

    vd = indicators.vernalisation_days(tas, season_start="10-01", season_end="03-31")
    assert np.isclose(vd.values[-1], 10.0)


def test_analytical_heatwave_spells_and_max_run() -> None:
    """
    Verify heatwave spell length filtering and max_run logic in CDI.

    Tests that spells shorter than min_duration are excluded from accumulation,
    and that max_run computes the running longest qualifying spell.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-06-01", periods=15, freq="D")
    tasmax_vals = [36.0, 36.0, 25.0, 37.0, 37.0, 37.0, 37.0, 20.0, 20.0, 38.0, 38.0, 38.0, 22.0, 22.0, 22.0]
    ds = xr.Dataset(
        {"tasmax": (["time"], np.array(tasmax_vals))},
        coords={"time": dates},
    )

    res_cum = indicators.heatwave_duration_season(
        ds=ds,
        season_start="06-01",
        season_end="08-31",
        thresh=35.0,
        min_duration=3,
    )
    assert np.isclose(res_cum.values[-1], 7.0)

    bounds = [{"var": "tasmax", "lower": 35.0}]
    res_max = cdi(
        ds,
        bounds=bounds,
        season_start="06-01",
        season_end="08-31",
        min_duration=3,
        max_run=True,
    )
    assert np.isclose(res_max["cum_days"].values[-1], 4.0)


def test_growing_degree_days_xclim_equivalence() -> None:
    """
    Verify numerical equivalence between growing_degree_days_season and xclim GDD.

    Compares output against xclim.indicators.atmos.growing_degree_days across
    a full calendar year season with matching threshold.

    Returns
    -------
    None
    """
    xclim.set_options(cf_compliance="log")
    dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")
    tas_vals = 15.0 + 8.0 * np.sin(2 * np.pi * np.arange(len(dates)) / 366.0)
    tas = xr.DataArray(
        tas_vals,
        coords={"time": dates},
        dims=["time"],
        name="tas",
        attrs={
            "units": "degC",
            "standard_name": "air_temperature",
            "cell_methods": "time: mean",
        },
    )

    gdd_ek = indicators.growing_degree_days_season(
        tas,
        season_start="01-01",
        season_end="12-31",
        tbase=10.0,
    )
    gdd_xc = xclim.indicators.atmos.growing_degree_days(
        tas,
        thresh="10.0 degC",
        freq="YS",
    )

    np.testing.assert_allclose(gdd_ek.values[-1], gdd_xc.values[0], rtol=1e-5)


def test_cei_custom_weight_function() -> None:
    """
    Test CEI engine with custom weighting function.

    Verifies that a custom scaling function f(x) is properly applied to
    the calculated daily excess.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=10, freq="D")
    vals = np.linspace(11.0, 20.0, 10)
    da = xr.DataArray(vals, coords={"time": dates}, dims=["time"], name="tas")

    def weight_func(x: np.ndarray) -> np.ndarray:
        """
        Scale temperature excess by half.

        Parameters
        ----------
        x : numpy.ndarray
            Input array.

        Returns
        -------
        numpy.ndarray
            Scaled excess.
        """
        return (x - 10.0) * 0.5

    res = cei(
        da,
        season_start="04-01",
        season_end="10-31",
        lower=10.0,
        upper=np.inf,
        direction="above",
        weight_fn=weight_func,
    )
    unweighted = cei(
        da,
        season_start="04-01",
        season_end="10-31",
        lower=10.0,
        upper=np.inf,
        direction="above",
    )

    np.testing.assert_allclose(res["cum_excess"].values, unweighted["cum_excess"].values * 0.5)


def test_cei_direction_below_and_exclusive_bounds() -> None:
    """
    Test CEI with direction='below' and exclusive boundary conditions.

    Verifies that direction='below' computes upper - x and that inc_lower=False
    excludes threshold boundary equality.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-10-01", periods=5, freq="D")
    da = xr.DataArray([-2.0, -1.0, 0.0, 1.0, 2.0], coords={"time": dates}, dims=["time"], name="tas")

    res_inc = cei(
        da,
        season_start="10-01",
        season_end="03-31",
        lower=-np.inf,
        upper=0.0,
        inc_upper=True,
        direction="below",
    )
    np.testing.assert_allclose(res_inc["cum_excess"].values, [2.0, 3.0, 3.0, 3.0, 3.0])

    res_exc = cei(
        da,
        season_start="10-01",
        season_end="03-31",
        lower=-np.inf,
        upper=0.0,
        inc_upper=False,
        direction="below",
    )
    assert res_exc["cond"].values[2] == 0.0
    assert res_inc["cond"].values[2] == 1.0


def test_agro_indicators_unnamed_dataarray_and_kwargs() -> None:
    """
    Test all agro indicator entry points with unnamed DataArrays and keyword arguments.

    Verifies robustness of _resolve_data_array across various input styles.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=10, freq="D")
    da_unnamed = xr.DataArray(np.full(10, 25.0), coords={"time": dates}, dims=["time"])

    ch = indicators.chilling_hours(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(ch, xr.DataArray)

    vd = indicators.vernalisation_days(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(vd, xr.DataArray)

    pdd = indicators.pest_degree_days(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(pdd, xr.DataArray)

    gdd = indicators.growing_degree_days_season(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(gdd, xr.DataArray)

    hsd = indicators.heat_stress_days(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(hsd, xr.DataArray)

    hwd = indicators.heatwave_duration_season(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(hwd, xr.DataArray)

    srad = indicators.cumulative_shortwave_radiation(da_unnamed, season_start="04-01", season_end="10-31")
    assert isinstance(srad, xr.DataArray)


def test_subdaily_resampling_aggregation() -> None:
    """
    Test sub-daily hourly input handling with daily aggregation in CEI and CDI.

    Verifies daily resampling via daily_agg parameter for hourly datasets.

    Returns
    -------
    None
    """
    hourly_dates = pd.date_range("2020-04-01 00:00", periods=48, freq="h")
    hourly_tas = np.tile(np.linspace(10.0, 33.0, 24), 2)
    da_hourly = xr.DataArray(
        hourly_tas,
        coords={"time": hourly_dates},
        dims=["time"],
        name="tas",
        attrs={"units": "degC"},
    )

    ch_native = indicators.chilling_hours(
        da_hourly,
        season_start="04-01",
        season_end="10-31",
        lower=10.0,
        upper=20.0,
        native_freq=True,
    )
    assert len(ch_native) == 48

    gdd_daily = indicators.growing_degree_days_season(
        da_hourly,
        season_start="04-01",
        season_end="10-31",
        tbase=10.0,
        daily_agg="mean",
    )
    assert len(gdd_daily) == 2


def test_agro_error_handling_and_validation() -> None:
    """
    Test error detection and input validation across agro indicators and engines.

    Verifies that invalid parameter configurations raise explicit ValueError or TypeError exceptions.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-04-01", periods=10, freq="D")
    da = xr.DataArray(np.full(10, 20.0), coords={"time": dates}, dims=["time"])
    ds = xr.Dataset({"tasmax": da})

    with pytest.raises(ValueError, match="direction must be 'above' or 'below'"):
        cei(da, season_start="04-01", season_end="10-31", direction="sideways")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="direction='below' requires a finite upper bound"):
        cei(da, season_start="04-01", season_end="10-31", direction="below", upper=np.inf)

    with pytest.raises(ValueError, match="min_duration must be >= 1"):
        cei(da, season_start="04-01", season_end="10-31", lower=10.0, min_duration=0)

    with pytest.raises(ValueError, match="na_action must be 'false' or 'skip_days'"):
        cei(da, season_start="04-01", season_end="10-31", lower=10.0, na_action="ignore")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="weight_fn must be callable or None"):
        cei(da, season_start="04-01", season_end="10-31", weight_fn="not_a_function")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="combiner must be 'all', 'any', or 'k_of_n'"):
        cdi(ds, bounds=[{"var": "tasmax", "lower": 30.0}], combiner="xor")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="Provide k \\(int\\) when combiner='k_of_n'"):
        cdi(ds, bounds=[{"var": "tasmax", "lower": 30.0}], combiner="k_of_n")

    with pytest.raises(ValueError, match="bounds must contain a 'var' column"):
        cdi(ds, bounds=[{"lower": 30.0}])

    with pytest.raises(ValueError, match="No time steps fall within the season window"):
        cei(da, season_start="01-01", season_end="02-01", lower=10.0)
