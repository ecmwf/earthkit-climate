# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import pytest
import xarray as xr

from .conftest import _run_indicator


@pytest.mark.integration
def test_indicator_correctness(indicator_config: dict[str, Any]) -> None:
    """
    Verify that the earthkit indicator result matches the xclim result.

    Parameters
    ----------
    indicator_config : dict[str, Any]
        Configuration dict produced by the ``indicator_config`` fixture.

    Returns
    -------
    None
    """
    name: str = indicator_config["name"]

    # --- Run earthkit ---
    ek_result = _run_indicator(
        indicator_config["ek_func"],
        indicator_config["ek_args"]["optimized"],
        use_flox=True,
    )
    if hasattr(ek_result, "compute"):
        ek_result = ek_result.compute()
    if isinstance(ek_result, xr.Dataset):
        ek_da: xr.DataArray = ek_result[list(ek_result.data_vars)[0]]
    else:
        ek_da = ek_result

    # --- Run xclim ---
    xc_result = _run_indicator(
        indicator_config["xi_func"],
        indicator_config["xi_args"]["optimized"],
        use_flox=True,
    )
    if hasattr(xc_result, "compute"):
        xc_result = xc_result.compute()
    if isinstance(xc_result, xr.Dataset):
        xc_da: xr.DataArray = xc_result[list(xc_result.data_vars)[0]]
    else:
        xc_da = xc_result

    # --- Assertions ---
    assert isinstance(ek_da, xr.DataArray), f"[{name}] earthkit result is not a DataArray: {type(ek_da)}"
    assert isinstance(xc_da, xr.DataArray), f"[{name}] xclim result is not a DataArray: {type(xc_da)}"
    assert ek_da.size > 0, f"[{name}] earthkit result is empty"
    assert xc_da.size > 0, f"[{name}] xclim result is empty"
    assert ek_da.notnull().any().item(), f"[{name}] earthkit result is all-NaN"
    assert xc_da.notnull().any().item(), f"[{name}] xclim result is all-NaN"

    xr.testing.assert_allclose(ek_da, xc_da, rtol=1e-2)
