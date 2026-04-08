# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Temperature indices."""

from typing import Any, Literal

import xarray
import xclim.indicators.atmos
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.atmos.australian_hardiness_zones)
def australian_hardiness_zones(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 30,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum temperature.
    window : int
        The length of the averaging window, in years.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.australian_hardiness_zones(
        tasmin=tasmin,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.biologically_effective_degree_days)
def biologically_effective_degree_days(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    lat: xarray.DataArray | str = "lat",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "10 degC",
    method: Literal["gladstones", "icclim", "jones", "smoothed", "stepwise"] = "gladstones",
    cap_value: float = 1.0,
    low_dtr: Any = "10 degC",
    high_dtr: Any = "13 degC",
    max_daily_degree_days: Any = "9 degC",
    start_date: str | str = "04-01",
    end_date: str | str = "11-01",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    lat : xarray.DataArray | str
        Latitude coordinate. If None and method is not "icclim", a CF-conformant "latitude"
        field must be available within the passed DataArray.
    thresh_tasmin : Any
        The minimum temperature threshold.
    method : Literal['gladstones', 'icclim', 'jones', 'smoothed', 'stepwise']
        The formula to use for the daily temperature range and latitude coefficient. The
        "gladstones" method uses a temperature range adjustment and a latitude coefficient
        based on :cite:t:`gladstones_wine_2011`. End_date should be "11-01" for the Northern
        Hemisphere. The "huglin" method uses a temperature range adjustment and a stepwise
        latitude coefficient for values between 40° and 50° based on
        :cite:t:`huglin_nouveau_1978`. End_date should be "11-01" for the Northern
        Hemisphere. The "icclim" method does not implement daily temperature range and nor a
        latitude coefficient based on :cite:t:`project_team_eca&d_algorithm_2013`. End date
        should be "10-01" for the Northern Hemisphere. The "interpolated" method uses a
        temperature range adjustment and a smoothed curve latitude coefficient for values
        between 40° and 50° based on :cite:t:`huglin_nouveau_1978`. The "jones" method uses
        a temperature range adjustment and integrates axial tilt, latitude, and day-of-year
        based on :cite:t:`hall_spatial_2010`. End_date should be "11-01" for the Northern
        Hemisphere.
    cap_value : float
        The value to use for the latitude coefficient for latitudes north of 50°N or south
        of 50°S. Only applicable for methods "huglin" and "interpolated".
    low_dtr : Any
        The lower bound for daily temperature range adjustment.
    high_dtr : Any
        The higher bound for daily temperature range adjustment.
    max_daily_degree_days : Any
        The maximum number of biologically effective degrees days that can be summed daily.
    start_date : str | str
        The hemisphere-based start date to consider (north = April, south = October).
    end_date : str | str
        The hemisphere-based start date to consider (north = October, south = April). This
        date is non-inclusive.
    freq : str
        Resampling frequency (For Southern Hemisphere, should be "YS-JUL").
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.biologically_effective_degree_days(
        tasmin=tasmin,
        tasmax=tasmax,
        lat=lat,
        thresh_tasmin=thresh_tasmin,
        method=method,
        cap_value=cap_value,
        low_dtr=low_dtr,
        high_dtr=high_dtr,
        max_daily_degree_days=max_daily_degree_days,
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_spell_days)
def cold_spell_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "-10 degC",
    window: int = 5,
    freq: str = "YS-JUL",
    op: Literal["<", "lt", "<=", "le"] = "<",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Cold spell days.

    The number of days that are part of a cold spell. A cold spell is defined as a minimum
    number of consecutive days with mean daily temperature below a given threshold.

    **Units:**

    - cold_spell_days: days

    This function wraps `xclim.indicators.atmos.cold_spell_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature below which a cold spell begins.
    window : int
        Minimum number of days with temperature below the threshold to qualify as a cold
        spell.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cold_spell_days(
        tas=tas,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_spell_duration_index)
def cold_spell_duration_index(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmin_per: xarray.DataArray | str = "tasmin_per",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 6,
    freq: str = "YS",
    resample_before_rl: bool = True,
    bootstrap: bool = False,
    op: Literal["<", "<=", "lt", "le"] = "<",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmin_per : xarray.DataArray | str
        The nth percentile of daily minimum temperature with `dayofyear` coordinate.
    window : int
        Minimum number of days with temperature below threshold to qualify as a cold spell.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Keep
        bootstrap to `False` when there is no common period, as bootstrapping is
        computationally expensive, and it might provide the wrong results.
    op : Literal['<', '<=', 'lt', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cold_spell_duration_index(
        tasmin=tasmin,
        tasmin_per=tasmin_per,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_spell_frequency)
def cold_spell_frequency(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "-10 degC",
    window: int = 5,
    freq: str = "YS-JUL",
    op: Literal["<", "lt", "<=", "le"] = "<",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Cold spell frequency.

    The frequency of cold periods of `N` days or more, during which the temperature over a
    given time window of days is below a given threshold.

    **Units:**

    - cold_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.cold_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_frequency>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature below which a cold spell begins.
    window : int
        Minimum number of days with temperature below the threshold to qualify as a cold
        spell.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cold_spell_frequency(
        tas=tas,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_spell_max_length)
def cold_spell_max_length(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "-10 degC",
    window: int = 1,
    freq: str = "YS-JUL",
    op: Literal["<", "lt", "<=", "le"] = "<",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Cold spell maximum length.

    The maximum length of a cold period of `N` days or more, during which the temperature
    over a given time window of days is below a given threshold.

    **Units:**

    - cold_spell_max_length: days

    This function wraps `xclim.indicators.atmos.cold_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_max_length>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a cold spell.
    window : int
        Minimum number of days with temperatures below the threshold to qualify as a cold
        spell.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cold_spell_max_length(
        tas=tas,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_spell_total_length)
def cold_spell_total_length(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "-10 degC",
    window: int = 3,
    freq: str = "YS-JUL",
    op: Literal["<", "lt", "<=", "le"] = "<",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Cold spell total length.

    The total length of cold periods of `N` days or more, during which the temperature over
    a given time window of days is below a given threshold.

    **Units:**

    - cold_spell_total_length: days

    This function wraps `xclim.indicators.atmos.cold_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_spell_total_length>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a cold spell.
    window : int
        Minimum number of days with temperatures below the threshold to qualify as a cold
        spell.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cold_spell_total_length(
        tas=tas,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.consecutive_frost_days)
def consecutive_frost_days(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS-JUL",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Consecutive frost days.

    Maximum number of consecutive days where the daily minimum temperature is below 0°C

    **Units:**

    - consecutive_frost_days: days

    This function wraps `xclim.indicators.atmos.consecutive_frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.consecutive_frost_days>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.consecutive_frost_days(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.maximum_consecutive_frost_free_days)
def maximum_consecutive_frost_free_days(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Maximum consecutive frost free days.

    Maximum number of consecutive frost-free days: where the daily minimum temperature is
    above or equal to 0°C

    **Units:**

    - consecutive_frost_free_days: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_frost_free_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_frost_free_days>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.maximum_consecutive_frost_free_days(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cool_night_index)
def cool_night_index(
    tasmin: xarray.DataArray | str = "tasmin",
    lat: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    freq: Literal["YS", "YS-JAN"] = "YS",
    **kwargs: Any,
) -> Any:
    """
    Cool night index.

    A night coolness variable which takes into account the mean minimum night temperatures
    during the month when ripening usually occurs beyond the ripening period.

    **Units:**

    - cool_night_index: degC

    This function wraps `xclim.indicators.atmos.cool_night_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cool_night_index>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    lat : xarray.DataArray | str | None
        Latitude coordinate as an array, float or string. If None, a CF-conformant
        "latitude" field must be available within the passed DataArray.
    freq : Literal['YS', 'YS-JAN']
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cool_night_index(
        tasmin=tasmin,
        lat=lat,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cooling_degree_days)
def cooling_degree_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "18.0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Cooling degree days.

    The cumulative degree days for days when the mean daily temperature is above a given
    threshold and buildings must be air conditioned.

    **Units:**

    - cooling_degree_days: K days

    This function wraps `xclim.indicators.atmos.cooling_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cooling_degree_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Temperature threshold above which air is cooled.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cooling_degree_days(
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cooling_degree_days_approximation)
def cooling_degree_days_approximation(
    tasmax: xarray.DataArray | str = "tasmax",
    tasmin: xarray.DataArray | str = "tasmin",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "18.0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Temperature threshold above which air is cooled.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cooling_degree_days_approximation(
        tasmax=tasmax,
        tasmin=tasmin,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.corn_heat_units)
def corn_heat_units(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "4.44 degC",
    thresh_tasmax: Any = "10 degC",
    **kwargs: Any,
) -> Any:
    """
    Corn heat units.

    A temperature-based index used to estimate the development of corn crops. Corn growth
    occurs when the daily minimum and maximum temperatures exceed given thresholds.

    **Units:**

    - chu: dimensionless

    This function wraps `xclim.indicators.atmos.corn_heat_units <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.corn_heat_units>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The minimum temperature threshold needed for corn growth.
    thresh_tasmax : Any
        The maximum temperature threshold needed for corn growth.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.corn_heat_units(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.chill_portions)
def chill_portions(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tas : xarray.DataArray | str
        Hourly temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.chill_portions(
        tas=tas,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.chill_units)
def chill_units(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    positive_only: bool = False,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tas : xarray.DataArray | str
        Hourly temperature.
    positive_only : bool
        If `True`, only positive daily chill units are aggregated.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.chill_units(
        tas=tas,
        positive_only=positive_only,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.degree_days_exceedance_date)
def degree_days_exceedance_date(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    sum_thresh: Any = "25 K days",
    op: Literal[">", "gt", "<", "lt", ">=", "ge", "<=", "le"] = ">",
    after_date: str | None = None,
    never_reached: str | int | None = None,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Degree day exceedance date.

    The day of the year when the sum of degree days exceeds a threshold, occurring after a
    given date. Degree days are calculated above or below a given temperature threshold.

    **Units:**

    - degree_days_exceedance_date: dimensionless

    This function wraps `xclim.indicators.atmos.degree_days_exceedance_date <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.degree_days_exceedance_date>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base degree-days evaluation.
    sum_thresh : Any
        Threshold of the degree days sum.
    op : Literal['>', 'gt', '<', 'lt', '>=', 'ge', '<=', 'le']
        If equivalent to '>', degree days are computed as `tas - thresh` and if equivalent
        to '<', they are computed as `thresh - tas`.
    after_date : str | None
        Date at which to start the cumulative sum. In "MM-DD" format, defaults to the start
        of the sampling period.
    never_reached : str | int | None
        What to do when `sum_thresh` is never exceeded. If an int, the value to assign as a
        day-of-year. If a string, must be in "MM-DD" format, the day-of-year of that date is
        assigned. Default (None) assigns "NaN".
    freq : str
        Resampling frequency. If `after_date` is given, `freq` should be annual.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.degree_days_exceedance_date(
        tas=tas,
        thresh=thresh,
        sum_thresh=sum_thresh,
        op=op,
        after_date=after_date,
        never_reached=never_reached,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.daily_freezethaw_cycles)
def daily_freezethaw_cycles(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "0 degC",
    thresh_tasmax: Any = "0 degC",
    op_tasmin: Literal["<", "<=", "lt", "le"] = "<=",
    op_tasmax: Literal[">", ">=", "gt", "ge"] = ">",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The temperature threshold needed to trigger a freeze event.
    thresh_tasmax : Any
        The temperature threshold needed to trigger a thaw event.
    op_tasmin : Literal['<', '<=', 'lt', 'le']
        Comparison operation for tasmin. Default: "<=".
    op_tasmax : Literal['>', '>=', 'gt', 'ge']
        Comparison operation for tasmax. Default: ">".
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.daily_freezethaw_cycles(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        op_tasmin=op_tasmin,
        op_tasmax=op_tasmax,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.daily_temperature_range)
def daily_temperature_range(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean of daily temperature range.

    The average difference between the daily maximum and minimum temperatures.

    **Units:**

    - dtr: K

    This function wraps `xclim.indicators.atmos.daily_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_temperature_range>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.daily_temperature_range(
        tasmin=tasmin,
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.max_daily_temperature_range)
def max_daily_temperature_range(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum of daily temperature range.

    The maximum difference between the daily maximum and minimum temperatures.

    **Units:**

    - dtrmax: K

    This function wraps `xclim.indicators.atmos.max_daily_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_daily_temperature_range>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.max_daily_temperature_range(
        tasmin=tasmin,
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.daily_temperature_range_variability)
def daily_temperature_range_variability(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Variability of daily temperature range.

    The average day-to-day variation in daily temperature range.

    **Units:**

    - dtrvar: K

    This function wraps `xclim.indicators.atmos.daily_temperature_range_variability <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_temperature_range_variability>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.daily_temperature_range_variability(
        tasmin=tasmin,
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.extreme_temperature_range)
def extreme_temperature_range(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Extreme temperature range.

    The maximum of the maximum temperature minus the minimum of the minimum temperature.

    **Units:**

    - etr: K

    This function wraps `xclim.indicators.atmos.extreme_temperature_range <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.extreme_temperature_range>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.extreme_temperature_range(
        tasmin=tasmin,
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.fire_season)
def fire_season(
    tas: xarray.DataArray | str = "tas",
    snd: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    method: str = "WF93",
    freq: str | None = None,
    temp_start_thresh: Any = "12 degC",
    temp_end_thresh: Any = "5 degC",
    temp_condition_days: int = 3,
    snow_condition_days: int = 3,
    snow_thresh: Any = "0.01 m",
    **kwargs: Any,
) -> Any:
    """
    Fire season mask.

    Binary mask of the active fire season, defined by conditions on consecutive daily
    temperatures and, optionally, snow depths.

    **Units:**

    - fire_season: dimensionless

    This function wraps `xclim.indicators.atmos.fire_season <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fire_season>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Daily surface temperature, cffdrs recommends using maximum daily temperature.
    snd : xarray.DataArray | str | None
        Snow depth, used with method == 'LA08'.
    method : str
        Which method to use. "LA08"  and "GFWED" need the snow depth.
    freq : str | None
        If given only the longest fire season for each period defined by this frequency,
        Every "seasons" are returned if None, including the short shoulder seasons.
    temp_start_thresh : Any
        Minimal temperature needed to start the season. Must be scalar.
    temp_end_thresh : Any
        Maximal temperature needed to end the season. Must be scalar.
    temp_condition_days : int
        Number of days with temperature above or below the thresholds to trigger a start or
        an end of the fire season.
    snow_condition_days : int
        Parameters for the fire season determination. See :py:func:`fire_season`.
        Temperature is in degC, snow in m. The `snow_thresh` parameters is also used when
        `dry_start` is set to "GFWED".
    snow_thresh : Any
        Minimal snow depth level to end a fire season, only used with method "LA08". Must be
        scalar.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.fire_season(
        tas=tas,
        snd=snd,
        method=method,
        freq=freq,
        temp_start_thresh=temp_start_thresh,
        temp_end_thresh=temp_end_thresh,
        temp_condition_days=temp_condition_days,
        snow_condition_days=snow_condition_days,
        snow_thresh=snow_thresh,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tg_above)
def first_day_tg_above(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    after_date: str = "01-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tg_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tg_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tg_above>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature above the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tg_above(
        tas=tas,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tg_below)
def first_day_tg_below(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal["<", "lt", "<=", "le"] = "<",
    after_date: str = "07-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tg_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tg_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tg_below>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature below the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tg_below(
        tas=tas,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tn_above)
def first_day_tn_above(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    after_date: str = "01-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tn_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tn_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tn_above>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum surface temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature above the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tn_above(
        tasmin=tasmin,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tn_below)
def first_day_tn_below(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal["<", "lt", "<=", "le"] = "<",
    after_date: str = "07-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tn_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tn_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tn_below>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum surface temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature below the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tn_below(
        tasmin=tasmin,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tx_above)
def first_day_tx_above(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    after_date: str = "01-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures superior to a given temperature threshold.

    Returns first day of period where temperature is superior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: January 1st).

    **Units:**

    - first_day_tx_above: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tx_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tx_above>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum surface temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature above the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tx_above(
        tasmax=tasmax,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_day_tx_below)
def first_day_tx_below(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal["<", "lt", "<=", "le"] = "<",
    after_date: str = "07-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    First day of temperatures inferior to a given temperature threshold.

    Returns first day of period where temperature is inferior to a threshold over a given
    number of days (default: 1), limited to a starting calendar date (default: July 1st).

    **Units:**

    - first_day_tx_below: dimensionless

    This function wraps `xclim.indicators.atmos.first_day_tx_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_day_tx_below>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum surface temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature below the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.first_day_tx_below(
        tasmax=tasmax,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.freezethaw_spell_frequency)
def freezethaw_spell_frequency(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "0 degC",
    thresh_tasmax: Any = "0 degC",
    window: int = 1,
    op_tasmin: Literal["<", "<=", "lt", "le"] = "<=",
    op_tasmax: Literal[">", ">=", "gt", "ge"] = ">",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The temperature threshold needed to trigger a freeze event.
    thresh_tasmax : Any
        The temperature threshold needed to trigger a thaw event.
    window : int
        The minimal length of spells to be included in the statistics.
    op_tasmin : Literal['<', '<=', 'lt', 'le']
        Comparison operation for tasmin. Default: "<=".
    op_tasmax : Literal['>', '>=', 'gt', 'ge']
        Comparison operation for tasmax. Default: ">".
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.freezethaw_spell_frequency(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        op_tasmin=op_tasmin,
        op_tasmax=op_tasmax,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.freezethaw_spell_max_length)
def freezethaw_spell_max_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "0 degC",
    thresh_tasmax: Any = "0 degC",
    window: int = 1,
    op_tasmin: Literal["<", "<=", "lt", "le"] = "<=",
    op_tasmax: Literal[">", ">=", "gt", "ge"] = ">",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The temperature threshold needed to trigger a freeze event.
    thresh_tasmax : Any
        The temperature threshold needed to trigger a thaw event.
    window : int
        The minimal length of spells to be included in the statistics.
    op_tasmin : Literal['<', '<=', 'lt', 'le']
        Comparison operation for tasmin. Default: "<=".
    op_tasmax : Literal['>', '>=', 'gt', 'ge']
        Comparison operation for tasmax. Default: ">".
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.freezethaw_spell_max_length(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        op_tasmin=op_tasmin,
        op_tasmax=op_tasmax,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.freezethaw_spell_mean_length)
def freezethaw_spell_mean_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "0 degC",
    thresh_tasmax: Any = "0 degC",
    window: int = 1,
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The temperature threshold needed to trigger a freeze event.
    thresh_tasmax : Any
        The temperature threshold needed to trigger a thaw event.
    window : int
        The minimal length of spells to be included in the statistics.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.freezethaw_spell_mean_length(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.freezing_degree_days)
def freezing_degree_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Freezing degree days.

    The cumulative degree days for days when the average temperature is below a given
    threshold, typically 0°C.

    **Units:**

    - freezing_degree_days: K days

    This function wraps `xclim.indicators.atmos.freezing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freezing_degree_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.freezing_degree_days(
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.freshet_start)
def freshet_start(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    after_date: str = "01-01",
    window: int = 5,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Day of year of spring freshet start.

    Day of year of the spring freshet start, defined as the first day when the temperature
    exceeds a certain threshold for a given number of consecutive days.

    **Units:**

    - freshet_start: dimensionless

    This function wraps `xclim.indicators.atmos.freshet_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.freshet_start>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    after_date : str
        Date of the year after which to look for the first event. Should have the format
        '%m-%d'.
    window : int
        Minimum number of days with temperature above the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.freshet_start(
        tas=tas,
        thresh=thresh,
        op=op,
        after_date=after_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_days)
def frost_days(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Frost days.

    Number of days where the daily minimum temperature is below a given threshold.

    **Units:**

    - frost_days: days

    This function wraps `xclim.indicators.atmos.frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_days>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Freezing temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_days(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_free_season_end)
def frost_free_season_end(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    window: int = 5,
    mid_date: str | None = "07-01",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Frost free season end.

    First day when the temperature is below a given threshold for a given number of
    consecutive days after a median calendar date.

    **Units:**

    - frost_free_season_end: dimensionless

    This function wraps `xclim.indicators.atmos.frost_free_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_season_end>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    window : int
        Minimum number of days with temperature above/under the threshold to start/end the
        season.
    mid_date : str | None
        A date what must be included in the season. `None` removes that constraint.
    op : Literal['>', 'gt', '>=', 'ge']
        How to compare tasmin and the threshold.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_free_season_end(
        tasmin=tasmin,
        thresh=thresh,
        window=window,
        mid_date=mid_date,
        op=op,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_free_season_length)
def frost_free_season_length(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    window: int = 5,
    mid_date: str | None = "07-01",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    window : int
        Minimum number of days with temperature above/under the threshold to start/end the
        season.
    mid_date : str | None
        A date what must be included in the season. `None` removes that constraint.
    op : Literal['>', 'gt', '>=', 'ge']
        How to compare tasmin and the threshold.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_free_season_length(
        tasmin=tasmin,
        thresh=thresh,
        window=window,
        mid_date=mid_date,
        op=op,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_free_season_start)
def frost_free_season_start(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    window: int = 5,
    mid_date: str | None = "07-01",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Frost free season start.

    First day when minimum daily temperature exceeds a given threshold for a given number of
    consecutive days

    **Units:**

    - frost_free_season_start: dimensionless

    This function wraps `xclim.indicators.atmos.frost_free_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_season_start>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    window : int
        Minimum number of days with temperature above/under the threshold to start/end the
        season.
    mid_date : str | None
        A date that must be included in the season. `None` removes that constraint.
    op : Literal['>', 'gt', '>=', 'ge']
        How to compare tasmin and the threshold.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_free_season_start(
        tasmin=tasmin,
        thresh=thresh,
        window=window,
        mid_date=mid_date,
        op=op,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_free_spell_max_length)
def frost_free_spell_max_length(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0.0 degC",
    window: int = 1,
    freq: str = "YS-JUL",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Frost free spell maximum length.

    The maximum length of a frost free period of `N` days or more, during which the minimum
    temperature over a given time window of days is above a given threshold.

    **Units:**

    - frost_free_spell_max_length: days

    This function wraps `xclim.indicators.atmos.frost_free_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.frost_free_spell_max_length>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a frost-free spell.
    window : int
        Minimum number of days with temperatures above thresholds to qualify as a frost-free
        day.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">=".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_free_spell_max_length(
        tasmin=tasmin,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.frost_season_length)
def frost_season_length(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 5,
    mid_date: str | None = "01-01",
    thresh: Any = "0 degC",
    freq: str = "YS-JUL",
    op: Literal["<", "lt", "<=", "le"] = "<",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    window : int
        Minimum number of days with temperature below threshold to mark the beginning and
        end of frost season.
    mid_date : str | None
        The date must be included in the season. It is the earliest the end of the season
        can be. ``None`` removes that constraint.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.frost_season_length(
        tasmin=tasmin,
        window=window,
        mid_date=mid_date,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.growing_degree_days)
def growing_degree_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "4.0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Growing degree days.

    The cumulative degree days for days when the average temperature is above a given
    threshold.

    **Units:**

    - growing_degree_days: K days

    This function wraps `xclim.indicators.atmos.growing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_degree_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.growing_degree_days(
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.growing_season_end)
def growing_season_end(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "5.0 degC",
    mid_date: str | None = "07-01",
    window: int = 5,
    freq: str = "YS",
    op: Literal[">", ">=", "lt", "le"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Growing season end.

    The first day when the temperature is below a certain threshold for a certain number of
    consecutive days after a given calendar date.

    **Units:**

    - growing_season_end: dimensionless

    This function wraps `xclim.indicators.atmos.growing_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_season_end>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    mid_date : str | None
        Date of the year after which to look for the end of the season. Should have the
        format '%m-%d'. ``None`` removes that constraint.
    window : int
        Minimum number of days with temperature below threshold needed for evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', '>=', 'lt', 'le']
        Comparison operation. Default: ">". Note that this comparison is what defines the
        season. The end of the season happens when the condition is NOT met for `window`
        consecutive days.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.growing_season_end(
        tas=tas,
        thresh=thresh,
        mid_date=mid_date,
        window=window,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.growing_season_length)
def growing_season_length(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "5.0 degC",
    window: int = 6,
    mid_date: str | None = "07-01",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
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
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    window : int
        Minimum number of days with temperature above the threshold to mark the beginning
        and end of growing season.
    mid_date : str | None
        Date of the year before which the season must start and after which it can end.
        Should have the format '%m-%d'. Setting `None` removes that constraint.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">=".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.growing_season_length(
        tas=tas,
        thresh=thresh,
        window=window,
        mid_date=mid_date,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.growing_season_start)
def growing_season_start(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "5.0 degC",
    mid_date: str | None = "07-01",
    window: int = 5,
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Growing season start.

    The first day when the temperature exceeds a certain threshold for a given number of
    consecutive days.

    **Units:**

    - growing_season_start: dimensionless

    This function wraps `xclim.indicators.atmos.growing_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.growing_season_start>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    mid_date : str | None
        Date of the year before which the season must start. Should have the format '%m-%d'.
        ``None`` removes that constraint.
    window : int
        Minimum number of days with temperature above threshold needed for evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">=".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.growing_season_start(
        tas=tas,
        thresh=thresh,
        mid_date=mid_date,
        window=window,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_spell_frequency)
def heat_spell_frequency(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 3,
    win_reducer: Literal["min", "max", "sum", "mean"] = "mean",
    freq: str = "YS",
    min_gap: int = 1,
    resample_before_rl: bool = True,
    thresh_tasmin: Any = "20 °C",
    thresh_tasmax: Any = "33 °C",
    **kwargs: Any,
) -> Any:
    """
    Heat spell frequency.

    Number of heat spells. A heat spell occurs when rolling averages of daily minimum and
    maximumtemperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.heat_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_frequency>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum surface temperature.
    tasmax : xarray.DataArray | str
        Maximum surface temperature.
    window : int
        Minimum length of a spell.
    win_reducer : Literal['min', 'max', 'sum', 'mean']
        Reduction along the spell length to compute the spell value. Note that this does not
        matter when `window` is 1.
    freq : str
        Resampling frequency.
    min_gap : int
        The shortest possible gap between two spells. Spells closer than this are merged by
        assigning the gap steps to the merged spell.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    thresh_tasmin : Any
        Threshold for tasmin
    thresh_tasmax : Any
        Threshold for tasmax
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_spell_frequency(
        tasmin=tasmin,
        tasmax=tasmax,
        window=window,
        win_reducer=win_reducer,
        freq=freq,
        min_gap=min_gap,
        resample_before_rl=resample_before_rl,
        ds=ds,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_spell_max_length)
def heat_spell_max_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 3,
    win_reducer: Literal["min", "max", "sum", "mean"] = "mean",
    freq: str = "YS",
    min_gap: int = 1,
    resample_before_rl: bool = True,
    thresh_tasmin: Any = "20 °C",
    thresh_tasmax: Any = "33 °C",
    **kwargs: Any,
) -> Any:
    """
    Heat spell maximum length.

    The longest heat spell of a period. A heat spell occurs when rolling averages of daily
    minimum and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_max_length: days

    This function wraps `xclim.indicators.atmos.heat_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_max_length>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum surface temperature.
    tasmax : xarray.DataArray | str
        Maximum surface temperature.
    window : int
        Minimum length of a spell.
    win_reducer : Literal['min', 'max', 'sum', 'mean']
        Reduction along the spell length to compute the spell value. Note that this does not
        matter when `window` is 1.
    freq : str
        Resampling frequency.
    min_gap : int
        The shortest possible gap between two spells. Spells closer than this are merged by
        assigning the gap steps to the merged spell.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    thresh_tasmin : Any
        Threshold for tasmin
    thresh_tasmax : Any
        Threshold for tasmax
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_spell_max_length(
        tasmin=tasmin,
        tasmax=tasmax,
        window=window,
        win_reducer=win_reducer,
        freq=freq,
        min_gap=min_gap,
        resample_before_rl=resample_before_rl,
        ds=ds,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_spell_total_length)
def heat_spell_total_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 3,
    win_reducer: Literal["min", "max", "sum", "mean"] = "mean",
    freq: str = "YS",
    min_gap: int = 1,
    resample_before_rl: bool = True,
    thresh_tasmin: Any = "20 °C",
    thresh_tasmax: Any = "33 °C",
    **kwargs: Any,
) -> Any:
    """
    Heat spell total length.

    Total length of heat spells. A heat spell occurs when rolling averages of daily minimum
    and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_spell_total_length: days

    This function wraps `xclim.indicators.atmos.heat_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_spell_total_length>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum surface temperature.
    tasmax : xarray.DataArray | str
        Maximum surface temperature.
    window : int
        Minimum length of a spell.
    win_reducer : Literal['min', 'max', 'sum', 'mean']
        Reduction along the spell length to compute the spell value. Note that this does not
        matter when `window` is 1.
    freq : str
        Resampling frequency.
    min_gap : int
        The shortest possible gap between two spells. Spells closer than this are merged by
        assigning the gap steps to the merged spell.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    thresh_tasmin : Any
        Threshold for tasmin
    thresh_tasmax : Any
        Threshold for tasmax
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_spell_total_length(
        tasmin=tasmin,
        tasmax=tasmax,
        window=window,
        win_reducer=win_reducer,
        freq=freq,
        min_gap=min_gap,
        resample_before_rl=resample_before_rl,
        ds=ds,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_wave_frequency)
def heat_wave_frequency(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "22.0 degC",
    thresh_tasmax: Any = "30 degC",
    window: int = 3,
    freq: str = "YS",
    op: Literal[">", ">=", "gt", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Heat wave frequency.

    Number of heat waves. A heat wave occurs when daily minimum and maximum temperatures
    exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.heat_wave_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_frequency>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The minimum temperature threshold needed to trigger a heatwave event.
    thresh_tasmax : Any
        The maximum temperature threshold needed to trigger a heatwave event.
    window : int
        Minimum number of days with temperatures above thresholds to qualify as a heatwave.
    freq : str
        Resampling frequency.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_wave_frequency(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_wave_index)
def heat_wave_index(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25 degC",
    window: int = 5,
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Heat wave index.

    Number of days that constitute heatwave events. A heat wave occurs when daily minimum
    and maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_index: days

    This function wraps `xclim.indicators.atmos.heat_wave_index <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_index>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a hot spell.
    window : int
        Minimum number of days with temperatures below the threshold to qualify as a hot
        spell.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_wave_index(
        tasmax=tasmax,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_wave_max_length)
def heat_wave_max_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "22.0 degC",
    thresh_tasmax: Any = "30 degC",
    window: int = 3,
    freq: str = "YS",
    op: Literal[">", ">=", "gt", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Heat wave maximum length.

    Maximal duration of heat waves. A heat wave occurs when daily minimum and maximum
    temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_max_length: days

    This function wraps `xclim.indicators.atmos.heat_wave_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_max_length>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The minimum temperature threshold needed to trigger a heatwave event.
    thresh_tasmax : Any
        The maximum temperature threshold needed to trigger a heatwave event.
    window : int
        Minimum number of days with temperatures above thresholds to qualify as a heatwave.
    freq : str
        Resampling frequency.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_wave_max_length(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heat_wave_total_length)
def heat_wave_total_length(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "22.0 degC",
    thresh_tasmax: Any = "30 degC",
    window: int = 3,
    freq: str = "YS",
    op: Literal[">", ">=", "gt", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Heat wave total length.

    Total length of heat waves. A heat wave occurs when daily minimum and maximum
    temperatures exceed given thresholds for a number of days.

    **Units:**

    - heat_wave_total_length: days

    This function wraps `xclim.indicators.atmos.heat_wave_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heat_wave_total_length>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        The minimum temperature threshold needed to trigger a heatwave event.
    thresh_tasmax : Any
        The maximum temperature threshold needed to trigger a heatwave event.
    window : int
        Minimum number of days with temperatures above thresholds to qualify as a heatwave.
    freq : str
        Resampling frequency.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heat_wave_total_length(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heating_degree_days)
def heating_degree_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "17.0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Heating degree days.

    The cumulative degree days for days when the mean daily temperature is below a given
    threshold and buildings must be heated.

    **Units:**

    - heating_degree_days: K days

    This function wraps `xclim.indicators.atmos.heating_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.heating_degree_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heating_degree_days(
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.heating_degree_days_approximation)
def heating_degree_days_approximation(
    tasmax: xarray.DataArray | str = "tasmax",
    tasmin: xarray.DataArray | str = "tasmin",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "17.0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.heating_degree_days_approximation(
        tasmax=tasmax,
        tasmin=tasmin,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.hot_days)
def hot_days(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Hot days.

    Number of days where the daily maximum temperature is above a given threshold.

    **Units:**

    - hot_days: days

    This function wraps `xclim.indicators.atmos.hot_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_days>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Threshold temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.hot_days(
        tasmax=tasmax,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.hot_spell_frequency)
def hot_spell_frequency(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "30 degC",
    window: int = 3,
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Hot spell frequency.

    The frequency of hot periods of `N` days or more, during which the temperature over a
    given time window of days is above a given threshold.

    **Units:**

    - hot_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.hot_spell_frequency <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_frequency>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Threshold temperature below which a hot spell begins.
    window : int
        Minimum number of days with temperature above the threshold to qualify as a hot
        spell.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.hot_spell_frequency(
        tasmax=tasmax,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.hot_spell_max_length)
def hot_spell_max_length(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "30 degC",
    window: int = 1,
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Hot spell maximum length.

    The maximum length of a hot period of `N` days or more, during which the temperature
    over a given time window of days is above a given threshold.

    **Units:**

    - hot_spell_max_length: days

    This function wraps `xclim.indicators.atmos.hot_spell_max_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_max_length>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a hot spell.
    window : int
        Minimum number of days with temperatures below thresholds to qualify as a hot spell.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.hot_spell_max_length(
        tasmax=tasmax,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.hot_spell_max_magnitude)
def hot_spell_max_magnitude(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25.0 degC",
    window: int = 3,
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Hot spell maximum magnitude.

    Magnitude of the most intensive heat wave per {freq}. A heat wave occurs when daily
    maximum temperatures exceed given thresholds for a number of days.

    **Units:**

    - hot_spell_max_magnitude: K d

    This function wraps `xclim.indicators.atmos.hot_spell_max_magnitude <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_max_magnitude>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Threshold temperature on which to designate a heatwave.
    window : int
        Minimum number of days with temperature above the threshold to qualify as a
        heatwave.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.hot_spell_max_magnitude(
        tasmax=tasmax,
        thresh=thresh,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.hot_spell_total_length)
def hot_spell_total_length(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "30 degC",
    window: int = 3,
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Hot spell total length.

    The total length of hot periods of `N` days or more, during which the temperature over a
    given time window of days is above a given threshold.

    **Units:**

    - hot_spell_total_length: days

    This function wraps `xclim.indicators.atmos.hot_spell_total_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.hot_spell_total_length>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        The temperature threshold needed to trigger a hot spell.
    window : int
        Minimum number of days with temperatures below the threshold to qualify as a hot
        spell.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.hot_spell_total_length(
        tasmax=tasmax,
        thresh=thresh,
        window=window,
        freq=freq,
        op=op,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.huglin_index)
def huglin_index(
    tas: xarray.DataArray | str = "tas",
    tasmax: xarray.DataArray | str = "tasmax",
    lat: xarray.DataArray | str = "lat",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "10 degC",
    method: str = "jones",
    cap_value: float = 1.0,
    start_date: str | str = "04-01",
    end_date: str | str = "10-01",
    freq: Literal["YS", "YS-JAN", "YS-JUL"] = "YS",
    **kwargs: Any,
) -> Any:
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
    tas : xarray.DataArray | str
        Mean daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    lat : xarray.DataArray | str
        Latitude coordinate. If None, a CF-conformant "latitude" field must be available
        within the passed DataArray.
    thresh : Any
        The temperature threshold.
    method : str
        The formula to use for the latitude coefficient calculation. The "huglin" method
        uses a stepwise latitude coefficient for values between 40° and 50° based on
        :cite:t:`huglin_nouveau_1978`. The "interpolated" method uses a smoothed curve
        latitude coefficient for values based on the intervals set in
        :cite:t:`huglin_nouveau_1978`. The "jones" method integrates axial tilt, latitude,
        and day-of-year based on :cite:t:`hall_spatial_2010`. The "icclim" method is
        deprecated but is identical to method "huglin".
    cap_value : float
        The value to use for the latitude coefficient when latitude is above 50°N or below
        50°S. Only applicable for methods "huglin", "icclim", and "interpolated" (default:
        1.0).
    start_date : str | str
        The hemisphere-based start date to consider (north = April, south = October).
    end_date : str | str
        The hemisphere-based start date to consider (north = October, south = April). This
        date is non-inclusive.
    freq : Literal['YS', 'YS-JAN', 'YS-JUL']
        Resampling frequency (default: "YS"; For Southern Hemisphere, should be "YS-JUL").
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.huglin_index(
        tas=tas,
        tasmax=tasmax,
        lat=lat,
        thresh=thresh,
        method=method,
        cap_value=cap_value,
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.ice_days)
def ice_days(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Ice days.

    Number of days where the daily maximum temperature is below 0°C

    **Units:**

    - ice_days: days

    This function wraps `xclim.indicators.atmos.ice_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.ice_days>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Freezing temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.ice_days(
        tasmax=tasmax,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.last_spring_frost)
def last_spring_frost(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    op: Literal["<", "lt", "<=", "le"] = "<",
    before_date: str = "07-01",
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Last spring frost.

    The last day when minimum temperature is below a given threshold for a certain number of
    days, limited by a final calendar date.

    **Units:**

    - last_spring_frost: dimensionless

    This function wraps `xclim.indicators.atmos.last_spring_frost <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.last_spring_frost>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    before_date : str
        Date of the year before which to look for the final frost event. Should have the
        format '%m-%d'.
    window : int
        Minimum number of days with temperature below the threshold needed for evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.last_spring_frost(
        tasmin=tasmin,
        thresh=thresh,
        op=op,
        before_date=before_date,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.late_frost_days)
def late_frost_days(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Late frost days.

    Number of days where the daily minimum temperature is below a given threshold between a
    givenstart date and a given end date.

    **Units:**

    - late_frost_days: days

    This function wraps `xclim.indicators.atmos.late_frost_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.late_frost_days>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Freezing temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.late_frost_days(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.latitude_temperature_index)
def latitude_temperature_index(
    tas: xarray.DataArray | str = "tas",
    lat: xarray.DataArray | str = "lat",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tas : xarray.DataArray | str
        Mean daily temperature.
    lat : xarray.DataArray | str
        Latitude coordinate. If None, a CF-conformant "latitude" field must be available
        within the passed DataArray.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.latitude_temperature_index(
        tas=tas,
        lat=lat,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.maximum_consecutive_warm_days)
def maximum_consecutive_warm_days(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25 degC",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Maximum consecutive warm days.

    Maximum number of consecutive days where the maximum daily temperature exceeds a certain
    threshold.

    **Units:**

    - maximum_consecutive_warm_days: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_warm_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_warm_days>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Max daily temperature.
    thresh : Any
        Threshold temperature.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.maximum_consecutive_warm_days(
        tasmax=tasmax,
        thresh=thresh,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg10p)
def tg10p(
    tas: xarray.DataArray | str = "tas",
    tas_per: xarray.DataArray | str = "tas_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Days with mean temperature below the 10th percentile.

    Number of days with mean temperature below the 10th percentile.

    **Units:**

    - tg10p: days

    This function wraps `xclim.indicators.atmos.tg10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg10p>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    tas_per : xarray.DataArray | str
        10th percentile of daily mean temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg10p(
        tas=tas,
        tas_per=tas_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg90p)
def tg90p(
    tas: xarray.DataArray | str = "tas",
    tas_per: xarray.DataArray | str = "tas_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Days with mean temperature above the 90th percentile.

    Number of days with mean temperature above the 90th percentile.

    **Units:**

    - tg90p: days

    This function wraps `xclim.indicators.atmos.tg90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg90p>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    tas_per : xarray.DataArray | str
        90th percentile of daily mean temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg90p(
        tas=tas,
        tas_per=tas_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg_days_above)
def tg_days_above(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "10.0 degC",
    freq: str = "YS",
    op: Literal["<", "lt", "<=", "le"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with mean temperature above a given threshold.

    The number of days with mean temperature above a given threshold.

    **Units:**

    - tg_days_above: days

    This function wraps `xclim.indicators.atmos.tg_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_days_above>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg_days_above(
        tas=tas,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg_days_below)
def tg_days_below(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "10.0 degC",
    freq: str = "YS",
    op: Literal["<", "lt", "<=", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Number of days with mean temperature below a given threshold.

    The number of days with mean temperature below a given threshold.

    **Units:**

    - tg_days_below: days

    This function wraps `xclim.indicators.atmos.tg_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_days_below>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg_days_below(
        tas=tas,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg_max)
def tg_max(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum of mean temperature.

    Maximum of daily mean temperature.

    **Units:**

    - tg_max: K

    This function wraps `xclim.indicators.atmos.tg_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_max>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg_max(
        tas=tas,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg_mean)
def tg_mean(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean temperature.

    Mean of daily mean temperature.

    **Units:**

    - tg_mean: K

    This function wraps `xclim.indicators.atmos.tg_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_mean>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg_mean(
        tas=tas,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tg_min)
def tg_min(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Minimum of mean temperature.

    Minimum of daily mean temperature.

    **Units:**

    - tg_min: K

    This function wraps `xclim.indicators.atmos.tg_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tg_min>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tg_min(
        tas=tas,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.thawing_degree_days)
def thawing_degree_days(
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Thawing degree days.

    The cumulative degree days for days when the average temperature is above a given
    threshold, typically 0°C.

    **Units:**

    - thawing_degree_days: K days

    This function wraps `xclim.indicators.atmos.thawing_degree_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.thawing_degree_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.thawing_degree_days(
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn10p)
def tn10p(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmin_per: xarray.DataArray | str = "tasmin_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal["<", "<=", "lt", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Days with minimum temperature below the 10th percentile.

    Number of days with minimum temperature below the 10th percentile.

    **Units:**

    - tn10p: days

    This function wraps `xclim.indicators.atmos.tn10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn10p>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Mean daily temperature.
    tasmin_per : xarray.DataArray | str
        10th percentile of daily minimum temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['<', '<=', 'lt', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn10p(
        tasmin=tasmin,
        tasmin_per=tasmin_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn90p)
def tn90p(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmin_per: xarray.DataArray | str = "tasmin_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Days with minimum temperature above the 90th percentile.

    Number of days with minimum temperature above the 90th percentile.

    **Units:**

    - tn90p: days

    This function wraps `xclim.indicators.atmos.tn90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn90p>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmin_per : xarray.DataArray | str
        90th percentile of daily minimum temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn90p(
        tasmin=tasmin,
        tasmin_per=tasmin_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn_days_above)
def tn_days_above(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "20.0 degC",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with minimum temperature above a given threshold.

    The number of days with minimum temperature above a given threshold.

    **Units:**

    - tn_days_above: days

    This function wraps `xclim.indicators.atmos.tn_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_days_above>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn_days_above(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn_days_below)
def tn_days_below(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "-10.0 degC",
    freq: str = "YS",
    op: Literal["<", "lt", "<=", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Number of days with minimum temperature below a given threshold.

    The number of days with minimum temperature below a given threshold.

    **Units:**

    - tn_days_below: days

    This function wraps `xclim.indicators.atmos.tn_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_days_below>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn_days_below(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn_max)
def tn_max(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum of minimum temperature.

    Maximum of daily minimum temperature.

    **Units:**

    - tn_max: K

    This function wraps `xclim.indicators.atmos.tn_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_max>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn_max(
        tasmin=tasmin,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn_mean)
def tn_mean(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean of minimum temperature.

    Mean of daily minimum temperature.

    **Units:**

    - tn_mean: K

    This function wraps `xclim.indicators.atmos.tn_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_mean>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn_mean(
        tasmin=tasmin,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tn_min)
def tn_min(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Minimum temperature.

    Minimum of daily minimum temperature.

    **Units:**

    - tn_min: K

    This function wraps `xclim.indicators.atmos.tn_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tn_min>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tn_min(
        tasmin=tasmin,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tropical_nights)
def tropical_nights(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "20.0 degC",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Tropical nights.

    Number of days where minimum temperature is above a given threshold.

    **Units:**

    - tropical_nights: days

    This function wraps `xclim.indicators.atmos.tropical_nights <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tropical_nights>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tropical_nights(
        tasmin=tasmin,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx10p)
def tx10p(
    tasmax: xarray.DataArray | str = "tasmax",
    tasmax_per: xarray.DataArray | str = "tasmax_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal["<", "<=", "lt", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Days with maximum temperature below the 10th percentile.

    Number of days with maximum temperature below the 10th percentile.

    **Units:**

    - tx10p: days

    This function wraps `xclim.indicators.atmos.tx10p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx10p>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    tasmax_per : xarray.DataArray | str
        10th percentile of daily maximum temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['<', '<=', 'lt', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx10p(
        tasmax=tasmax,
        tasmax_per=tasmax_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx90p)
def tx90p(
    tasmax: xarray.DataArray | str = "tasmax",
    tasmax_per: xarray.DataArray | str = "tasmax_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal["<", "<=", "lt", "le"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Days with maximum temperature above the 90th percentile.

    Number of days with maximum temperature above the 90th percentile.

    **Units:**

    - tx90p: days

    This function wraps `xclim.indicators.atmos.tx90p <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx90p>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    tasmax_per : xarray.DataArray | str
        90th percentile of daily maximum temperature.
    freq : str
        Resampling frequency.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['<', '<=', 'lt', 'le']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx90p(
        tasmax=tasmax,
        tasmax_per=tasmax_per,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_days_above)
def tx_days_above(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25.0 degC",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with maximum temperature above a given threshold.

    The number of days with maximum temperature above a given threshold.

    **Units:**

    - tx_days_above: days

    This function wraps `xclim.indicators.atmos.tx_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_days_above>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_days_above(
        tasmax=tasmax,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_days_below)
def tx_days_below(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25.0 degC",
    freq: str = "YS",
    op: Literal["<", "lt", "<=", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Number of days with maximum temperature below a given threshold.

    The number of days with maximum temperature below a given threshold.

    **Units:**

    - tx_days_below: days

    This function wraps `xclim.indicators.atmos.tx_days_below <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_days_below>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh : Any
        Threshold temperature on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['<', 'lt', '<=', 'le']
        Comparison operation. Default: "<".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_days_below(
        tasmax=tasmax,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_max)
def tx_max(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum temperature.

    Maximum of daily maximum temperature.

    **Units:**

    - tx_max: K

    This function wraps `xclim.indicators.atmos.tx_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_max>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_max(
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_mean)
def tx_mean(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean of maximum temperature.

    Mean of daily maximum temperature.

    **Units:**

    - tx_mean: K

    This function wraps `xclim.indicators.atmos.tx_mean <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_mean>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_mean(
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_min)
def tx_min(
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Minimum of maximum temperature.

    Minimum of daily maximum temperature.

    **Units:**

    - tx_min: K

    This function wraps `xclim.indicators.atmos.tx_min <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_min>`_.

    Parameters
    ----------
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_min(
        tasmax=tasmax,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.tx_tn_days_above)
def tx_tn_days_above(
    tasmin: xarray.DataArray | str = "tasmin",
    tasmax: xarray.DataArray | str = "tasmax",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_tasmin: Any = "22 degC",
    thresh_tasmax: Any = "30 degC",
    freq: str = "YS",
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with daily minimum and maximum temperatures exceeding thresholds.

    Number of days with daily maximum and minimum temperatures above given thresholds.

    **Units:**

    - tx_tn_days_above: days

    This function wraps `xclim.indicators.atmos.tx_tn_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.tx_tn_days_above>`_.

    Parameters
    ----------
    tasmin : xarray.DataArray | str
        Minimum daily temperature.
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    thresh_tasmin : Any
        Threshold temperature for tasmin on which to base evaluation.
    thresh_tasmax : Any
        Threshold temperature for tasmax on which to base evaluation.
    freq : str
        Resampling frequency.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.tx_tn_days_above(
        tasmin=tasmin,
        tasmax=tasmax,
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.usda_hardiness_zones)
def usda_hardiness_zones(
    tasmin: xarray.DataArray | str = "tasmin",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 30,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
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
    tasmin : xarray.DataArray | str
        Minimum temperature.
    window : int
        The length of the averaging window, in years.
    freq : str
        Resampling frequency.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.usda_hardiness_zones(
        tasmin=tasmin,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.warm_spell_duration_index)
def warm_spell_duration_index(
    tasmax: xarray.DataArray | str = "tasmax",
    tasmax_per: xarray.DataArray | str = "tasmax_per",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 6,
    freq: str = "YS",
    resample_before_rl: bool = True,
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
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
    tasmax : xarray.DataArray | str
        Maximum daily temperature.
    tasmax_per : xarray.DataArray | str
        Percentile(s) of daily maximum temperature.
    window : int
        Minimum number of days with temperature above threshold to qualify as a warm spell.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    bootstrap : bool
        Flag to run bootstrapping of percentiles. Used by percentile_bootstrap decorator.
        Bootstrapping is only useful when the percentiles are computed on a part of the
        studied sample. This period, common to percentiles and the sample must be
        bootstrapped to avoid inhomogeneities with the rest of the time series. Do not
        enable bootstrap when there is no common period, otherwise it will provide the wrong
        results. Note that bootstrapping is computationally expensive.
    op : Literal['>', '>=', 'gt', 'ge']
        Comparison operation. Default: ">".
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.warm_spell_duration_index(
        tasmax=tasmax,
        tasmax_per=tasmax_per,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )
