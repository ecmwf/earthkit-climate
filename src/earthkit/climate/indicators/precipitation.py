# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Precipitation indices."""

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def antecedent_precipitation_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Antecedent precipitation index.

    Calculate the running weighted sum of daily precipitation values given a window and
    weighting exponent. This index serves as an indicator for soil moisture.

    **Units:**

    - api: mm

    This function wraps `xclim.indicators.atmos.antecedent_precipitation_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.antecedent_precipitation_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.antecedent_precipitation_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.antecedent_precipitation_index)
    return wrapper(ds, **kwargs)


def maximum_consecutive_dry_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum consecutive dry days.

    The longest number of consecutive days where daily precipitation below a given
    threshold.

    **Units:**

    - cdd: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_dry_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_dry_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.maximum_consecutive_dry_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.maximum_consecutive_dry_days)
    return wrapper(ds, **kwargs)


def cffwis_indices(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Canadian fire weather index system indices.

    Computes the six (6) fire weather indexes, as defined by the Canadian Forest Service: -
    The Drought Code - The Duff-Moisture Code - The Fine Fuel Moisture Code - The Initial
    Spread Index - The Build Up Index - The Fire Weather Index.

    **Units:**

    - dc: dimensionless
    - dmc: dimensionless
    - ffmc: dimensionless
    - isi: dimensionless
    - bui: dimensionless
    - fwi: dimensionless

    This function wraps `xclim.indicators.atmos.cffwis_indices <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cffwis_indices>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cffwis_indices`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cffwis_indices)
    return wrapper(ds, **kwargs)


def cold_and_dry_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold and dry days.

    Number of days with temperature below a given percentile and precipitation below a given
    percentile.

    **Units:**

    - cold_and_dry_days: days

    This function wraps `xclim.indicators.atmos.cold_and_dry_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_and_dry_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_and_dry_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_and_dry_days)
    return wrapper(ds, **kwargs)


def cold_and_wet_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold and wet days.

    Number of days with temperature below a given percentile and precipitation above a given
    percentile.

    **Units:**

    - cold_and_wet_days: days

    This function wraps `xclim.indicators.atmos.cold_and_wet_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_and_wet_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_and_wet_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_and_wet_days)
    return wrapper(ds, **kwargs)


def maximum_consecutive_wet_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum consecutive wet days.

    The longest number of consecutive days where daily precipitation is at or above a given
    threshold.

    **Units:**

    - cwd: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_wet_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_wet_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.maximum_consecutive_wet_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.maximum_consecutive_wet_days)
    return wrapper(ds, **kwargs)


def days_over_precip_doy_thresh(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with precipitation above a given daily percentile.

    Number of days in a period where precipitation is above a given daily percentile and a
    fixed threshold.

    **Units:**

    - days_over_precip_doy_thresh: days

    This function wraps `xclim.indicators.atmos.days_over_precip_doy_thresh <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_over_precip_doy_thresh>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.days_over_precip_doy_thresh`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.days_over_precip_doy_thresh)
    return wrapper(ds, **kwargs)


def days_over_precip_thresh(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with precipitation above a given percentile.

    Number of days in a period where precipitation is above a given percentile, calculated
    over a given period and a fixed threshold.

    **Units:**

    - days_over_precip_thresh: days

    This function wraps `xclim.indicators.atmos.days_over_precip_thresh <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_over_precip_thresh>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.days_over_precip_thresh`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.days_over_precip_thresh)
    return wrapper(ds, **kwargs)


def days_with_snow(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with snowfall.

    Number of days with snow between a lower and upper limit.

    **Units:**

    - days_with_snow: days

    This function wraps `xclim.indicators.atmos.days_with_snow <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_with_snow>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.days_with_snow`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.days_with_snow)
    return wrapper(ds, **kwargs)


def drought_code(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Daily drought code.

    The Drought Index is part of the Canadian Forest-Weather Index system. It is a numerical
    code that estimates the average moisture content of organic layers.

    **Units:**

    - dc: dimensionless

    This function wraps `xclim.indicators.atmos.drought_code <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.drought_code>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.drought_code`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.drought_code)
    return wrapper(ds, **kwargs)


def griffiths_drought_factor(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Griffiths drought factor based on the soil moisture deficit.

    The drought factor is a numeric indicator of the forest fire fuel availability in the
    deep litter bed. It is often used in the calculation of the McArthur Forest Fire Danger
    Index. The method implemented here follows :cite:t:`ffdi-finkele_2006`.

    **Units:**

    - df: dimensionless

    This function wraps `xclim.indicators.atmos.griffiths_drought_factor <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.griffiths_drought_factor>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.griffiths_drought_factor`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.griffiths_drought_factor)
    return wrapper(ds, **kwargs)


def duff_moisture_code(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Duff moisture code (fwi component).

    The duff moisture code is part of the Canadian Forest Fire Weather Index System. It is a
    numeric rating of the average moisture content of loosely compacted organic layers of
    moderate depth.

    **Units:**

    - dmc: dimensionless

    This function wraps `xclim.indicators.atmos.duff_moisture_code <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.duff_moisture_code>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.duff_moisture_code`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.duff_moisture_code)
    return wrapper(ds, **kwargs)


def dry_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of dry days.

    The number of days with daily precipitation under a given threshold.

    **Units:**

    - dry_days: days

    This function wraps `xclim.indicators.atmos.dry_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.dry_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.dry_days)
    return wrapper(ds, **kwargs)


