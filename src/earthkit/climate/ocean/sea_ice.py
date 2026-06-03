# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Sea_ice indices."""

from typing import Any

import xarray
import xclim.indicators.seaIce
from earthkit.utils.decorators import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.seaIce.sea_ice_area)
def sea_ice_area(
    siconc: xarray.DataArray | str = "siconc",
    areacello: xarray.DataArray | str = "areacello",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "15 %",
    **kwargs: Any,
) -> Any:
    """
    Sea ice area.

    A measure of total ocean surface covered by sea ice.

    **Units:**

    - sea_ice_area: m2

    This function wraps `xclim.indicators.seaIce.sea_ice_area <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.seaIce.sea_ice_area>`_.

    Parameters
    ----------
    siconc : xarray.DataArray | str
        Sea ice concentration (area fraction).
    areacello : xarray.DataArray | str
        Grid cell area (usually over the ocean).
    thresh : Any
        Minimum sea ice concentration for a grid cell to contribute to the sea ice extent.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.seaIce.sea_ice_area(
        siconc=siconc,
        areacello=areacello,
        thresh=thresh,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.seaIce.sea_ice_extent)
def sea_ice_extent(
    siconc: xarray.DataArray | str = "siconc",
    areacello: xarray.DataArray | str = "areacello",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "15 %",
    **kwargs: Any,
) -> Any:
    """
    Sea ice extent.

    A measure of the extent of all areas where sea ice concentration exceeds a threshold.

    **Units:**

    - sea_ice_extent: m2

    This function wraps `xclim.indicators.seaIce.sea_ice_extent <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.seaIce.sea_ice_extent>`_.

    Parameters
    ----------
    siconc : xarray.DataArray | str
        Sea ice concentration (area fraction).
    areacello : xarray.DataArray | str
        Grid cell area.
    thresh : Any
        Minimum sea ice concentration for a grid cell to contribute to the sea ice extent.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.seaIce.sea_ice_extent(
        siconc=siconc,
        areacello=areacello,
        thresh=thresh,
        ds=ds,
        **kwargs,
    )
