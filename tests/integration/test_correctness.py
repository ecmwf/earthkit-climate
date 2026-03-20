# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""
Integration tests for climate indicator correctness.

These tests verify that the earthkit-climate indicators produce results that are
consistent with their xclim counterparts when applied to real CMIP6 datasets.
They run in optimized mode (flox enabled, time axis rechunked to -1).

Run with:
    export PYTHONPATH="."
    pixi run -e dev python -m pytest tests/integration/test_correctness.py -vv
"""

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
    xc_da: xr.DataArray = xc_result

    # --- Assertions ---
    assert isinstance(ek_da, xr.DataArray), f"[{name}] earthkit result is not a DataArray: {type(ek_da)}"
    assert isinstance(xc_da, xr.DataArray), f"[{name}] xclim result is not a DataArray: {type(xc_da)}"
    assert ek_da.size > 0, f"[{name}] earthkit result is empty"
    assert xc_da.size > 0, f"[{name}] xclim result is empty"
    assert ek_da.notnull().any().item(), f"[{name}] earthkit result is all-NaN"
    assert xc_da.notnull().any().item(), f"[{name}] xclim result is all-NaN"

    xr.testing.assert_allclose(ek_da, xc_da, rtol=1e-2)