def dry_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Dry spell frequency.

    The frequency of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.dry_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.dry_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.dry_spell_frequency)
    return wrapper(ds, **kwargs)


def dry_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Dry spell maximum length.

    The maximum length of a dry period of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_max_length: days

    This function wraps `xclim.indicators.atmos.dry_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.dry_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.dry_spell_max_length)
    return wrapper(ds, **kwargs)


def dry_spell_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Dry spell total length.

    The total length of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_total_length: days

    This function wraps `xclim.indicators.atmos.dry_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.dry_spell_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.dry_spell_total_length)
    return wrapper(ds, **kwargs)


def dryness_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Dryness index.

    The dryness index is a characterization of the water component in winegrowing regions
    which considers the precipitation and evapotranspiration factors without deduction for
    surface runoff or drainage. Metric originally published in Riou et al. (1994).

    **Units:**

    - dryness_index: mm

    This function wraps `xclim.indicators.atmos.dryness_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dryness_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.dryness_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.dryness_index)
    return wrapper(ds, **kwargs)


def mcarthur_forest_fire_danger_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mcarthur forest fire danger index (ffdi) mark 5.

    The FFDI is a numeric indicator of the potential danger of a forest fire.

    **Units:**

    - ffdi: dimensionless

    This function wraps `xclim.indicators.atmos.mcarthur_forest_fire_danger_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.mcarthur_forest_fire_danger_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.mcarthur_forest_fire_danger_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.mcarthur_forest_fire_danger_index)
    return wrapper(ds, **kwargs)


def first_snowfall(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day where snowfall exceeded a given threshold.

    The first day where snowfall exceeded a given threshold during a time period (the
    threshold can be given as a snowfall flux or a liquid water equivalent snowfall rate).

    **Units:**

    - first_snowfall: dimensionless

    This function wraps `xclim.indicators.atmos.first_snowfall <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_snowfall>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_snowfall`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_snowfall)
    return wrapper(ds, **kwargs)


def fraction_over_precip_doy_thresh(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Fraction of precipitation due to wet days with daily precipitation over a given daily percentile.

    The percentage of the total precipitation over a period occurring for days when the
    precipitation is above a threshold defining wet days and above a given percentile for
    that day.

    **Units:**

    - fraction_over_precip_doy_thresh: dimensionless

    This function wraps `xclim.indicators.atmos.fraction_over_precip_doy_thresh <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fraction_over_precip_doy_thresh>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.fraction_over_precip_doy_thresh`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.fraction_over_precip_doy_thresh)
    return wrapper(ds, **kwargs)


