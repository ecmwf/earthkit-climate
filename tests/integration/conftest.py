# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Shared Pytest fixtures for integration tests."""

from contextlib import nullcontext
from typing import Any, Callable, Optional

import pytest
import xarray as xr

import earthkit.climate.indicators.atmos.precipitation as ek_pr
import earthkit.climate.indicators.atmos.temperature as ek_temp
from earthkit.climate.datasets import load_sample_datasets
from earthkit.climate.utils import percentile_doy


def _run_indicator(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    use_flox: Optional[bool] = None,
) -> Any:
    """
    Execute a climate indicator function with configurable xarray flox backend.

    Parameters
    ----------
    func : callable
        The indicator function to execute (earthkit or xclim).
    kwargs : dict[str, Any]
        Keyword arguments forwarded to *func*.
    use_flox : bool or None
        If True/False, sets xarray's ``use_flox`` option for the call.

    Returns
    -------
    Any
        The result returned by *func* (typically an xr.DataArray or Dataset).
    """
    ctx = xr.set_options(use_flox=use_flox) if use_flox is not None else nullcontext()
    with ctx:
        return func(**kwargs)


def get_indicator_configs(
    data_cache: dict[str, xr.Dataset],
) -> list[dict[str, Any]]:
    """
    Construct the list of benchmarks sharing data and indicator configs.

    Parameters
    ----------
    data_cache : dict[str, xr.Dataset]
        Dictionary of loaded datasets.

    Returns
    -------
    list[dict[str, Any]]
        List of benchmark/test configurations.
    """
    import xclim.indicators

    tasmax_ssp = data_cache["tasmax_ACCESS-CM2_ssp585_far_future"]["tasmax"]
    tasmin_ssp = data_cache["tasmin_ACCESS-CM2_ssp585_far_future"]["tasmin"]
    pr_ssp = data_cache["pr_ACCESS-CM2_ssp585_far_future"]["pr"]

    # Pre-calculate percentile for WSDI
    per_90: xr.DataArray = percentile_doy(data_cache["tasmax_ACCESS-CM2_historical_reference"]["tasmax"], per=90)
    per_90.name = "tasmax_per"

    # Optimized views (Chunk -1)
    tasmax_opt = tasmax_ssp.chunk({"time": -1})

    return [
        {
            "name": "TX90P",
            "ek_func": ek_temp.tx90p,
            "xi_func": xclim.indicators.atmos.tx90p,
            "ek_args": {
                "lazy": {"ds": xr.merge([tasmax_ssp, per_90]), "freq": "MS"},
                "optimized": {
                    "ds": xr.merge([tasmax_opt, per_90]).chunk({"time": -1}),
                    "freq": "MS",
                },
            },
            "xi_args": {
                "lazy": {"tasmax": tasmax_ssp, "tasmax_per": per_90, "freq": "MS"},
                "optimized": {
                    "tasmax": tasmax_opt,
                    "tasmax_per": per_90,
                    "freq": "MS",
                },
            },
        },
        {
            "name": "PRCPTOT",
            "ek_func": ek_pr.precip_accumulation,
            "xi_func": xclim.indicators.atmos.precip_accumulation,
            "ek_args": {
                "lazy": {"ds": pr_ssp, "freq": "MS"},
                "optimized": {"ds": pr_ssp, "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"pr": pr_ssp, "freq": "MS"},
                "optimized": {"pr": pr_ssp, "freq": "MS"},
            },
        },
        {
            "name": "DTR",
            "ek_func": ek_temp.daily_temperature_range,
            "xi_func": xclim.indicators.atmos.daily_temperature_range,
            "ek_args": {
                "lazy": {"ds": xr.merge([tasmax_ssp, tasmin_ssp]), "freq": "MS"},
                "optimized": {"ds": xr.merge([tasmax_ssp, tasmin_ssp]), "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"tasmax": tasmax_ssp, "tasmin": tasmin_ssp, "freq": "MS"},
                "optimized": {"tasmax": tasmax_ssp, "tasmin": tasmin_ssp, "freq": "MS"},
            },
        },
        {
            "name": "HDD",
            "ek_func": ek_temp.heating_degree_days,
            "xi_func": xclim.indicators.atmos.heating_degree_days,
            "ek_args": {
                "lazy": {
                    "ds": ((tasmax_ssp + tasmin_ssp) / 2).to_dataset(name="tas"),
                    "freq": "MS",
                },
                "optimized": {
                    "ds": ((tasmax_ssp + tasmin_ssp) / 2).to_dataset(name="tas"),
                    "freq": "MS",
                },
            },
            "xi_args": {
                "lazy": {"tas": (tasmax_ssp + tasmin_ssp) / 2, "freq": "MS"},
                "optimized": {"tas": (tasmax_ssp + tasmin_ssp) / 2, "freq": "MS"},
            },
        },
        {
            "name": "SDII",
            "ek_func": ek_pr.daily_pr_intensity,
            "xi_func": xclim.indicators.atmos.daily_pr_intensity,
            "ek_args": {
                "lazy": {"ds": pr_ssp, "freq": "MS"},
                "optimized": {"ds": pr_ssp, "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"pr": pr_ssp, "freq": "MS"},
                "optimized": {"pr": pr_ssp, "freq": "MS"},
            },
        },
    ]


@pytest.fixture(scope="session")
def data_cache() -> dict[str, xr.Dataset]:
    """
    Download or use cached CMIP6 datasets required for integration tests.

    Returns
    -------
    dict[str, xr.Dataset]
        Mapping from short name to xarray Dataset.
    """
    return load_sample_datasets()


@pytest.fixture(
    params=["TX90P", "PRCPTOT", "DTR", "HDD", "SDII"],
    ids=["TX90P", "PRCPTOT", "DTR", "HDD", "SDII"],
)
def indicator_config(
    request: pytest.FixtureRequest,
    data_cache: dict[str, xr.Dataset],
) -> dict[str, Any]:
    """
    Build the indicator configuration for parameterized tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest fixture request.
    data_cache : dict[str, xr.Dataset]
        Session-scoped mapping of downloaded CMIP6 datasets.

    Returns
    -------
    dict[str, Any]
        Configuration for the specific indicator.
    """
    name: str = request.param
    configs = get_indicator_configs(data_cache)
    config = next(c for c in configs if c["name"] == name)
    return config
