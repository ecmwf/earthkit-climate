# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Utilities to bridge Earthkit data objects and xarray structures."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

import xarray

import earthkit.data as ekd

EarthkitData = ekd.FieldList | ekd.Field
MetadataDict = Dict[str, Any]


def to_xarray_dataset(
    earthkit_input: EarthkitData | xarray.Dataset,
    metadata: Mapping[str, Any] | None = None,
) -> Tuple[xarray.Dataset, MetadataDict]:
    """
    Convert Earthkit-like data to an ``xarray.Dataset`` and gather metadata.

    Parameters
    ----------
    earthkit_input : EarthkitData | xarray.Dataset
        Input data in any supported Earthkit or xarray representation.
    metadata : Mapping[str, Any], optional
        Existing metadata to propagate and enrich during the conversion.

    Returns
    -------
    tuple[xr.Dataset, dict[str, Any]]
        Dataset ready to be consumed by xclim and an updated metadata mapping.

    Raises
    ------
    TypeError
        If the input cannot be converted to an ``xarray.Dataset``.
    """
    meta: MetadataDict = dict(metadata or {})
    earthkit_internal = dict(meta.get("earthkit_internal", {}))
    earthkit_internal["input_type"] = _describe_type(earthkit_input)

    if isinstance(earthkit_input, xarray.Dataset):
        dataset = earthkit_input
    elif isinstance(earthkit_input, xarray.DataArray):
        variable_name = earthkit_input.name or "variable"
        dataset = earthkit_input.to_dataset(name=variable_name)
        earthkit_internal["dataarray_name"] = variable_name
    elif hasattr(earthkit_input, "to_xarray"):
        dataset = earthkit_input.to_xarray()
        if isinstance(dataset, xarray.DataArray):
            variable_name = dataset.name or "variable"
            dataset = dataset.to_dataset(name=variable_name)
            earthkit_internal["dataarray_name"] = variable_name
        elif not isinstance(dataset, xarray.Dataset):
            raise TypeError("The object returned by 'to_xarray' is not an xarray.Dataset instance.")
    else:
        raise TypeError(
            "Unsupported input type for conversion to xarray. "
            "Expected an xarray object or an Earthkit field exposing 'to_xarray'."
        )

    meta["earthkit_internal"] = earthkit_internal
    return dataset, meta


def _describe_type(obj: Any) -> str:
    """
    Return a human-readable description of an object's type, with special handling for xarray objects.

    Parameters
    ----------
    obj : Any
        The object to describe.

    Returns
    -------
    str
        A string describing the object type.
    """
    if isinstance(obj, xarray.Dataset):
        return "xarray.Dataset"
    if isinstance(obj, xarray.DataArray):
        return "xarray.DataArray"
    obj_type = type(obj)
    return f"{obj_type.__module__}.{obj_type.__qualname__}"


def to_earthkit_field(
    output: xarray.Dataset | xarray.DataArray,
    metadata: Mapping[str, Any] | None = None,
) -> EarthkitData:
    """
    Convert an xarray result back into an Earthkit representation.

    Parameters
    ----------
    output : xarray.Dataset or xarray.DataArray
        Resulting data returned by an xclim indicator.
    metadata : Mapping[str, Any], optional
        Provenance metadata gathered during the conversion and call workflow.

    Returns
    -------
    EarthkitData
        The indicator output converted to the closest possible Earthkit type.
    """
    meta: MetadataDict = dict(metadata or {})

    # Ensure we always have a dataset
    dataset: xarray.Dataset
    if isinstance(output, xarray.DataArray):
        dataset = output.to_dataset(name=output.name or "variable")
    else:
        dataset = output

    dataset = dataset.copy()

    # Attach provenance metadata
    provenance = dict(meta)
    if provenance:
        dataset.attrs.setdefault("earthkit_provenance", provenance)

    # --- Use Earthkit’s official wrapper system ---
    ek_object = ekd.from_object(dataset)
    return ek_object
