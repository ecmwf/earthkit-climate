# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from earthkit.climate import indicators
from earthkit.climate.indicators import icclim


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


def test_icclim_submodule_namespace(synthetic_temp_da: xr.DataArray) -> None:
    """
    Test summer days (su) indicator called via icclim submodule namespace.

    Parameters
    ----------
    synthetic_temp_da : xarray.DataArray
        Synthetic temperature data fixture.

    Returns
    -------
    None
    """
    res = icclim.su(synthetic_temp_da, freq="YS")
    assert isinstance(res, xr.DataArray)
    assert res.name == "SU"
    assert res.values[0] == 366.0


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


def test_icclim_tx90p_available_in_submodule() -> None:
    """
    Test that tx90p is accessible via the icclim submodule for explicit ECA&D calls.

    Returns
    -------
    None
    """
    assert hasattr(icclim, "tx90p")
    assert callable(icclim.tx90p)
