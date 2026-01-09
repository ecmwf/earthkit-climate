# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from functools import wraps
from typing import Any, Callable, Dict, Union

import xarray as xr

from earthkit.climate.utils import conversions, provenance, units


def wrap_xclim_indicator(xclim_fn: Callable) -> Callable:
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
        earthkit_input: Union[conversions.EarthkitData, xr.Dataset],
        *args,
        **kwargs,
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
        metadata: Dict[str, Any] = {}

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
        output_dataset: xr.Dataset = xclim_fn(ds=dataset, *args, **kwargs)

        # --- STEP 3: Provenance & Output ---
        metadata = provenance.add_indicator_provenance(metadata, xclim_fn, dataset, **kwargs)

        return conversions.to_earthkit_field(output_dataset, metadata)

    return wrapper
