# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Temperature indices."""

from typing import Any

import xarray
import xclim.indicators.atmos

import earthkit.climate.utils.conversions as conversions
from earthkit.climate.api.wrapper import wrap_xclim_indicator


def australian_hardiness_zones(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Australian hardiness zones.

    A climate indice based on a multi-year rolling average of the annual minimum
    temperature. Developed specifically to aid in determining plant suitability of
    geographic regions. The Australian National Botanical Gardens (ANBG) classification
    scheme divides categories into 5-degree Celsius zones, starting from -15 degrees Celsius
    and ending at 20 degrees Celsius.

    **Units:**

    - hz: dimensionless

    This function wraps `xclim.indicators.atmos.australian_hardiness_zones <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.australian_hardiness_zones>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.australian_hardiness_zones`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.australian_hardiness_zones)
    return wrapper(ds, **kwargs)


def biologically_effective_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Biologically effective degree days.

    Considers daily minimum and maximum temperature with a given base threshold between 1
    April and 31 October, with a maximum daily value for cumulative degree days (typically
    9°C), and integrates modification coefficients for latitudes between 40°N and 50°N as
    well as for swings in daily temperature range. Metric originally published in Gladstones
    (1992).

    **Units:**

    - bedd: K days

    This function wraps `xclim.indicators.atmos.biologically_effective_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.biologically_effective_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.biologically_effective_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.biologically_effective_degree_days)
    return wrapper(ds, **kwargs)


def cold_spell_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold spell days.

    The number of days that are part of a cold spell. A cold spell is defined as a minimum
    number of consecutive days with mean daily temperature below a given threshold.

    **Units:**

    - cold_spell_days: days

    This function wraps `xclim.indicators.atmos.cold_spell_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_spell_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_spell_days)
    return wrapper(ds, **kwargs)


def cold_spell_duration_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold spell duration index (csdi).

    Number of days part of a percentile-defined cold spell. A cold spell occurs when the
    daily minimum temperature is below a given percentile for a given number of consecutive
    days.

    **Units:**

    - csdi_{window}: days

    This function wraps `xclim.indicators.atmos.cold_spell_duration_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_duration_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_spell_duration_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_spell_duration_index)
    return wrapper(ds, **kwargs)


def cold_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold spell frequency.

    The frequency of cold periods of `N` days or more, during which the temperature over a
    given time window of days is below a given threshold.

    **Units:**

    - cold_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.cold_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_spell_frequency)
    return wrapper(ds, **kwargs)


def cold_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold spell maximum length.

    The maximum length of a cold period of `N` days or more, during which the temperature
    over a given time window of days is below a given threshold.

    **Units:**

    - cold_spell_max_length: days

    This function wraps `xclim.indicators.atmos.cold_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_spell_max_length)
    return wrapper(ds, **kwargs)


def cold_spell_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cold spell total length.

    The total length of cold periods of `N` days or more, during which the temperature over
    a given time window of days is below a given threshold.

    **Units:**

    - cold_spell_total_length: days

    This function wraps `xclim.indicators.atmos.cold_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cold_spell_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cold_spell_total_length)
    return wrapper(ds, **kwargs)


def consecutive_frost_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Consecutive frost days.

    Maximum number of consecutive days where the daily minimum temperature is below 0°C

    **Units:**

    - consecutive_frost_days: days

    This function wraps `xclim.indicators.atmos.consecutive_frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.consecutive_frost_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.consecutive_frost_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.consecutive_frost_days)
    return wrapper(ds, **kwargs)


def maximum_consecutive_frost_free_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum consecutive frost free days.

    Maximum number of consecutive frost-free days: where the daily minimum temperature is
    above or equal to 0°C

    **Units:**

    - consecutive_frost_free_days: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_frost_free_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_frost_free_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.maximum_consecutive_frost_free_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.maximum_consecutive_frost_free_days)
    return wrapper(ds, **kwargs)