def fraction_over_precip_thresh(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Fraction of precipitation due to wet days with daily precipitation over a given percentile.

    The percentage of the total precipitation over a period occurring for days when the
    precipitation is above a threshold defining wet days and above a given percentile for
    that day.

    **Units:**

    - fraction_over_precip_thresh: dimensionless

    This function wraps `xclim.indicators.atmos.fraction_over_precip_thresh <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fraction_over_precip_thresh>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.fraction_over_precip_thresh`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.fraction_over_precip_thresh)
    return wrapper(ds, **kwargs)


def high_precip_low_temp(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with precipitation and cold temperature.

    Number of days with precipitation above a given threshold and temperature below a given
    threshold.

    **Units:**

    - high_precip_low_temp: days

    This function wraps `xclim.indicators.atmos.high_precip_low_temp <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.high_precip_low_temp>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.high_precip_low_temp`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.high_precip_low_temp)
    return wrapper(ds, **kwargs)


def keetch_byram_drought_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Keetch-byram drought index (kbdi) for soil moisture deficit.

    The KBDI indicates the amount of water necessary to bring the soil moisture content back
    to field capacity. It is often used in the calculation of the McArthur Forest Fire
    Danger Index. The method implemented here follows :cite:t:`ffdi-finkele_2006` but limits
    the maximum KBDI to 203.2 mm, rather than 200 mm, in order to align best with the
    majority of the literature.

    **Units:**

    - kbdi: mm/day

    This function wraps `xclim.indicators.atmos.keetch_byram_drought_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.keetch_byram_drought_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.keetch_byram_drought_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.keetch_byram_drought_index)
    return wrapper(ds, **kwargs)


def last_snowfall(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Last day where snowfall exceeded a given threshold.

    The last day where snowfall exceeded a given threshold during a time period (the
    threshold can be given as a snowfall flux or a liquid water equivalent snowfall rate).

    **Units:**

    - last_snowfall: dimensionless

    This function wraps `xclim.indicators.atmos.last_snowfall <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.last_snowfall>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.last_snowfall`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.last_snowfall)
    return wrapper(ds, **kwargs)


def liquid_precip_ratio(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Fraction of liquid to total precipitation.

    The ratio of total liquid precipitation over the total precipitation. Liquid
    precipitation is approximated from total precipitation on days where temperature is
    above a given threshold.

    **Units:**

    - liquid_precip_ratio: dimensionless

    This function wraps `xclim.indicators.atmos.liquid_precip_ratio <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_ratio>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.liquid_precip_ratio`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.liquid_precip_ratio)
    return wrapper(ds, **kwargs)


def liquid_precip_average(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Averaged liquid precipitation.

    Averaged liquid precipitation. Precipitation is considered liquid when the average daily
    temperature is above a given threshold.

    **Units:**

    - liquidprcpavg: mm

    This function wraps `xclim.indicators.atmos.liquid_precip_average <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_average>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.liquid_precip_average`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.liquid_precip_average)
    return wrapper(ds, **kwargs)


def liquid_precip_accumulation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Total accumulated liquid precipitation.

    Total accumulated liquid precipitation. Precipitation is considered liquid when the
    average daily temperature is above a given threshold.

    **Units:**

    - liquidprcptot: mm

    This function wraps `xclim.indicators.atmos.liquid_precip_accumulation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_accumulation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.liquid_precip_accumulation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.liquid_precip_accumulation)
    return wrapper(ds, **kwargs)


def max_n_day_precipitation_amount(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum n-day total precipitation.

    Maximum of the moving sum of daily precipitation for a given period.

    **Units:**

    - rx{window}day: mm

    This function wraps `xclim.indicators.atmos.max_n_day_precipitation_amount <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_n_day_precipitation_amount>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.max_n_day_precipitation_amount`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.max_n_day_precipitation_amount)
    return wrapper(ds, **kwargs)


