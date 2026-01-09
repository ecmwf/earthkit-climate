# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from __future__ import annotations

import inspect
from typing import Any, Dict

import xarray as xr

from earthkit.climate.utils.provenance import add_indicator_provenance


class DummyIndicator:
    """
    Minimal indicator stub exposing parameters, cf_attrs, and a compute method.
    Behaves like an xclim indicator in terms of inspect.signature().
    """

    parameters = {"threshold": {"default": 2.0}, "window": {"default": 3}}
    cf_attrs = [{"standard_name": "dummy"}]

    def compute(self, ds: xr.Dataset, threshold: float = 2.0, window: int = 3) -> xr.DataArray:
        """Fake compute method similar to xclim indicators."""
        return ds[list(ds.data_vars)[0]].mean(dim="time")

    __signature__ = inspect.signature(compute)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the indicator callable, like real xclim indicators."""
        return self.compute(*args, **kwargs)


class NoAttrsIndicator:
    """Stub indicator without parameters or cf_attrs."""

    def compute(self, ds: xr.Dataset, alpha: float = 0.5) -> xr.DataArray:
        return ds[list(ds.data_vars)[0]]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.compute(*args, **kwargs)


def test_populates_indicator_definition_and_cf_attrs() -> None:
    """
    Test that `add_indicator_provenance` correctly populates the metadata with
    the indicator definition and CF attributes when they are present in the indicator.
    """
    ds: xr.Dataset = xr.Dataset({"tas": ("time", [1.0, 2.0, 3.0])}, coords={"time": [0, 1, 2]})
    meta: Dict[str, Any] = {}

    ind = DummyIndicator()
    out: Dict[str, Any] = add_indicator_provenance(meta, ind, ds, threshold=10.0)

    assert out["indicator_definition"] == DummyIndicator.parameters
    assert out["cf_attrs"] == DummyIndicator.cf_attrs


def test_call_info_contains_compute_name_and_bound_args() -> None:
    """
    Test that `add_indicator_provenance` stores function call metadata correctly,
    including the function name and bound parameters (e.g., Dataset and arguments).
    """
    ds: xr.Dataset = xr.Dataset({"pr": ("time", [0.1, 0.2])}, coords={"time": [0, 1]})
    meta: Dict[str, Any] = {}

    ind = DummyIndicator()
    out: Dict[str, Any] = add_indicator_provenance(meta, ind, ds, window=5)

    assert "call_info" in out
    call = out["call_info"]
    assert call["xclim_function"] == ind.compute.__name__
    assert isinstance(call["parameters"]["ds"], xr.Dataset)
    assert call["parameters"]["window"] == 5
    # default threshold applied
    assert call["parameters"]["threshold"] == 2.0


def test_handles_missing_optional_attributes() -> None:
    """
    Test that `add_indicator_provenance` handles indicators without optional
    attributes (`parameters` or `cf_attrs`) without raising errors.
    """
    ds: xr.Dataset = xr.Dataset({"tas": ("time", [1.0])}, coords={"time": [0]})
    meta: Dict[str, Any] = {}

    ind = NoAttrsIndicator()
    out: Dict[str, Any] = add_indicator_provenance(meta, ind, ds)

    assert out["indicator_definition"] is None
    assert out["cf_attrs"] is None
    assert out["call_info"]["xclim_function"] == ind.compute.__name__


def test_uses_indicator_signature() -> None:
    """
    Test that the `compute` method of the indicator exposes the expected
    function signature, including the `ds` parameter.
    """
    ind = DummyIndicator()
    sig = inspect.signature(ind.compute)
    assert "ds" in sig.parameters


def test_mutates_metadata_in_place() -> None:
    """
    Test that `add_indicator_provenance` mutates the provided metadata dictionary
    in place instead of returning a new object.
    """
    ds: xr.Dataset = xr.Dataset({"tas": ("time", [1.0, 2.0])}, coords={"time": [0, 1]})
    meta: Dict[str, Any] = {"pre": True}
    ind = DummyIndicator()

    out: Dict[str, Any] = add_indicator_provenance(meta, ind, ds)
    assert out is meta
    assert "call_info" in meta
