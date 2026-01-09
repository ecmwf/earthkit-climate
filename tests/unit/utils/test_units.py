# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import warnings
from typing import Any

import pytest
import xarray

from earthkit.climate.utils.units import ensure_units


def test_ensure_units_non_strict_overwrites_and_warns() -> None:
    """
    Test that `ensure_units` overwrites units without conversion in non-strict mode
    and emits a warning message.
    """
    ds = xarray.Dataset({"tas": ("time", [273.15, 274.15])})
    ds["tas"].attrs["units"] = "K"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = ensure_units(ds, "tas", "degC", strict=False)
        assert out["tas"].attrs["units"] == "degC"
        assert any("Overwriting without conversion" in str(ww.message) for ww in w)


def test_ensure_units_strict_uses_xclim_convert_units_to(monkeypatch: Any) -> None:
    """
    Test that `ensure_units` calls `convert_units_to` (from xclim) in strict mode,
    performing unit conversion and emitting a conversion warning.
    """
    ds = xarray.Dataset({"tas": ("time", [273.15, 274.15])})
    ds["tas"].attrs["units"] = "K"

    # Mock convert_units_to to avoid requiring pint configuration
    from earthkit.climate.utils import units as units_mod

    def fake_convert(var: xarray.DataArray, units: str) -> xarray.DataArray:
        # fake conversion K -> degC
        data = var - 273.15
        data.attrs = dict(var.attrs)
        data.attrs["units"] = units
        return data

    monkeypatch.setattr(units_mod, "convert_units_to", fake_convert)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = ensure_units(ds, "tas", "degC", strict=True)
        assert pytest.approx(out["tas"].values.tolist()) == [0.0, 1.0]
        assert out["tas"].attrs["units"] == "degC"
        assert any("converted from" in str(ww.message) for ww in w)


def test_ensure_units_strict_raises_on_conversion_error(monkeypatch: Any) -> None:
    """Test that `ensure_units` raises a ValueError when conversion fails in strict mode."""
    ds = xarray.Dataset({"tas": ("time", [1.0, 2.0])})
    ds["tas"].attrs["units"] = "unknown"

    from earthkit.climate.utils import units as units_mod

    def failing_convert(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("no conversion")

    monkeypatch.setattr(units_mod, "convert_units_to", failing_convert)

    with pytest.raises(ValueError) as exc:
        ensure_units(ds, "tas", "degC", strict=True)
    assert "Failed to convert" in str(exc.value)


def test_ensure_units_noop_when_units_already_expected() -> None:
    """
    Test that `ensure_units` does nothing (no conversion or overwrite)
    when the variable already has the expected units.
    """
    ds = xarray.Dataset({"pr": ("time", [0.1, 0.2])})
    ds["pr"].attrs["units"] = "mm/day"
    out = ensure_units(ds, "pr", "mm/day", strict=True)
    # identical object references are ok since we don't copy in function
    assert out["pr"].attrs["units"] == "mm/day"