def cool_night_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cool night index.

    A night coolness variable which takes into account the mean minimum night temperatures
    during the month when ripening usually occurs beyond the ripening period.

    **Units:**

    - cool_night_index: degC

    This function wraps `xclim.indicators.atmos.cool_night_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cool_night_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cool_night_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cool_night_index)
    return wrapper(ds, **kwargs)


def cooling_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cooling degree days.

    The cumulative degree days for days when the mean daily temperature is above a given
    threshold and buildings must be air conditioned.

    **Units:**

    - cooling_degree_days: K days

    This function wraps `xclim.indicators.atmos.cooling_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cooling_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cooling_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cooling_degree_days)
    return wrapper(ds, **kwargs)


def cooling_degree_days_approximation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Cooling degree days approximation.

    The cumulative degree days for days when temperatures are above a given threshold and
    buildings must be air conditioned. This method integrates mean, minimum, and maximum
    temperatures, accounting for asymmetry in the distributions of temperatures throughout
    the diurnal cycle.

    **Units:**

    - cooling_degree_days_approximation: K days

    This function wraps `xclim.indicators.atmos.cooling_degree_days_approximation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cooling_degree_days_approximation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.cooling_degree_days_approximation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.cooling_degree_days_approximation)
    return wrapper(ds, **kwargs)


def corn_heat_units(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Corn heat units.

    A temperature-based index used to estimate the development of corn crops. Corn growth
    occurs when the daily minimum and maximum temperatures exceed given thresholds.

    **Units:**

    - chu: dimensionless

    This function wraps `xclim.indicators.atmos.corn_heat_units <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.corn_heat_units>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.corn_heat_units`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.corn_heat_units)
    return wrapper(ds, **kwargs)


def chill_portions(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Chill portions.

    Chill portions are a measure to estimate the bud breaking potential of different crops.
    The constants and functions are taken from Luedeling et al. (2009) which formalises the
    method described in Fishman et al. (1987). The model computes the accumulation of cold
    temperatures in a two-step process. First, cold temperatures contribute to an
    intermediate product that is transformed to a chill portion once it exceeds a certain
    concentration. The intermediate product can be broken down at higher temperatures but
    the final product is stable even at higher temperature. Thus the dynamic model is more
    accurate than other chill models like the Chilling hours or Utah model, especially in
    moderate climates like Israel, California or Spain.

    **Units:**

    - cp: dimensionless

    This function wraps `xclim.indicators.atmos.chill_portions <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.chill_portions>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.chill_portions`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.chill_portions)
    return wrapper(ds, **kwargs)


def chill_units(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Chill units.

    Chill units are a measure to estimate the bud breaking potential of different crop based
    on Richardson et al. (1974). The Utah model assigns a weight to each hour depending on
    the temperature recognising that high temperatures can actual decrease, the potential
    for bud breaking. Providing `positive_only=True` will ignore days with negative chill
    units.

    **Units:**

    - cu: dimensionless

    This function wraps `xclim.indicators.atmos.chill_units <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.chill_units>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.chill_units`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.chill_units)
    return wrapper(ds, **kwargs)


def degree_days_exceedance_date(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Degree day exceedance date.

    The day of the year when the sum of degree days exceeds a threshold, occurring after a
    given date. Degree days are calculated above or below a given temperature threshold.

    **Units:**

    - degree_days_exceedance_date: dimensionless

    This function wraps `xclim.indicators.atmos.degree_days_exceedance_date <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.degree_days_exceedance_date>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.degree_days_exceedance_date`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.degree_days_exceedance_date)
    return wrapper(ds, **kwargs)


def daily_freezethaw_cycles(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Daily freeze-thaw cycles.

    The number of days with a freeze-thaw cycle. A freeze-thaw cycle is defined as a day
    where maximum daily temperature is above a given threshold and minimum daily temperature
    is at or below a given threshold, usually 0°C for both.

    **Units:**

    - dlyfrzthw: days

    This function wraps `xclim.indicators.atmos.daily_freezethaw_cycles <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_freezethaw_cycles>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.daily_freezethaw_cycles`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_freezethaw_cycles)
    return wrapper(ds, **kwargs)


def daily_temperature_range(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean of daily temperature range.

    The average difference between the daily maximum and minimum temperatures.

    **Units:**

    - dtr: K

    This function wraps `xclim.indicators.atmos.daily_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_temperature_range>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.daily_temperature_range`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_temperature_range)
    return wrapper(ds, **kwargs)


def max_daily_temperature_range(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum of daily temperature range.

    The maximum difference between the daily maximum and minimum temperatures.

    **Units:**

    - dtrmax: K

    This function wraps `xclim.indicators.atmos.max_daily_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_daily_temperature_range>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.max_daily_temperature_range`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.max_daily_temperature_range)
    return wrapper(ds, **kwargs)


def daily_temperature_range_variability(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Variability of daily temperature range.

    The average day-to-day variation in daily temperature range.

    **Units:**

    - dtrvar: K

    This function wraps `xclim.indicators.atmos.daily_temperature_range_variability <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_temperature_range_variability>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.daily_temperature_range_variability`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.daily_temperature_range_variability)
    return wrapper(ds, **kwargs)


def extreme_temperature_range(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Extreme temperature range.

    The maximum of the maximum temperature minus the minimum of the minimum temperature.

    **Units:**

    - etr: K

    This function wraps `xclim.indicators.atmos.extreme_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.extreme_temperature_range>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.extreme_temperature_range`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.extreme_temperature_range)
    return wrapper(ds, **kwargs)


def fire_season(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Fire season mask.

    Binary mask of the active fire season, defined by conditions on consecutive daily
    temperatures and, optionally, snow depths.

    **Units:**

    - fire_season: dimensionless

    This function wraps `xclim.indicators.atmos.fire_season <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fire_season>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.fire_season`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.fire_season)
    return wrapper(ds, **kwargs)


def first_day_tg_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tg_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tg_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tg_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tg_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tg_above)
    return wrapper(ds, **kwargs)


def first_day_tg_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tg_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tg_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tg_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tg_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tg_below)
    return wrapper(ds, **kwargs)


def first_day_tn_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tn_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tn_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tn_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tn_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tn_above)
    return wrapper(ds, **kwargs)


def first_day_tn_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tn_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tn_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tn_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tn_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tn_below)
    return wrapper(ds, **kwargs)


def first_day_tx_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tx_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tx_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tx_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tx_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tx_above)
    return wrapper(ds, **kwargs)


def first_day_tx_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tx_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tx_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tx_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.first_day_tx_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.first_day_tx_below)
    return wrapper(ds, **kwargs)


def freezethaw_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Freeze-thaw spell frequency.

    Frequency of daily freeze-thaw spells. A freeze-thaw spell is defined as a number of
    consecutive days where maximum daily temperatures are above a given threshold and
    minimum daily temperatures are at or below a given threshold, usually 0°C for both.

    **Units:**

    - freezethaw_spell_frequency: days

    This function wraps `xclim.indicators.atmos.freezethaw_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freezethaw_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.freezethaw_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.freezethaw_spell_frequency)
    return wrapper(ds, **kwargs)


