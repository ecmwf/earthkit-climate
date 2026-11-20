# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr
import xclim.core.calendar as xcal

from earthkit.climate import indicators
from earthkit.climate.indicators.xarray import _icclim


@pytest.fixture
def synthetic_temp_da() -> xr.DataArray:
    """
    Create a synthetic daily temperature DataArray for testing.

    Returns
    -------
    xarray.DataArray
        Synthetic temperature series.
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    return xr.DataArray(
        np.full(len(dates), 28.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )


@pytest.fixture
def synthetic_temp_dataset() -> xr.Dataset:
    """
    Create a synthetic daily temperature Dataset with tasmax and tasmin.

    Returns
    -------
    xarray.Dataset
        Synthetic temperature dataset.
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tx = xr.DataArray(
        np.full(len(dates), 28.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )
    tn = xr.DataArray(
        np.full(len(dates), 14.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmin",
        attrs={"units": "degC"},
    )
    return xr.Dataset({"tasmax": tx, "tasmin": tn})


def test_icclim_su_direct_call(synthetic_temp_da: xr.DataArray) -> None:
    """
    Test summer days (su) indicator called directly from indicators root namespace.

    Parameters
    ----------
    synthetic_temp_da : xarray.DataArray
        Synthetic temperature data fixture.

    Returns
    -------
    None
    """
    res = indicators.su(synthetic_temp_da, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "SU"
    assert np.isclose(res.values[0], 366.0)
    assert res.attrs["units"] == "d"


def test_icclim_dtr_dataset_call(synthetic_temp_dataset: xr.Dataset) -> None:
    """
    Test diurnal temperature range (dtr) indicator called with a Dataset.

    Parameters
    ----------
    synthetic_temp_dataset : xarray.Dataset
        Synthetic temperature dataset fixture.

    Returns
    -------
    None
    """
    res = indicators.dtr(ds=synthetic_temp_dataset, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "DTR"
    assert np.isclose(res.values[0], 14.0)


def test_icclim_fd_frost_days() -> None:
    """
    Test frost days (fd) indicator with cold temperatures.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tn = xr.DataArray(
        np.full(len(dates), -5.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmin",
        attrs={"units": "degC"},
    )
    res = indicators.fd(tn, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "FD"
    assert np.isclose(res.values[0], 366.0)


def test_icclim_cdd_dry_days() -> None:
    """
    Test consecutive dry days (cdd) indicator with dry precipitation series.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    pr = xr.DataArray(
        np.zeros(len(dates)),
        coords={"time": dates},
        dims=["time"],
        name="pr",
        attrs={"units": "mm/day"},
    )
    res = indicators.cdd(pr, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "CDD"
    assert np.isclose(res.values[0], 366.0)


def test_icclim_rx5day() -> None:
    """
    Test maximum 5-day precipitation amount (rx5day) indicator.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    pr = xr.DataArray(
        np.ones(len(dates)) * 10.0,
        coords={"time": dates},
        dims=["time"],
        name="pr",
        attrs={"units": "mm/day"},
    )
    res = indicators.rx5day(pr, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "RX5day"
    assert np.isclose(res.values[0], 50.0)


def test_icclim_module_has_all_indices() -> None:
    """
    Test that _icclim defines the standard ECA&D indices.

    Returns
    -------
    None
    """
    for index_name in ["su", "fd", "cdd", "rx1day", "rx5day", "dtr"]:
        assert hasattr(_icclim, index_name)
        assert callable(getattr(_icclim, index_name))
    for index_name in ["tx90p", "tx10p", "tn90p", "tn10p", "tg90p", "tg10p"]:
        assert hasattr(_icclim, f"_{index_name}")
        assert hasattr(_icclim, f"icclim_{index_name}")
        assert hasattr(indicators, index_name)


def test_icclim_overlapping_aliases() -> None:
    """
    Test explicit icclim_* aliases for the 6 overlapping percentile indices.

    Returns
    -------
    None
    """
    overlapping = ["tg10p", "tg90p", "tn10p", "tn90p", "tx10p", "tx90p"]
    for name in overlapping:
        alias_name = f"icclim_{name}"
        assert hasattr(indicators, alias_name)
        fn = getattr(indicators, alias_name)
        assert callable(fn)
        assert fn.__module__ == "earthkit.climate.indicators.xarray._icclim"


def test_percentile_backend_dispatch_auto_and_explicit(synthetic_temp_da: xr.DataArray) -> None:
    """
    Test unified tx90p dispatch with backend='auto', backend='icclim', and backend='xclim'.

    Parameters
    ----------
    synthetic_temp_da : xarray.DataArray
        Synthetic temperature series fixture.

    Returns
    -------
    None
    """
    # 1. Auto dispatch without tasmax_per selects icclim
    res_auto = indicators.tx90p(
        synthetic_temp_da,
        base_period_time_range=["2020-01-01", "2020-06-30"],
        freq="YS",
    )
    assert isinstance(res_auto, xr.DataArray)
    assert res_auto.name == "TX90p"

    # 2. Explicit backend='icclim'
    res_icclim = indicators.tx90p(
        synthetic_temp_da,
        base_period_time_range=["2020-01-01", "2020-06-30"],
        freq="YS",
        backend="icclim",
    )
    assert isinstance(res_icclim, xr.DataArray)
    assert res_icclim.name == "TX90p"

    # 3. Explicit backend='xclim' without tasmax_per raises ValueError
    with pytest.raises(ValueError, match="When using backend='xclim', 'tasmax_per'"):
        indicators.tx90p(synthetic_temp_da, backend="xclim")

    # 4. Unknown backend raises ValueError
    with pytest.raises(ValueError, match="Unknown backend: 'invalid'"):
        indicators.tx90p(synthetic_temp_da, backend="invalid")  # type: ignore[arg-type]


def test_regression_icclim_unnamed_dataarrays() -> None:
    """
    Verify that multi-variable icclim indices accept unnamed DataArrays without error.

    Returns
    -------
    None
    """
    t = pd.date_range("2000-01-01", periods=10)
    tas = xr.DataArray(np.ones(10) * 300, coords={"time": t}, dims=["time"], attrs={"units": "K"})
    pr = xr.DataArray(np.ones(10) * 5, coords={"time": t}, dims=["time"], attrs={"units": "mm/day"})
    res = indicators.cd(tas=tas, pr=pr)
    assert isinstance(res, xr.DataArray)
    assert res.name == "CD"


def test_regression_icclim_custom_ds_var_names() -> None:
    """
    Verify that custom variable names passed as strings in ds resolve correctly in icclim.

    Returns
    -------
    None
    """
    t = pd.date_range("2000-01-01", periods=10)
    ds = xr.Dataset(
        {"temp_max": (["time"], np.ones(10) * 300), "extra": (["time"], np.ones(10))},
        coords={"time": t},
    )
    res = indicators.su(tasmax="temp_max", ds=ds)
    assert isinstance(res, xr.DataArray)
    assert res.name == "SU"


def test_icclim_temperature_threshold_indices() -> None:
    """
    Test standard temperature extreme and threshold indices in icclim.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tx = xr.DataArray(
        np.full(len(dates), -3.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )
    tn = xr.DataArray(
        np.full(len(dates), 22.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmin",
        attrs={"units": "degC"},
    )

    # Ice days (TX < 0 degC)
    res_id = indicators.id(tx, freq="YS")
    assert isinstance(res_id, xr.DataArray)
    assert res_id.name == "ID"
    assert np.isclose(res_id.values[0], 366.0)

    # Tropical nights (TN > 20 degC)
    res_tr = indicators.tr(tn, freq="YS")
    assert isinstance(res_tr, xr.DataArray)
    assert res_tr.name == "TR"
    assert np.isclose(res_tr.values[0], 366.0)

    # Daily temperature extrema
    tx_var = xr.DataArray(
        np.linspace(10.0, 30.0, len(dates)),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )
    res_txx = indicators.txx(tx_var, freq="YS")
    assert np.isclose(res_txx.values[0], 30.0)

    res_txn = indicators.txn(tx_var, freq="YS")
    assert np.isclose(res_txn.values[0], 10.0)


def test_icclim_precipitation_indices() -> None:
    """
    Test precipitation count and intensity indices in icclim.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    # 5 days with 15 mm/day, 5 days with 5 mm/day, rest dry (0 mm/day)
    pr_vals = np.array([15.0] * 5 + [5.0] * 5 + [0.0] * 356)
    pr = xr.DataArray(
        pr_vals,
        coords={"time": dates},
        dims=["time"],
        name="pr",
        attrs={"units": "mm/day"},
    )

    # Wet days (RR >= 1 mm)
    res_rr1 = indicators.rr1(pr, freq="YS")
    assert np.isclose(res_rr1.values[0], 10.0)

    # Heavy precipitation days (RR >= 10 mm)
    res_r10mm = indicators.r10mm(pr, freq="YS")
    assert np.isclose(res_r10mm.values[0], 5.0)

    # Total precipitation on wet days
    res_prcptot = indicators.prcptot(pr, freq="YS")
    assert np.isclose(res_prcptot.values[0], 100.0)

    # Simple daily intensity index (prcptot / rr1 = 100 / 10 = 10 mm/day)
    res_sdii = indicators.sdii(pr, freq="YS")
    assert np.isclose(res_sdii.values[0], 10.0)


def test_icclim_compound_bivariate_indices() -> None:
    """
    Test bivariate and temperature range indices in icclim.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tx = xr.DataArray(
        np.full(len(dates), 28.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )
    tn = xr.DataArray(
        np.full(len(dates), 14.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmin",
        attrs={"units": "degC"},
    )
    pr = xr.DataArray(
        np.full(len(dates), 5.0),
        coords={"time": dates},
        dims=["time"],
        name="pr",
        attrs={"units": "mm/day"},
    )

    # Diurnal temperature range (TX - TN = 14)
    res_dtr = indicators.dtr(tasmax=tx, tasmin=tn, freq="YS")
    assert np.isclose(res_dtr.values[0], 14.0)

    # Extreme temperature range
    res_etr = indicators.etr(tasmax=tx, tasmin=tn, freq="YS")
    assert np.isclose(res_etr.values[0], 14.0)

    # Bivariate warm and wet days (WW)
    res_ww = indicators.ww(tas=tx, pr=pr, freq="YS")
    assert isinstance(res_ww, xr.DataArray)
    assert res_ww.name == "WW"


def test_icclim_xclim_equivalence_fixed_thresholds() -> None:
    """
    Verify numerical equivalence between homologous icclim and xclim indicators.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tn = xr.DataArray(
        np.full(len(dates), -5.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmin",
        attrs={"units": "degC"},
    )
    pr = xr.DataArray(
        np.zeros(len(dates)),
        coords={"time": dates},
        dims=["time"],
        name="pr",
        attrs={"units": "mm/day"},
    )

    # Frost days: icclim fd vs xclim frost_days
    res_icclim_fd = indicators.fd(tn, freq="YS")
    res_xclim_fd = indicators.frost_days(tn, freq="YS")
    np.testing.assert_allclose(res_icclim_fd.values, res_xclim_fd.values)

    # Maximum consecutive dry days: icclim cdd vs xclim maximum_consecutive_dry_days
    res_icclim_cdd = indicators.cdd(pr, freq="YS")
    res_xclim_cdd = indicators.maximum_consecutive_dry_days(pr, freq="YS")
    np.testing.assert_allclose(res_icclim_cdd.values, res_xclim_cdd.values)


def test_percentile_backend_numerical_agreement() -> None:
    """
    Verify numerical consistency between backend='icclim' and backend='xclim' for tx90p.

    Returns
    -------
    None
    """
    dates = pd.date_range("1990-01-01", "1995-12-31", freq="D")
    np.random.seed(42)
    temp_vals = 15.0 + 10.0 * np.sin(2 * np.pi * dates.dayofyear / 365.25) + np.random.normal(0, 2, len(dates))
    tasmax = xr.DataArray(
        temp_vals,
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )

    # Backend icclim computes percentiles on-the-fly across the reference period
    res_icclim = indicators.tx90p(
        tasmax,
        base_period_time_range=["1990-01-01", "1995-12-31"],
        freq="YS",
        backend="icclim",
    )

    # Backend xclim takes precomputed DOY percentiles
    base_slice = tasmax.sel(time=slice("1990-01-01", "1995-12-31"))
    per_doy = xcal.percentile_doy(base_slice, per=90, window=5)
    res_xclim = indicators.tx90p(
        tasmax,
        tasmax_per=per_doy,
        freq="YS",
        backend="xclim",
    )

    np.testing.assert_allclose(res_icclim.values, res_xclim.values.squeeze(), atol=1.0)


def test_icclim_dask_lazy_evaluation() -> None:
    """
    Verify that icclim indicators preserve Dask chunking and lazy execution.

    Returns
    -------
    None
    """
    dates = pd.date_range("2020-01-01", periods=366, freq="D")
    tx = xr.DataArray(
        np.full(len(dates), 28.0),
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={"units": "degC"},
    )
    tx_chunked = tx.chunk({"time": 60})

    res_lazy = indicators.su(tx_chunked, freq="YS")
    assert hasattr(res_lazy.data, "dask")

    computed = res_lazy.compute()
    assert isinstance(computed, xr.DataArray)
    assert not hasattr(computed.data, "dask")
    assert np.isclose(computed.values[0], 366.0)
