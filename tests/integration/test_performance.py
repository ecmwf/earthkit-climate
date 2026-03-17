# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""
Integration tests for climate indicator performance analysis.

Migrated from docs/notebooks/performance_analysis.ipynb.

These tests verify that the earthkit-climate indicators produce results that are
consistent with their xclim counterparts when applied to real CMIP6 datasets
downloaded via earthkit-data. They run in the optimised mode (flox enabled,
time axis rechunked to -1) which avoids the multi-minute timing runs from the
original notebook.

Run with:
    export PYTHONPATH="."
    pixi run -e dev python -m pytest tests/integration/test_performance.py -vv
"""

import os
import warnings
from contextlib import nullcontext
from typing import Any

import earthkit.data
import pytest
import xarray as xr

import earthkit.climate.indicators.precipitation as ek_pr
import earthkit.climate.indicators.temperature as ek_temp
from earthkit.climate.utils.percentile import percentile_doy

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Dataset URLs (same as the notebook)
# ---------------------------------------------------------------------------

_URLS: dict[str, str] = {
    "tasmax_hist": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmax_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_historical.nc"
    ),
    "tasmax_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmax_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
    "tasmin_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmin_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
    "pr_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "pr_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
}


# ---------------------------------------------------------------------------
# Session-scoped fixture: download / cache datasets once per test session
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def data_cache() -> dict[str, xr.Dataset]:
    """
    Download (or use cached) CMIP6 datasets required by the indicator tests.

    Uses earthkit-data's URL source with a user-level cache so that large
    files are only downloaded once across test runs.

    ## Returns

    dict[str, xr.Dataset]
        Mapping from short name to xarray Dataset.
    """
    cache_dir: str = os.path.expanduser("~/.cache/earthkit/data")
    os.makedirs(cache_dir, exist_ok=True)
    earthkit.data.config.set(
        {
            "cache-policy": "user",
            "temporary-directory-root": cache_dir,
        }
    )

    datasets: dict[str, xr.Dataset] = {}
    for key, url in _URLS.items():
        ds = earthkit.data.from_source("url", url).to_xarray()
        datasets[key] = ds
    return datasets


# ---------------------------------------------------------------------------
# Helper: run a climate indicator with optional flox setting
# ---------------------------------------------------------------------------


def _run_indicator(
    func: Any,
    kwargs: dict[str, Any],
    use_flox: bool | None = None,
) -> Any:
    """
    Execute a climate indicator function with configurable xarray flox backend.

    ## Parameters

    func : callable
        The indicator function to execute (earthkit or xclim).
    kwargs : dict[str, Any]
        Keyword arguments forwarded to *func*.
    use_flox : bool or None
        If True/False, sets xarray's ``use_flox`` option for the call.
        If None (default) the environment's current setting is used unchanged.

    ## Returns

    Any
        The result returned by *func* (typically an xr.DataArray or Dataset).
    """
    ctx = xr.set_options(use_flox=use_flox) if use_flox is not None else nullcontext()
    with ctx:
        return func(**kwargs)


# ---------------------------------------------------------------------------
# Parametrised benchmark fixture
# ---------------------------------------------------------------------------


@pytest.fixture(
    params=["WSDI", "CWD", "DTR", "HDD", "SDII"],
    ids=["WSDI", "CWD", "DTR", "HDD", "SDII"],
)
def indicator_config(
    request: pytest.FixtureRequest,
    data_cache: dict[str, xr.Dataset],
) -> dict[str, Any]:
    """
    Build the indicator configuration for the parametrised performance test.

    Mirrors the ``benchmarks`` list from the notebook, but only the *optimised*
    mode (``time: -1`` chunking + flox) is included because that is the
    deterministic variant used for correctness checking.

    ## Parameters

    request : pytest.FixtureRequest
        Pytest fixture request, carries the indicator name via ``request.param``.
    data_cache : dict[str, xr.Dataset]
        Session-scoped mapping of downloaded CMIP6 datasets.

    ## Returns

    dict[str, Any]
        Dictionary with keys ``name``, ``ek_func``, ``xi_func``,
        ``ek_args`` and ``xi_args``.
    """
    import xclim.indicators

    name: str = request.param

    tasmax_ssp = data_cache["tasmax_ssp"]["tasmax"]
    tasmin_ssp = data_cache["tasmin_ssp"]["tasmin"]
    pr_ssp = data_cache["pr_ssp"]["pr"]

    # Rechunk time to -1 for the optimised variant
    tasmax_opt = tasmax_ssp.chunk({"time": -1})
    tasmin_opt = tasmin_ssp.chunk({"time": -1})
    pr_opt = pr_ssp.chunk({"time": -1})

    if name == "WSDI":
        per_90 = percentile_doy(data_cache["tasmax_hist"]["tasmax"], per=90)
        per_90.name = "tasmax_per"
        return {
            "name": name,
            "ek_func": ek_temp.warm_spell_duration_index,
            "xi_func": xclim.indicators.atmos.warm_spell_duration_index,
            "ek_args": {
                "ds": xr.merge([tasmax_opt, per_90]).chunk({"time": -1}),
                "freq": "MS",
            },
            "xi_args": {
                "tasmax": tasmax_opt,
                "tasmax_per": per_90,
                "freq": "MS",
            },
        }

    if name == "CWD":
        return {
            "name": name,
            "ek_func": ek_pr.maximum_consecutive_wet_days,
            "xi_func": xclim.indicators.atmos.maximum_consecutive_wet_days,
            "ek_args": {"ds": pr_opt, "freq": "MS"},
            "xi_args": {"pr": pr_opt, "freq": "MS"},
        }

    if name == "DTR":
        return {
            "name": name,
            "ek_func": ek_temp.daily_temperature_range,
            "xi_func": xclim.indicators.atmos.daily_temperature_range,
            "ek_args": {
                "ds": xr.merge([tasmax_opt, tasmin_opt]),
                "freq": "MS",
            },
            "xi_args": {
                "tasmax": tasmax_opt,
                "tasmin": tasmin_opt,
                "freq": "MS",
            },
        }

    if name == "HDD":
        tas_opt = ((tasmax_opt + tasmin_opt) / 2).chunk({"time": -1})
        return {
            "name": name,
            "ek_func": ek_temp.heating_degree_days,
            "xi_func": xclim.indicators.atmos.heating_degree_days,
            "ek_args": {"ds": tas_opt.to_dataset(name="tas"), "freq": "MS"},
            "xi_args": {"tas": tas_opt, "freq": "MS"},
        }

    if name == "SDII":
        return {
            "name": name,
            "ek_func": ek_pr.daily_pr_intensity,
            "xi_func": xclim.indicators.atmos.daily_pr_intensity,
            "ek_args": {"ds": pr_opt, "freq": "MS"},
            "xi_args": {"pr": pr_opt, "freq": "MS"},
        }

    raise ValueError(f"Unknown indicator: {name}")


# ---------------------------------------------------------------------------
# Main correctness test
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_indicator_correctness(indicator_config: dict[str, Any]) -> None:
    """
    Verify that the earthkit indicator result matches the xclim result.

    Runs both calls in optimised mode (flox=True, time rechunked to -1) and
    asserts:

    * Both results are non-empty xarray DataArrays.
    * Both results contain at least one finite value.
    * The results agree within a relative tolerance of 1 %.

    ## Parameters

    indicator_config : dict[str, Any]
        Configuration dict produced by the ``indicator_config`` fixture.
        Keys: ``name``, ``ek_func``, ``xi_func``, ``ek_args``, ``xi_args``.

    ## Returns

    None
        Asserts raise on failure; the test passes silently on success.
    """
    name: str = indicator_config["name"]

    # --- Run earthkit ---
    ek_result = _run_indicator(
        indicator_config["ek_func"],
        indicator_config["ek_args"],
        use_flox=True,
    )
    if hasattr(ek_result, "compute"):
        ek_result = ek_result.compute()
    if isinstance(ek_result, xr.Dataset):
        # earthkit may return a Dataset; take the first data variable
        ek_da: xr.DataArray = ek_result[list(ek_result.data_vars)[0]]
    else:
        ek_da = ek_result  # type: ignore[assignment]

    # --- Run xclim ---
    xc_result = _run_indicator(
        indicator_config["xi_func"],
        indicator_config["xi_args"],
        use_flox=True,
    )
    if hasattr(xc_result, "compute"):
        xc_result = xc_result.compute()
    xc_da: xr.DataArray = xc_result

    # --- Assertions: both results must be non-empty DataArrays ---
    assert isinstance(ek_da, xr.DataArray), (
        f"[{name}] earthkit result is not a DataArray: {type(ek_da)}"
    )
    assert isinstance(xc_da, xr.DataArray), (
        f"[{name}] xclim result is not a DataArray: {type(xc_da)}"
    )
    assert ek_da.size > 0, f"[{name}] earthkit result is empty"
    assert xc_da.size > 0, f"[{name}] xclim result is empty"
    assert ek_da.notnull().any().item(), f"[{name}] earthkit result is all-NaN"
    assert xc_da.notnull().any().item(), f"[{name}] xclim result is all-NaN"

    # --- Assertions: results agree within 1 % ---
    xr.testing.assert_allclose(ek_da, xc_da, rtol=1e-2)