def freezethaw_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximal length of freeze-thaw spells.

    Maximal length of daily freeze-thaw spells. A freeze-thaw spell is defined as a number
    of consecutive days where maximum daily temperatures are above a given threshold and
    minimum daily temperatures are at or below a threshold, usually 0°C for both.

    **Units:**

    - freezethaw_spell_max_length: days

    This function wraps `xclim.indicators.atmos.freezethaw_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freezethaw_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.freezethaw_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.freezethaw_spell_max_length)
    return wrapper(ds, **kwargs)


def freezethaw_spell_mean_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Freeze-thaw spell mean length.

    Average length of daily freeze-thaw spells. A freeze-thaw spell is defined as a number
    of consecutive days where maximum daily temperatures are above a given threshold and
    minimum daily temperatures are at or below a given threshold, usually 0°C for both.

    **Units:**

    - freezethaw_spell_mean_length: days

    This function wraps `xclim.indicators.atmos.freezethaw_spell_mean_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freezethaw_spell_mean_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.freezethaw_spell_mean_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.freezethaw_spell_mean_length)
    return wrapper(ds, **kwargs)


def freezing_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Freezing degree days.

    The cumulative degree days for days when the average temperature is below a given
    threshold, typically 0°C.

    **Units:**

    - freezing_degree_days: K days

    This function wraps `xclim.indicators.atmos.freezing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freezing_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.freezing_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.freezing_degree_days)
    return wrapper(ds, **kwargs)


def freshet_start(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Day of year of spring freshet start.

    Day of year of the spring freshet start, defined as the first day when the temperature
    exceeds a certain threshold for a given number of consecutive days.

    **Units:**

    - freshet_start: dimensionless

    This function wraps `xclim.indicators.atmos.freshet_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freshet_start>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.freshet_start`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.freshet_start)
    return wrapper(ds, **kwargs)


def frost_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost days.

    Number of days where the daily minimum temperature is below a given threshold.

    **Units:**

    - frost_days: days

    This function wraps `xclim.indicators.atmos.frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_days)
    return wrapper(ds, **kwargs)


