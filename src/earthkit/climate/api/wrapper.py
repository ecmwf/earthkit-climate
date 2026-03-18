# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, Protocol, TypeAlias

import xarray as xr

from ..utils import conversions, provenance, units

IndicatorInput: TypeAlias = conversions.EarthkitData | xr.Dataset


class XclimIndicator(Protocol):
    """Protocol for xclim indicators wrapped by this module."""

    parameters: Any
    cf_attrs: Any
    compute: Any

    def __call__(self, *args: Any, **kwargs: Any) -> xr.Dataset | xr.DataArray: ...


def wrap_xclim_indicator(xclim_fn: XclimIndicator) -> Callable[..., conversions.EarthkitData]:
    """
    Wraps an xclim indicator to handle Earthkit inputs and unit alignment.

    Parameters
    ----------
    xclim_fn : Callable
        The xclim indicator function to be wrapped.

    Returns
    -------
    Callable
        The wrapped function which accepts Earthkit inputs.
    """

    @wraps(xclim_fn)
    def wrapper(
        earthkit_input: IndicatorInput,
        *args: Any,
        **kwargs: Any,
    ) -> conversions.EarthkitData:
        """
        Wrapper function that processes Earthkit inputs and calls the xclim indicator.

        Parameters
        ----------
        earthkit_input : Union[conversions.EarthkitData, xr.Dataset]
            The input data, either as an Earthkit object or an xarray Dataset.
        *args
            Variable length argument list passed to the xclim indicator.
        **kwargs
            Arbitrary keyword arguments passed to the xclim indicator.

        Returns
        -------
        conversions.EarthkitData
            The result of the indicator calculation wrapped as an Earthkit object.
        """
        metadata: conversions.MetadataDict = {}

        # --- STEP 1: Load & Standardize Main Data ---
        # Convert Earthkit object to xarray Dataset
        dataset, metadata = conversions.to_xarray_dataset(earthkit_input, metadata)

        # Standardize units for common variables to Kelvin
        for var in ["tas", "tasmin", "tasmax"]:
            if var in dataset:
                dataset = units.ensure_units(dataset, var, "degC", strict=False)
        if "pr" in dataset:
            dataset = units.ensure_units(dataset, "pr", "mm/day", strict=False)

        # --- STEP 2: Execution ---
        # We pass the single merged dataset (ds) and the variable name mappings
        output_dataset = xclim_fn(ds=dataset, *args, **kwargs)

        # --- STEP 3: Provenance & Output ---
        metadata = provenance.add_indicator_provenance(metadata, xclim_fn, dataset, **kwargs)

        return conversions.to_earthkit_field(output_dataset, metadata)

    return wrapper
