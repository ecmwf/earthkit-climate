# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Helpers for collecting provenance information from xclim indicators."""

from __future__ import annotations

import inspect
from typing import Any

import xarray as xr

from earthkit.climate.utils.conversions import MetadataDict


def add_indicator_provenance(
    metadata: MetadataDict,
    indicator: Any,
    dataset: xr.Dataset,
    **kwargs: Any,
) -> MetadataDict:
    """
    Add provenance information from an xclim indicator call to the metadata.

    Parameters
    ----------
    metadata : MetadataDict
        Metadata dictionary to update.
    indicator : Callable
        xclim indicator function used to compute the index.
    dataset : xarray.Dataset
        Dataset passed to the indicator.
    **kwargs : Any
        Keyword arguments passed to the indicator.

    Returns
    -------
    MetadataDict
        The updated metadata dictionary.
    """
    metadata["indicator_definition"] = getattr(indicator, "parameters", None)
    metadata["cf_attrs"] = getattr(indicator, "cf_attrs", None)

    signature = inspect.signature(indicator)
    bound_args = signature.bind_partial(ds=dataset, **kwargs)
    bound_args.apply_defaults()

    metadata["call_info"] = {
        "xclim_function": indicator.compute.__name__,
        "parameters": dict(bound_args.arguments),
    }

    return metadata