def frost_free_season_end(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost free season end.

    First day when the temperature is below a given threshold for a given number of
    consecutive days after a median calendar date.

    **Units:**

    - frost_free_season_end: dimensionless

    This function wraps `xclim.indicators.atmos.frost_free_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_season_end>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_free_season_end`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_free_season_end)
    return wrapper(ds, **kwargs)


def frost_free_season_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost free season length.

    Duration of the frost free season, defined as the period when the minimum daily
    temperature is above 0°C without a freezing window of `N` days, with freezing occurring
    after a median calendar date.

    **Units:**

    - frost_free_season_length: days

    This function wraps `xclim.indicators.atmos.frost_free_season_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_season_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_free_season_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_free_season_length)
    return wrapper(ds, **kwargs)


def frost_free_season_start(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost free season start.

    First day when minimum daily temperature exceeds a given threshold for a given number of
    consecutive days

    **Units:**

    - frost_free_season_start: dimensionless

    This function wraps `xclim.indicators.atmos.frost_free_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_season_start>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_free_season_start`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_free_season_start)
    return wrapper(ds, **kwargs)


def frost_free_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost free spell maximum length.

    The maximum length of a frost free period of `N` days or more, during which the minimum
    temperature over a given time window of days is above a given threshold.

    **Units:**

    - frost_free_spell_max_length: days

    This function wraps `xclim.indicators.atmos.frost_free_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_free_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_free_spell_max_length)
    return wrapper(ds, **kwargs)


def frost_season_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Frost season length.

    Duration of the freezing season, defined as the period when the daily minimum
    temperature is below 0°C without a thawing window of days, with the thaw occurring after
    a median calendar date.

    **Units:**

    - frost_season_length: days

    This function wraps `xclim.indicators.atmos.frost_season_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_season_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.frost_season_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.frost_season_length)
    return wrapper(ds, **kwargs)


def growing_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Growing degree days.

    The cumulative degree days for days when the average temperature is above a given
    threshold.

    **Units:**

    - growing_degree_days: K days

    This function wraps `xclim.indicators.atmos.growing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.growing_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.growing_degree_days)
    return wrapper(ds, **kwargs)


def growing_season_end(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Growing season end.

    The first day when the temperature is below a certain threshold for a certain number of
    consecutive days after a given calendar date.

    **Units:**

    - growing_season_end: dimensionless

    This function wraps `xclim.indicators.atmos.growing_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_season_end>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.growing_season_end`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.growing_season_end)
    return wrapper(ds, **kwargs)


