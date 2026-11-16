# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr

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
    assert res.values[0] == 366.0
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
    assert res.values[0] == 366.0


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
    assert res.values[0] == 366.0


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
    for index_name in ["su", "fd", "cdd", "rx1day", "rx5day", "dtr", "tx90p"]:
        assert hasattr(_icclim, index_name)
        assert callable(getattr(_icclim, index_name))


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