def max_pr_intensity(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum precipitation intensity over time window.

    Maximum precipitation intensity over a given rolling time window.

    **Units:**

    - max_pr_intensity: mm h-1

    This function wraps `xclim.indicators.atmos.max_pr_intensity <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_pr_intensity>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.max_pr_intensity`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.max_pr_intensity)
    return wrapper(ds, **kwargs)


def precip_average(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Averaged precipitation (solid and liquid).

    Averaged precipitation. If the average daily temperature is given, the phase parameter
    can be used to restrict the calculation to precipitation of only one phase (liquid or
    solid). Precipitation is considered solid if the average daily temperature is below 0°C
    threshold (and vice versa).

    **Units:**

    - prcpavg: mm

    This function wraps `xclim.indicators.atmos.precip_average <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.precip_average>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.precip_average`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.precip_average)
    return wrapper(ds, **kwargs)


def precip_accumulation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Total accumulated precipitation (solid and liquid).

    Total accumulated precipitation. If the average daily temperature is given, the phase
    parameter can be used to restrict the calculation to precipitation of only one phase
    (liquid or solid). Precipitation is considered solid if the average daily temperature is
    below 0°C (and vice versa).

    **Units:**

    - prcptot: mm

    This function wraps `xclim.indicators.atmos.precip_accumulation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.precip_accumulation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.precip_accumulation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.precip_accumulation)
    return wrapper(ds, **kwargs)


def rain_on_frozen_ground_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of rain on frozen ground days.

    The number of days with rain above a given threshold after a series of seven days with
    average daily temperature below 0°C. Precipitation is assumed to be rain when the daily
    average temperature is above 0°C.

    **Units:**

    - rain_frzgr: days

    This function wraps `xclim.indicators.atmos.rain_on_frozen_ground_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rain_on_frozen_ground_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.rain_on_frozen_ground_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.rain_on_frozen_ground_days)
    return wrapper(ds, **kwargs)


def rain_season(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Rain season.

    Start time, end time and length of the rain season, notably useful for West Africa
    (sivakumar, 1998). The rain season starts with a period of abundant rainfall, followed
    by a period without prolonged dry sequences, which must happen before a given date. The
    rain season stops during a dry period happening after a given date.

    **Units:**

    - rain_season_start: dimensionless
    - rain_season_end: dimensionless
    - rain_season_length: days

    This function wraps `xclim.indicators.atmos.rain_season <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rain_season>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.rain_season`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.rain_season)
    return wrapper(ds, **kwargs)


def rprctot(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Proportion of accumulated precipitation arising from convective processes.

    The proportion of total precipitation due to convective processes. Only days with
    surpassing a minimum precipitation flux are considered.

    **Units:**

    - rprctot: dimensionless

    This function wraps `xclim.indicators.atmos.rprctot <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rprctot>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.rprctot`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.rprctot)
    return wrapper(ds, **kwargs)


def max_1day_precipitation_amount(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum 1-day total precipitation.

    Maximum total daily precipitation for a given period.

    **Units:**

    - rx1day: mm/day

    This function wraps `xclim.indicators.atmos.max_1day_precipitation_amount <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_1day_precipitation_amount>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.max_1day_precipitation_amount`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.max_1day_precipitation_amount)
    return wrapper(ds, **kwargs)


def daily_pr_intensity(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Simple daily intensity index.

    Average precipitation for days with daily precipitation above a given threshold.

    **Units:**

    - sdii: mm d-1

    This function wraps `xclim.indicators.atmos.daily_pr_intensity <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_pr_intensity>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.daily_pr_intensity`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_pr_intensity)
    return wrapper(ds, **kwargs)