def growing_season_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Growing season length.

    Number of days between the first occurrence of a series of days with a daily average
    temperature above a threshold and the first occurrence of a series of days with a daily
    average temperature below that same threshold, occurring after a given calendar date.

    **Units:**

    - growing_season_length: days

    This function wraps `xclim.indicators.atmos.growing_season_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_season_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.growing_season_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.growing_season_length)
    return wrapper(ds, **kwargs)


def growing_season_start(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Growing season start.

    The first day when the temperature exceeds a certain threshold for a given number of
    consecutive days.

    **Units:**

    - growing_season_start: dimensionless

    This function wraps `xclim.indicators.atmos.growing_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_season_start>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.growing_season_start`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.growing_season_start)
    return wrapper(ds, **kwargs)


def heat_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat spell frequency.

    Number of heat spells. A heat spell occurs when rolling averages of daily minimum and
    maximumtemperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.heat_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_spell_frequency)
    return wrapper(ds, **kwargs)


def heat_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat spell maximum length.

    The longest heat spell of a period. A heat spell occurs when rolling averages of daily
    minimum and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_max_length: days

    This function wraps `xclim.indicators.atmos.heat_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_spell_max_length)
    return wrapper(ds, **kwargs)


def heat_spell_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat spell total length.

    Total length of heat spells. A heat spell occurs when rolling averages of daily minimum
    and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_total_length: days

    This function wraps `xclim.indicators.atmos.heat_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_spell_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_spell_total_length)
    return wrapper(ds, **kwargs)


def heat_wave_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat wave frequency.

    Number of heat waves. A heat wave occurs when daily minimum and maximum temperatures
    exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.heat_wave_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_wave_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_wave_frequency)
    return wrapper(ds, **kwargs)


def heat_wave_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat wave index.

    Number of days that constitute heatwave events. A heat wave occurs when daily minimum
    and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_index: days

    This function wraps `xclim.indicators.atmos.heat_wave_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_wave_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_wave_index)
    return wrapper(ds, **kwargs)


def heat_wave_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat wave maximum length.

    Maximal duration of heat waves. A heat wave occurs when daily minimum and maximum
    temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_max_length: days

    This function wraps `xclim.indicators.atmos.heat_wave_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_wave_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_wave_max_length)
    return wrapper(ds, **kwargs)


def heat_wave_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heat wave total length.

    Total length of heat waves. A heat wave occurs when daily minimum and maximum
    temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_total_length: days

    This function wraps `xclim.indicators.atmos.heat_wave_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heat_wave_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heat_wave_total_length)
    return wrapper(ds, **kwargs)


def heating_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heating degree days.

    The cumulative degree days for days when the mean daily temperature is below a given
    threshold and buildings must be heated.

    **Units:**

    - heating_degree_days: K days

    This function wraps `xclim.indicators.atmos.heating_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heating_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heating_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heating_degree_days)
    return wrapper(ds, **kwargs)


def heating_degree_days_approximation(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Heating degree days approximation.

    The cumulative degree days for days where temperatures are below a given threshold and
    buildings must be heated. This method integrates mean, minimum, and maximum
    temperatures, accounting for asymmetry in the distributions of temperatures throughout
    the diurnal cycle.

    **Units:**

    - heating_degree_days_approximation: K days

    This function wraps `xclim.indicators.atmos.heating_degree_days_approximation <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heating_degree_days_approximation>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.heating_degree_days_approximation`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.heating_degree_days_approximation)
    return wrapper(ds, **kwargs)


def hot_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Hot days.

    Number of days where the daily maximum temperature is above a given threshold.

    **Units:**

    - hot_days: days

    This function wraps `xclim.indicators.atmos.hot_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.hot_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.hot_days)
    return wrapper(ds, **kwargs)


def hot_spell_frequency(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Hot spell frequency.

    The frequency of hot periods of `N` days or more, during which the temperature over a
    given time window of days is above a given threshold.

    **Units:**

    - hot_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.hot_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_frequency>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.hot_spell_frequency`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.hot_spell_frequency)
    return wrapper(ds, **kwargs)


def hot_spell_max_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Hot spell maximum length.

    The maximum length of a hot period of `N` days or more, during which the temperature
    over a given time window of days is above a given threshold.

    **Units:**

    - hot_spell_max_length: days

    This function wraps `xclim.indicators.atmos.hot_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_max_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.hot_spell_max_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.hot_spell_max_length)
    return wrapper(ds, **kwargs)


