# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Temperature-based climate indices."""

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def daily_temperature_range(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Compute the daily temperature range (DTR) using the xclim indices module.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input data containing maximum and minimum daily temperature values.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indices.daily_temperature_range`.

    Returns
    -------
    conversions.EarthkitData
        The computed daily temperature range converted back to an Earthkit-compatible type.

    """
    # Create wrapper inside the function
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_temperature_range)
    return wrapper(ds, **kwargs)


def heating_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Compute the Heating Degree Days (HDD) using the approximation method
    from the xclim indicators module.

    This version uses both daily maximum and minimum temperatures, following
    the approach used in :func:`xclim.indicators.atmos.heating_degree_days_approximation`.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Daily maximum, minimum and mean temperature data.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heating_degree_days_approximation`.

        Common arguments include:

        - `thresh` : str, default "18.0 degC"
            Base temperature threshold for heating.
        - `freq` : str, default "YS"
            Frequency for accumulation (e.g., "YS" = yearly sum).

    Returns
    -------
    conversions.EarthkitData
        The computed Heating Degree Days (HDD) converted back to an Earthkit-compatible type.
    """
    # Create wrapper inside the function
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heating_degree_days)
    return wrapper(ds, **kwargs)


def warm_spell_duration_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Compute the Warm Spell Duration Index (WSDI) using the xclim indices module.
    The 90th percentile threshold must be pre-calculated and included in the input dataset `ds`
    as a variable named `{variable}_per` (e.g., `tasmax_per`).

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Daily maximum temperature data for the target period, including the pre-calculated percentile.
    **kwargs : Any
        Additional arguments forwarded to :func:`xclim.indicators.atmos.warm_spell_duration_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed WSDI index as an Earthkit-compatible field.
    """
    # Create wrapper inside the function
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.warm_spell_duration_index)

    return wrapper(earthkit_input=ds, **kwargs)