def snowfall_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Snowfall frequency.

    Percentage of days with snowfall above a given threshold (either a snowfall flux or a
    liquid water equivalent snowfall rate).

    **Units:**

    - snowfall_frequency: %

    This function wraps `xclim.indicators.atmos.snowfall_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.snowfall_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.snowfall_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.snowfall_frequency)
    return wrapper(ds, **kwargs)


def snowfall_intensity(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Snowfall intensity.

    Mean daily liquid water equivalent snowfall rate above threshold (either a snowfall flux
    or a liquid water equivalent snowfall rate)

    **Units:**

    - snowfall_intensity: mm/day

    This function wraps `xclim.indicators.atmos.snowfall_intensity <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.snowfall_intensity>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.snowfall_intensity`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.snowfall_intensity)
    return wrapper(ds, **kwargs)


def solid_precip_average(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Averaged solid precipitation.

    Averaged solid precipitation. Precipitation is considered solid when the average daily
    temperature is at or below a given threshold.

    **Units:**

    - solidprcpavg: mm

    This function wraps `xclim.indicators.atmos.solid_precip_average <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.solid_precip_average>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.solid_precip_average`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.solid_precip_average)
    return wrapper(ds, **kwargs)


def solid_precip_accumulation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Total accumulated solid precipitation.

    Total accumulated solid precipitation. Precipitation is considered solid when the
    average daily temperature is at or below a given threshold.

    **Units:**

    - solidprcptot: mm

    This function wraps `xclim.indicators.atmos.solid_precip_accumulation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.solid_precip_accumulation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.solid_precip_accumulation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.solid_precip_accumulation)
    return wrapper(ds, **kwargs)


def warm_and_dry_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Warm and dry days.

    Number of days with temperature above a given percentile and precipitation below a given
    percentile.

    **Units:**

    - warm_and_dry_days: days

    This function wraps `xclim.indicators.atmos.warm_and_dry_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.warm_and_dry_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.warm_and_dry_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.warm_and_dry_days)
    return wrapper(ds, **kwargs)


def warm_and_wet_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Warm and wet days.

    Number of days with temperature above a given percentile and precipitation above a given
    percentile.

    **Units:**

    - warm_and_wet_days: days

    This function wraps `xclim.indicators.atmos.warm_and_wet_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.warm_and_wet_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.warm_and_wet_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.warm_and_wet_days)
    return wrapper(ds, **kwargs)


def water_cycle_intensity(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Water cycle intensity.

    The sum of precipitation and actual evapotranspiration.

    **Units:**

    - water_cycle_intensity: mm

    This function wraps `xclim.indicators.atmos.water_cycle_intensity <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.water_cycle_intensity>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.water_cycle_intensity`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.water_cycle_intensity)
    return wrapper(ds, **kwargs)


def wet_precip_accumulation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Total accumulated precipitation (solid and liquid) during wet days.

    Total accumulated precipitation on days with precipitation. A day is considered to have
    precipitation if the precipitation is greater than or equal to a given threshold.

    **Units:**

    - wet_prcptot: mm

    This function wraps `xclim.indicators.atmos.wet_precip_accumulation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_precip_accumulation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wet_precip_accumulation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wet_precip_accumulation)
    return wrapper(ds, **kwargs)


def wet_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Wet spell frequency.

    The frequency of wet periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.wet_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wet_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wet_spell_frequency)
    return wrapper(ds, **kwargs)


def wet_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Wet spell maximum length.

    The maximum length of a wet period of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_max_length: days

    This function wraps `xclim.indicators.atmos.wet_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wet_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wet_spell_max_length)
    return wrapper(ds, **kwargs)


def wet_spell_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Wet spell total length.

    The total length of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_total_length: days

    This function wraps `xclim.indicators.atmos.wet_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wet_spell_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wet_spell_total_length)
    return wrapper(ds, **kwargs)


def wetdays(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of wet days.

    The number of days with daily precipitation at or above a given threshold.

    **Units:**

    - wetdays: days

    This function wraps `xclim.indicators.atmos.wetdays <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wetdays>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wetdays`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wetdays)
    return wrapper(ds, **kwargs)


def wetdays_prop(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Proportion of wet days.

    The proportion of days with daily precipitation at or above a given threshold.

    **Units:**

    - wetdays_prop: 1

    This function wraps `xclim.indicators.atmos.wetdays_prop <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wetdays_prop>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.wetdays_prop`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.wetdays_prop)
    return wrapper(ds, **kwargs)