def hot_spell_max_magnitude(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Hot spell maximum magnitude.

    Magnitude of the most intensive heat wave per {freq}. A heat wave occurs when daily
    maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - hot_spell_max_magnitude: K d

    This function wraps `xclim.indicators.atmos.hot_spell_max_magnitude <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_max_magnitude>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.hot_spell_max_magnitude`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.hot_spell_max_magnitude)
    return wrapper(ds, **kwargs)


def hot_spell_total_length(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Hot spell total length.

    The total length of hot periods of `N` days or more, during which the temperature over a
    given time window of days is above a given threshold.

    **Units:**

    - hot_spell_total_length: days

    This function wraps `xclim.indicators.atmos.hot_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_total_length>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.hot_spell_total_length`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.hot_spell_total_length)
    return wrapper(ds, **kwargs)


def huglin_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Huglin heliothermal index.

    Heat-summation index for agroclimatic suitability estimation, developed specifically for
    viticulture. Considers daily minimum and maximum temperature with a given base
    threshold, typically between 1 April and 30September, and integrates a day-length
    coefficient calculation for higher latitudes. Metric originally published in Huglin
    (1978). Day-length coefficient based on Hall & Jones (2010).

    **Units:**

    - hi: dimensionless

    This function wraps `xclim.indicators.atmos.huglin_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.huglin_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.huglin_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.huglin_index)
    return wrapper(ds, **kwargs)


def ice_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Ice days.

    Number of days where the daily maximum temperature is below 0°C

    **Units:**

    - ice_days: days

    This function wraps `xclim.indicators.atmos.ice_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.ice_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.ice_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.ice_days)
    return wrapper(ds, **kwargs)


def last_spring_frost(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Last spring frost.

    The last day when minimum temperature is below a given threshold for a certain number of
    days, limited by a final calendar date.

    **Units:**

    - last_spring_frost: dimensionless

    This function wraps `xclim.indicators.atmos.last_spring_frost <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.last_spring_frost>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.last_spring_frost`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.last_spring_frost)
    return wrapper(ds, **kwargs)


def late_frost_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Late frost days.

    Number of days where the daily minimum temperature is below a given threshold between a
    givenstart date and a given end date.

    **Units:**

    - late_frost_days: days

    This function wraps `xclim.indicators.atmos.late_frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.late_frost_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.late_frost_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.late_frost_days)
    return wrapper(ds, **kwargs)


def latitude_temperature_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Latitude temperature index.

    A climate indice based on mean temperature of the warmest month and a latitude-based
    coefficient to account for longer day-length favouring growing conditions. Developed
    specifically for viticulture. Mean temperature of warmest month multiplied by the
    difference of latitude factor coefficient minus latitude. Metric originally published in
    Jackson, D. I., & Cherry, N. J. (1988).

    **Units:**

    - lti: dimensionless

    This function wraps `xclim.indicators.atmos.latitude_temperature_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.latitude_temperature_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.latitude_temperature_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.latitude_temperature_index)
    return wrapper(ds, **kwargs)


def maximum_consecutive_warm_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum consecutive warm days.

    Maximum number of consecutive days where the maximum daily temperature exceeds a certain
    threshold.

    **Units:**

    - maximum_consecutive_warm_days: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_warm_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_warm_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.maximum_consecutive_warm_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.maximum_consecutive_warm_days)
    return wrapper(ds, **kwargs)


def tg10p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with mean temperature below the 10th percentile.

    Number of days with mean temperature below the 10th percentile.

    **Units:**

    - tg10p: days

    This function wraps `xclim.indicators.atmos.tg10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg10p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg10p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg10p)
    return wrapper(ds, **kwargs)


def tg90p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with mean temperature above the 90th percentile.

    Number of days with mean temperature above the 90th percentile.

    **Units:**

    - tg90p: days

    This function wraps `xclim.indicators.atmos.tg90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg90p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg90p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg90p)
    return wrapper(ds, **kwargs)


def tg_days_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with mean temperature above a given threshold.

    The number of days with mean temperature above a given threshold.

    **Units:**

    - tg_days_above: days

    This function wraps `xclim.indicators.atmos.tg_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_days_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg_days_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg_days_above)
    return wrapper(ds, **kwargs)


def tg_days_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with mean temperature below a given threshold.

    The number of days with mean temperature below a given threshold.

    **Units:**

    - tg_days_below: days

    This function wraps `xclim.indicators.atmos.tg_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_days_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg_days_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg_days_below)
    return wrapper(ds, **kwargs)


def tg_max(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum of mean temperature.

    Maximum of daily mean temperature.

    **Units:**

    - tg_max: K

    This function wraps `xclim.indicators.atmos.tg_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_max>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg_max`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg_max)
    return wrapper(ds, **kwargs)


def tg_mean(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean temperature.

    Mean of daily mean temperature.

    **Units:**

    - tg_mean: K

    This function wraps `xclim.indicators.atmos.tg_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_mean>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg_mean`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg_mean)
    return wrapper(ds, **kwargs)


def tg_min(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Minimum of mean temperature.

    Minimum of daily mean temperature.

    **Units:**

    - tg_min: K

    This function wraps `xclim.indicators.atmos.tg_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_min>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tg_min`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tg_min)
    return wrapper(ds, **kwargs)


def thawing_degree_days(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Thawing degree days.

    The cumulative degree days for days when the average temperature is above a given
    threshold, typically 0°C.

    **Units:**

    - thawing_degree_days: K days

    This function wraps `xclim.indicators.atmos.thawing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.thawing_degree_days>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.thawing_degree_days`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.thawing_degree_days)
    return wrapper(ds, **kwargs)


def tn10p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with minimum temperature below the 10th percentile.

    Number of days with minimum temperature below the 10th percentile.

    **Units:**

    - tn10p: days

    This function wraps `xclim.indicators.atmos.tn10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn10p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn10p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn10p)
    return wrapper(ds, **kwargs)


def tn90p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with minimum temperature above the 90th percentile.

    Number of days with minimum temperature above the 90th percentile.

    **Units:**

    - tn90p: days

    This function wraps `xclim.indicators.atmos.tn90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn90p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn90p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn90p)
    return wrapper(ds, **kwargs)


def tn_days_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with minimum temperature above a given threshold.

    The number of days with minimum temperature above a given threshold.

    **Units:**

    - tn_days_above: days

    This function wraps `xclim.indicators.atmos.tn_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_days_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn_days_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn_days_above)
    return wrapper(ds, **kwargs)


def tn_days_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with minimum temperature below a given threshold.

    The number of days with minimum temperature below a given threshold.

    **Units:**

    - tn_days_below: days

    This function wraps `xclim.indicators.atmos.tn_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_days_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn_days_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn_days_below)
    return wrapper(ds, **kwargs)


def tn_max(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum of minimum temperature.

    Maximum of daily minimum temperature.

    **Units:**

    - tn_max: K

    This function wraps `xclim.indicators.atmos.tn_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_max>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn_max`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn_max)
    return wrapper(ds, **kwargs)


def tn_mean(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean of minimum temperature.

    Mean of daily minimum temperature.

    **Units:**

    - tn_mean: K

    This function wraps `xclim.indicators.atmos.tn_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_mean>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn_mean`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn_mean)
    return wrapper(ds, **kwargs)


def tn_min(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Minimum temperature.

    Minimum of daily minimum temperature.

    **Units:**

    - tn_min: K

    This function wraps `xclim.indicators.atmos.tn_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_min>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tn_min`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tn_min)
    return wrapper(ds, **kwargs)


def tropical_nights(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Tropical nights.

    Number of days where minimum temperature is above a given threshold.

    **Units:**

    - tropical_nights: days

    This function wraps `xclim.indicators.atmos.tropical_nights <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tropical_nights>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tropical_nights`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tropical_nights)
    return wrapper(ds, **kwargs)


def tx10p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with maximum temperature below the 10th percentile.

    Number of days with maximum temperature below the 10th percentile.

    **Units:**

    - tx10p: days

    This function wraps `xclim.indicators.atmos.tx10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx10p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx10p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx10p)
    return wrapper(ds, **kwargs)


def tx90p(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Days with maximum temperature above the 90th percentile.

    Number of days with maximum temperature above the 90th percentile.

    **Units:**

    - tx90p: days

    This function wraps `xclim.indicators.atmos.tx90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx90p>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx90p`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx90p)
    return wrapper(ds, **kwargs)


def tx_days_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with maximum temperature above a given threshold.

    The number of days with maximum temperature above a given threshold.

    **Units:**

    - tx_days_above: days

    This function wraps `xclim.indicators.atmos.tx_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_days_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_days_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_days_above)
    return wrapper(ds, **kwargs)


def tx_days_below(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with maximum temperature below a given threshold.

    The number of days with maximum temperature below a given threshold.

    **Units:**

    - tx_days_below: days

    This function wraps `xclim.indicators.atmos.tx_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_days_below>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_days_below`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_days_below)
    return wrapper(ds, **kwargs)


def tx_max(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Maximum temperature.

    Maximum of daily maximum temperature.

    **Units:**

    - tx_max: K

    This function wraps `xclim.indicators.atmos.tx_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_max>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_max`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_max)
    return wrapper(ds, **kwargs)


def tx_mean(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Mean of maximum temperature.

    Mean of daily maximum temperature.

    **Units:**

    - tx_mean: K

    This function wraps `xclim.indicators.atmos.tx_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_mean>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_mean`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_mean)
    return wrapper(ds, **kwargs)


def tx_min(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Minimum of maximum temperature.

    Minimum of daily maximum temperature.

    **Units:**

    - tx_min: K

    This function wraps `xclim.indicators.atmos.tx_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_min>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_min`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_min)
    return wrapper(ds, **kwargs)


def tx_tn_days_above(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Number of days with daily minimum and maximum temperatures exceeding thresholds.

    Number of days with daily maximum and minimum temperatures above given thresholds.

    **Units:**

    - tx_tn_days_above: days

    This function wraps `xclim.indicators.atmos.tx_tn_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_tn_days_above>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.tx_tn_days_above`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.tx_tn_days_above)
    return wrapper(ds, **kwargs)


def usda_hardiness_zones(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Usda hardiness zones.

    A climate indice based on a multi-year rolling average of the annual minimum
    temperature. Developed specifically to aid in determining plant suitability of
    geographic regions. The USDA classificationscheme divides categories into 10 degree
    Fahrenheit zones, with 5-degree Fahrenheit half-zones, starting from -65 degrees
    Fahrenheit and ending at 65 degrees Fahrenheit.

    **Units:**

    - hz: dimensionless

    This function wraps `xclim.indicators.atmos.usda_hardiness_zones <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.usda_hardiness_zones>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.usda_hardiness_zones`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.usda_hardiness_zones)
    return wrapper(ds, **kwargs)


def warm_spell_duration_index(
    ds: conversions.EarthkitData | xarray.Dataset,
    **kwargs: Any,
) -> conversions.EarthkitData:
    """
    Warm spell duration index.

    Number of days part of a percentile-defined warm spell. A warm spell occurs when the
    maximum daily temperature is above a given percentile for a given number of consecutive
    days.

    **Units:**

    - warm_spell_duration_index: days

    This function wraps `xclim.indicators.atmos.warm_spell_duration_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.warm_spell_duration_index>`_.

    Parameters
    ----------
    ds : conversions.EarthkitData | xarray.Dataset
        Input dataset. See xclim documentation for required variables.
    **kwargs : Any
        Additional keyword arguments forwarded to
        :func:`xclim.indicators.atmos.warm_spell_duration_index`.

    Returns
    -------
    conversions.EarthkitData
        The computed index as an Earthkit-compatible field.
    """
    wrapper = wrap_xclim_indicator(xclim.indicators.atmos.warm_spell_duration_index)
    return wrapper(ds, **kwargs)
