# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Precipitation indices."""

from typing import Any, Literal

import xarray
import xclim.indicators.atmos
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.atmos.antecedent_precipitation_index)
def antecedent_precipitation_index(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 7,
    p_exp: float = 0.935,
    **kwargs: Any,
) -> Any:
    """
    Antecedent precipitation index.

    Calculate the running weighted sum of daily precipitation values given a window and
    weighting exponent. This index serves as an indicator for soil moisture.

    **Units:**

    - api: mm

    This function wraps `xclim.indicators.atmos.antecedent_precipitation_index
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.antecedent_precipitation_index>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation data.
    window : int
        Window for the days of precipitation data to be weighted and summed, default is 7.
    p_exp : float
        Weighting exponent, default is 0.935.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.antecedent_precipitation_index(
        pr=pr,
        window=window,
        p_exp=p_exp,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.maximum_consecutive_dry_days)
def maximum_consecutive_dry_days(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Maximum consecutive dry days.

    The longest number of consecutive days where daily precipitation below a given
    threshold.

    **Units:**

    - cdd: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_dry_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_dry_days>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    thresh : Any
        Threshold precipitation on which to base evaluation.
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
    return xclim.indicators.atmos.maximum_consecutive_dry_days(
        pr=pr,
        thresh=thresh,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cffwis_indices)
def cffwis_indices(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    sfcWind: xarray.DataArray | str = "sfcWind",
    hurs: xarray.DataArray | str = "hurs",
    lat: xarray.DataArray | str = "lat",
    snd: xarray.DataArray | str | None = None,
    ffmc0: xarray.DataArray | str | None = None,
    dmc0: xarray.DataArray | str | None = None,
    dc0: xarray.DataArray | str | None = None,
    season_mask: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    season_method: str | None = None,
    overwintering: bool = False,
    dry_start: str | None = None,
    initial_start_up: bool = True,
    **kwargs: Any,
) -> Any:
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

    This function wraps `xclim.indicators.atmos.cffwis_indices
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cffwis_indices>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Noon temperature.
    pr : xarray.DataArray | str
        Rain fall in open over previous 24 hours, at noon.
    sfcWind : xarray.DataArray | str
        Noon wind speed.
    hurs : xarray.DataArray | str
        Noon relative humidity.
    lat : xarray.DataArray | str
        Latitude coordinate.
    snd : xarray.DataArray | str | None
        Noon snow depth, only used if `season_method='LA08'` is passed.
    ffmc0 : xarray.DataArray | str | None
        Initial values of the fine fuel moisture code.
    dmc0 : xarray.DataArray | str | None
        Initial values of the Duff moisture code.
    dc0 : xarray.DataArray | str | None
        Initial values of the drought code.
    season_mask : xarray.DataArray | str | None
        Boolean mask, True where/when the fire season is active.
    season_method : str | None
        How to compute the start-up and shutdown of the fire season. If "None", no start-ups
        or shutdowns are computed, similar to the R fire function. Ignored if `season_mask`
        is given.
    overwintering : bool
        Whether to activate DC overwintering or not. If True, either season_method or
        season_mask must be given.
    dry_start : str | None
        Whether to activate the DC and DMC "dry start" mechanism or not, see
        :py:func:`fire_weather_ufunc`.
    initial_start_up : bool
        If True (default), gridpoints where the fire season is active on the first timestep
        go through a start_up phase for that time step. Otherwise, previous codes must be
        given as a continuing fire season is assumed for those points.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.cffwis_indices(
        tas=tas,
        pr=pr,
        sfcWind=sfcWind,
        hurs=hurs,
        lat=lat,
        snd=snd,
        ffmc0=ffmc0,
        dmc0=dmc0,
        dc0=dc0,
        season_mask=season_mask,
        season_method=season_method,
        overwintering=overwintering,
        dry_start=dry_start,
        initial_start_up=initial_start_up,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_and_dry_days)
def cold_and_dry_days(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    tas_per: xarray.DataArray | str = "tas_per",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Cold and dry days.

    Number of days with temperature below a given percentile and precipitation below a given
    percentile.

    **Units:**

    - cold_and_dry_days: days

    This function wraps `xclim.indicators.atmos.cold_and_dry_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_and_dry_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature values.
    pr : xarray.DataArray | str
        Daily precipitation.
    tas_per : xarray.DataArray | str
        First quartile of daily mean temperature computed by month.
    pr_per : xarray.DataArray | str
        First quartile of daily total precipitation computed by month.
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
    return xclim.indicators.atmos.cold_and_dry_days(
        tas=tas,
        pr=pr,
        tas_per=tas_per,
        pr_per=pr_per,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.cold_and_wet_days)
def cold_and_wet_days(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    tas_per: xarray.DataArray | str = "tas_per",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Cold and wet days.

    Number of days with temperature below a given percentile and precipitation above a given
    percentile.

    **Units:**

    - cold_and_wet_days: days

    This function wraps `xclim.indicators.atmos.cold_and_wet_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.cold_and_wet_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature values.
    pr : xarray.DataArray | str
        Daily precipitation.
    tas_per : xarray.DataArray | str
        First quartile of daily mean temperature computed by month.
    pr_per : xarray.DataArray | str
        Third quartile of daily total precipitation computed by month.
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
    return xclim.indicators.atmos.cold_and_wet_days(
        tas=tas,
        pr=pr,
        tas_per=tas_per,
        pr_per=pr_per,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.maximum_consecutive_wet_days)
def maximum_consecutive_wet_days(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Maximum consecutive wet days.

    The longest number of consecutive days where daily precipitation is at or above a given
    threshold.

    **Units:**

    - cwd: days

    This function wraps `xclim.indicators.atmos.maximum_consecutive_wet_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.maximum_consecutive_wet_days>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    thresh : Any
        Threshold precipitation on which to base evaluation.
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
    return xclim.indicators.atmos.maximum_consecutive_wet_days(
        pr=pr,
        thresh=thresh,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.days_over_precip_doy_thresh)
def days_over_precip_doy_thresh(
    pr: xarray.DataArray | str = "pr",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with precipitation above a given daily percentile.

    Number of days in a period where precipitation is above a given daily percentile and a
    fixed threshold.

    **Units:**

    - days_over_precip_doy_thresh: days

    This function wraps `xclim.indicators.atmos.days_over_precip_doy_thresh
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_over_precip_doy_thresh>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    pr_per : xarray.DataArray | str
        Percentile of wet day precipitation flux. Either computed daily (one value per day
        of year) or computed over a period (one value per spatial point).
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.days_over_precip_doy_thresh(
        pr=pr,
        pr_per=pr_per,
        thresh=thresh,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.days_over_precip_thresh)
def days_over_precip_thresh(
    pr: xarray.DataArray | str = "pr",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Number of days with precipitation above a given percentile.

    Number of days in a period where precipitation is above a given percentile, calculated
    over a given period and a fixed threshold.

    **Units:**

    - days_over_precip_thresh: days

    This function wraps `xclim.indicators.atmos.days_over_precip_thresh
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_over_precip_thresh>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    pr_per : xarray.DataArray | str
        Percentile of wet day precipitation flux. Either computed daily (one value per day
        of year) or computed over a period (one value per spatial point).
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.days_over_precip_thresh(
        pr=pr,
        pr_per=pr_per,
        thresh=thresh,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.days_with_snow)
def days_with_snow(
    prsn: xarray.DataArray | str = "prsn",
    ds: xarray.Dataset | Any = None,
    *,
    low: Any = "0 kg m-2 s-1",
    high: Any = "1E6 kg m-2 s-1",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Days with snowfall.

    Number of days with snow between a lower and upper limit.

    **Units:**

    - days_with_snow: days

    This function wraps `xclim.indicators.atmos.days_with_snow
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.days_with_snow>`_.

    Parameters
    ----------
    prsn : xarray.DataArray | str
        Snowfall flux.
    low : Any
        Minimum threshold snowfall flux or liquid water equivalent snowfall rate.
    high : Any
        Maximum threshold snowfall flux or liquid water equivalent snowfall rate.
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
    return xclim.indicators.atmos.days_with_snow(
        prsn=prsn,
        low=low,
        high=high,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.drought_code)
def drought_code(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    lat: xarray.DataArray | str = "lat",
    snd: xarray.DataArray | str | None = None,
    dc0: xarray.DataArray | str | None = None,
    season_mask: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    season_method: str | None = None,
    overwintering: bool = False,
    dry_start: str | None = None,
    initial_start_up: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Daily drought code.

    The Drought Index is part of the Canadian Forest-Weather Index system. It is a numerical
    code that estimates the average moisture content of organic layers.

    **Units:**

    - dc: dimensionless

    This function wraps `xclim.indicators.atmos.drought_code
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.drought_code>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Noon temperature.
    pr : xarray.DataArray | str
        Rain fall in open over previous 24 hours, at noon.
    lat : xarray.DataArray | str
        Latitude coordinate.
    snd : xarray.DataArray | str | None
        Noon snow depth.
    dc0 : xarray.DataArray | str | None
        Initial values of the drought code.
    season_mask : xarray.DataArray | str | None
        Boolean mask, True where/when the fire season is active.
    season_method : str | None
        How to compute the start-up and shutdown of the fire season. If "None", no start-ups
        or shutdowns are computed, similar to the R fire function. Ignored if `season_mask`
        is given.
    overwintering : bool
        Whether to activate DC overwintering or not. If True, either season_method or
        season_mask must be given.
    dry_start : str | None
        Whether to activate the DC and DMC "dry start" mechanism and which method to use.
        See :py:func:`fire_weather_ufunc`.
    initial_start_up : bool
        If True (default), grid points where the fire season is active on the first timestep
        go through a start_up phase for that time step. Otherwise, previous codes must be
        given as a continuing fire season is assumed for those points.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.drought_code(
        tas=tas,
        pr=pr,
        lat=lat,
        snd=snd,
        dc0=dc0,
        season_mask=season_mask,
        season_method=season_method,
        overwintering=overwintering,
        dry_start=dry_start,
        initial_start_up=initial_start_up,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.griffiths_drought_factor)
def griffiths_drought_factor(
    pr: xarray.DataArray | str = "pr",
    smd: xarray.DataArray | str = "smd",
    ds: xarray.Dataset | Any = None,
    *,
    limiting_func: str = "xlim",
    **kwargs: Any,
) -> Any:
    """
    Griffiths drought factor based on the soil moisture deficit.

    The drought factor is a numeric indicator of the forest fire fuel availability in the
    deep litter bed. It is often used in the calculation of the McArthur Forest Fire Danger
    Index. The method implemented here follows :cite:t:`ffdi-finkele_2006`.

    **Units:**

    - df: dimensionless

    This function wraps `xclim.indicators.atmos.griffiths_drought_factor
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.griffiths_drought_factor>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Total rainfall over previous 24 hours [mm/day].
    smd : xarray.DataArray | str
        Daily soil moisture deficit (often KBDI) [mm/day].
    limiting_func : str
        How to limit the values of the drought factor. If "xlim" (default), use equation
        (14) in :cite:t:`ffdi-finkele_2006`. If "discrete", use equation Eq (13) in
        :cite:t:`ffdi-finkele_2006`, but with the lower limit of each category bound
        adjusted to match the upper limit of the previous bound.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.griffiths_drought_factor(
        pr=pr,
        smd=smd,
        limiting_func=limiting_func,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.duff_moisture_code)
def duff_moisture_code(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    hurs: xarray.DataArray | str = "hurs",
    lat: xarray.DataArray | str = "lat",
    snd: xarray.DataArray | str | None = None,
    dmc0: xarray.DataArray | str | None = None,
    season_mask: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    season_method: str | None = None,
    dry_start: str | None = None,
    initial_start_up: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Duff moisture code (fwi component).

    The duff moisture code is part of the Canadian Forest Fire Weather Index System. It is a
    numeric rating of the average moisture content of loosely compacted organic layers of
    moderate depth.

    **Units:**

    - dmc: dimensionless

    This function wraps `xclim.indicators.atmos.duff_moisture_code
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.duff_moisture_code>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Noon temperature.
    pr : xarray.DataArray | str
        Rain fall in open over previous 24 hours, at noon.
    hurs : xarray.DataArray | str
        Noon relative humidity.
    lat : xarray.DataArray | str
        Latitude coordinate.
    snd : xarray.DataArray | str | None
        Noon snow depth.
    dmc0 : xarray.DataArray | str | None
        Initial values of the duff moisture code.
    season_mask : xarray.DataArray | str | None
        Boolean mask, True where/when the fire season is active.
    season_method : str | None
        How to compute the start-up and shutdown of the fire season. If "None", no start-ups
        or shutdowns are computed, similar to the R fire function. Ignored if `season_mask`
        is given.
    dry_start : str | None
        Whether to activate the DC and DMC "dry start" mechanism and which method to use.
        See :py:func:`fire_weather_ufunc`.
    initial_start_up : bool
        If True (default), grid points where the fire season is active on the first timestep
        go through a start_up phase for that time step. Otherwise, previous codes must be
        given as a continuing fire season is assumed for those points.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.duff_moisture_code(
        tas=tas,
        pr=pr,
        hurs=hurs,
        lat=lat,
        snd=snd,
        dmc0=dmc0,
        season_mask=season_mask,
        season_method=season_method,
        dry_start=dry_start,
        initial_start_up=initial_start_up,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.dry_days)
def dry_days(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0.2 mm/d",
    freq: str = "YS",
    op: Literal["<", "lt", "<=", "le"] = "<",
    **kwargs: Any,
) -> Any:
    """
    Number of dry days.

    The number of days with daily precipitation under a given threshold.

    **Units:**

    - dry_days: days

    This function wraps `xclim.indicators.atmos.dry_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_days>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Threshold precipitation on which to base evaluation.
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
    return xclim.indicators.atmos.dry_days(
        pr=pr,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.dry_spell_frequency)
def dry_spell_frequency(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 3,
    freq: str = "YS",
    resample_before_rl: bool = True,
    op: Literal["sum", "max", "min", "mean"] = "sum",
    **kwargs: Any,
) -> Any:
    """
    Dry spell frequency.

    The frequency of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.dry_spell_frequency
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_frequency>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Precipitation amount under which a period is considered dry. The value against which
        the threshold is compared depends on `op`.
    window : int
        Minimum length of the spells.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    op : Literal['sum', 'max', 'min', 'mean']
        Operation to perform on the window. Default is "sum", which checks that the sum of
        accumulated precipitation over the whole window is less than the threshold. "max"
        checks that the maximal daily precipitation amount within the window is less than
        the threshold. This is the same as verifying that each individual day is below the
        threshold.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.dry_spell_frequency(
        pr=pr,
        thresh=thresh,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.dry_spell_max_length)
def dry_spell_max_length(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 1,
    op: Literal["max", "sum"] = "sum",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Dry spell maximum length.

    The maximum length of a dry period of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_max_length: days

    This function wraps `xclim.indicators.atmos.dry_spell_max_length
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_max_length>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Accumulated precipitation value under which a period is considered dry.
    window : int
        Number of days when the maximum or accumulated precipitation is under the threshold.
    op : Literal['max', 'sum']
        Reduce operation.
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
    return xclim.indicators.atmos.dry_spell_max_length(
        pr=pr,
        thresh=thresh,
        window=window,
        op=op,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.dry_spell_total_length)
def dry_spell_total_length(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 3,
    op: Literal["sum", "max", "min", "mean"] = "sum",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Dry spell total length.

    The total length of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is below a given threshold.

    **Units:**

    - dry_spell_total_length: days

    This function wraps `xclim.indicators.atmos.dry_spell_total_length
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dry_spell_total_length>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Accumulated precipitation value under which a period is considered dry.
    window : int
        Number of days when the maximum or accumulated precipitation is under the threshold.
    op : Literal['sum', 'max', 'min', 'mean']
        Operation to perform on the window. Default is "sum", which checks that the sum of
        accumulated precipitation over the whole window is less than the threshold. "max"
        checks that the maximal daily precipitation amount within the window is less than
        the threshold. This is the same as verifying that each individual day is below the
        threshold.
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
    return xclim.indicators.atmos.dry_spell_total_length(
        pr=pr,
        thresh=thresh,
        window=window,
        op=op,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.dryness_index)
def dryness_index(
    pr: xarray.DataArray | str = "pr",
    evspsblpot: xarray.DataArray | str = "evspsblpot",
    lat: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    wo: Any = "200 mm",
    freq: Literal["YS", "YS-JAN"] = "YS",
    **kwargs: Any,
) -> Any:
    """
    Dryness index.

    The dryness index is a characterization of the water component in winegrowing regions
    which considers the precipitation and evapotranspiration factors without deduction for
    surface runoff or drainage. Metric originally published in Riou et al. (1994).

    **Units:**

    - dryness_index: mm

    This function wraps `xclim.indicators.atmos.dryness_index
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.dryness_index>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Precipitation.
    evspsblpot : xarray.DataArray | str
        Potential evapotranspiration.
    lat : xarray.DataArray | str | None
        Latitude coordinate as an array, float or string. If None, a CF-conformant
        "latitude" field must be available within the passed DataArray.
    wo : Any
        The initial soil water reserve accessible to root systems [length]. Default: 200 mm.
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
    return xclim.indicators.atmos.dryness_index(
        pr=pr,
        evspsblpot=evspsblpot,
        lat=lat,
        wo=wo,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.mcarthur_forest_fire_danger_index)
def mcarthur_forest_fire_danger_index(
    drought_factor: xarray.DataArray | str = "drought_factor",
    tasmax: xarray.DataArray | str = "tasmax",
    hurs: xarray.DataArray | str = "hurs",
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    **kwargs: Any,
) -> Any:
    """
    Mcarthur forest fire danger index (ffdi) mark 5.

    The FFDI is a numeric indicator of the potential danger of a forest fire.

    **Units:**

    - ffdi: dimensionless

    This function wraps `xclim.indicators.atmos.mcarthur_forest_fire_danger_index
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.mcarthur_forest_fire_danger_index>`_.

    Parameters
    ----------
    drought_factor : xarray.DataArray | str
        The drought factor, often the daily Griffiths drought factor (see
        :py:func:`griffiths_drought_factor`).
    tasmax : xarray.DataArray | str
        The daily maximum temperature near the surface, or similar. Different applications
        have used different inputs here, including the previous/current day's maximum daily
        temperature at a height of 2m, and the daily mean temperature at a height of 2m.
    hurs : xarray.DataArray | str
        The relative humidity near the surface and near the time of the maximum daily
        temperature, or similar. Different applications have used different inputs here,
        including the mid-afternoon relative humidity at a height of 2m, and the daily mean
        relative humidity at a height of 2m.
    sfcWind : xarray.DataArray | str
        The wind speed near the surface and near the time of the maximum daily temperature,
        or similar. Different applications have used different inputs here, including the
        mid-afternoon wind speed at a height of 10m, and the daily mean wind speed at a
        height of 10m.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.mcarthur_forest_fire_danger_index(
        drought_factor=drought_factor,
        tasmax=tasmax,
        hurs=hurs,
        sfcWind=sfcWind,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.first_snowfall)
def first_snowfall(
    prsn: xarray.DataArray | str = "prsn",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    First day where snowfall exceeded a given threshold.

    The first day where snowfall exceeded a given threshold during a time period (the
    threshold can be given as a snowfall flux or a liquid water equivalent snowfall rate).

    **Units:**

    - first_snowfall: dimensionless

    This function wraps `xclim.indicators.atmos.first_snowfall
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.first_snowfall>`_.

    Parameters
    ----------
    prsn : xarray.DataArray | str
        Snowfall flux.
    thresh : Any
        Threshold snowfall flux or liquid water equivalent snowfall rate. (default: 1
        mm/day).
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
    return xclim.indicators.atmos.first_snowfall(
        prsn=prsn,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.fraction_over_precip_doy_thresh)
def fraction_over_precip_doy_thresh(
    pr: xarray.DataArray | str = "pr",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Fraction of precipitation due to wet days with daily precipitation over a given daily percentile.

    The percentage of the total precipitation over a period occurring for days when the
    precipitation is above a threshold defining wet days and above a given percentile for
    that day.

    **Units:**

    - fraction_over_precip_doy_thresh: dimensionless

    This function wraps `xclim.indicators.atmos.fraction_over_precip_doy_thresh
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fraction_over_precip_doy_thresh>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    pr_per : xarray.DataArray | str
        Percentile of wet day precipitation flux. Either computed daily (one value per day
        of year) or computed over a period (one value per spatial point).
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.fraction_over_precip_doy_thresh(
        pr=pr,
        pr_per=pr_per,
        thresh=thresh,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.fraction_over_precip_thresh)
def fraction_over_precip_thresh(
    pr: xarray.DataArray | str = "pr",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    bootstrap: bool = False,
    op: Literal[">", ">=", "gt", "ge"] = ">",
    **kwargs: Any,
) -> Any:
    """
    Fraction of precipitation due to wet days with daily precipitation over a given percentile.

    The percentage of the total precipitation over a period occurring for days when the
    precipitation is above a threshold defining wet days and above a given percentile for
    that day.

    **Units:**

    - fraction_over_precip_thresh: dimensionless

    This function wraps `xclim.indicators.atmos.fraction_over_precip_thresh
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.fraction_over_precip_thresh>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    pr_per : xarray.DataArray | str
        Percentile of wet day precipitation flux. Either computed daily (one value per day
        of year) or computed over a period (one value per spatial point).
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.fraction_over_precip_thresh(
        pr=pr,
        pr_per=pr_per,
        thresh=thresh,
        freq=freq,
        bootstrap=bootstrap,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.high_precip_low_temp)
def high_precip_low_temp(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    pr_thresh: Any = "0.4 mm/d",
    tas_thresh: Any = "-0.2 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Days with precipitation and cold temperature.

    Number of days with precipitation above a given threshold and temperature below a given
    threshold.

    **Units:**

    - high_precip_low_temp: days

    This function wraps `xclim.indicators.atmos.high_precip_low_temp
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.high_precip_low_temp>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Daily mean, minimum or maximum temperature.
    pr_thresh : Any
        Precipitation threshold to exceed.
    tas_thresh : Any
        Temperature threshold not to exceed.
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
    return xclim.indicators.atmos.high_precip_low_temp(
        pr=pr,
        tas=tas,
        pr_thresh=pr_thresh,
        tas_thresh=tas_thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.keetch_byram_drought_index)
def keetch_byram_drought_index(
    pr: xarray.DataArray | str = "pr",
    tasmax: xarray.DataArray | str = "tasmax",
    pr_annual: xarray.DataArray | str = "pr_annual",
    kbdi0: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    **kwargs: Any,
) -> Any:
    """
    Keetch-byram drought index (kbdi) for soil moisture deficit.

    The KBDI indicates the amount of water necessary to bring the soil moisture content back
    to field capacity. It is often used in the calculation of the McArthur Forest Fire
    Danger Index. The method implemented here follows :cite:t:`ffdi-finkele_2006` but limits
    the maximum KBDI to 203.2 mm, rather than 200 mm, in order to align best with the
    majority of the literature.

    **Units:**

    - kbdi: mm/day

    This function wraps `xclim.indicators.atmos.keetch_byram_drought_index
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.keetch_byram_drought_index>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Total rainfall over previous 24 hours [mm/day].
    tasmax : xarray.DataArray | str
        Maximum temperature near the surface over previous 24 hours [degC].
    pr_annual : xarray.DataArray | str
        Mean (over years) annual accumulated rainfall [mm/year].
    kbdi0 : xarray.DataArray | str | None
        Previous KBDI values used to initialise the KBDI calculation [mm/day]. Defaults to
        0.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.keetch_byram_drought_index(
        pr=pr,
        tasmax=tasmax,
        pr_annual=pr_annual,
        kbdi0=kbdi0,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.last_snowfall)
def last_snowfall(
    prsn: xarray.DataArray | str = "prsn",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Last day where snowfall exceeded a given threshold.

    The last day where snowfall exceeded a given threshold during a time period (the
    threshold can be given as a snowfall flux or a liquid water equivalent snowfall rate).

    **Units:**

    - last_snowfall: dimensionless

    This function wraps `xclim.indicators.atmos.last_snowfall
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.last_snowfall>`_.

    Parameters
    ----------
    prsn : xarray.DataArray | str
        Snowfall flux.
    thresh : Any
        Threshold snowfall flux or liquid water equivalent snowfall rate (default: 1
        mm/day).
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
    return xclim.indicators.atmos.last_snowfall(
        prsn=prsn,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.liquid_precip_ratio)
def liquid_precip_ratio(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "QS-DEC",
    **kwargs: Any,
) -> Any:
    """
    Fraction of liquid to total precipitation.

    The ratio of total liquid precipitation over the total precipitation. Liquid
    precipitation is approximated from total precipitation on days where temperature is
    above a given threshold.

    **Units:**

    - liquid_precip_ratio: dimensionless

    This function wraps `xclim.indicators.atmos.liquid_precip_ratio
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_ratio>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Threshold temperature under which precipitation is assumed to be solid.
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
    return xclim.indicators.atmos.liquid_precip_ratio(
        pr=pr,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.liquid_precip_average)
def liquid_precip_average(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Averaged liquid precipitation.

    Averaged liquid precipitation. Precipitation is considered liquid when the average daily
    temperature is above a given threshold.

    **Units:**

    - liquidprcpavg: mm

    This function wraps `xclim.indicators.atmos.liquid_precip_average
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_average>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean, maximum or minimum daily temperature.
    thresh : Any
        Threshold of `tas` over which the precipication is assumed to be liquid rain.
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
    return xclim.indicators.atmos.liquid_precip_average(
        pr=pr,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.liquid_precip_accumulation)
def liquid_precip_accumulation(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Total accumulated liquid precipitation.

    Total accumulated liquid precipitation. Precipitation is considered liquid when the
    average daily temperature is above a given threshold.

    **Units:**

    - liquidprcptot: mm

    This function wraps `xclim.indicators.atmos.liquid_precip_accumulation
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.liquid_precip_accumulation>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean, maximum or minimum daily temperature.
    thresh : Any
        Threshold of `tas` over which the precipication is assumed to be liquid rain.
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
    return xclim.indicators.atmos.liquid_precip_accumulation(
        pr=pr,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.max_n_day_precipitation_amount)
def max_n_day_precipitation_amount(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum n-day total precipitation.

    Maximum of the moving sum of daily precipitation for a given period.

    **Units:**

    - rx{window}day: mm

    This function wraps `xclim.indicators.atmos.max_n_day_precipitation_amount
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_n_day_precipitation_amount>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation values.
    window : int
        Window size in days.
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
    return xclim.indicators.atmos.max_n_day_precipitation_amount(
        pr=pr,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.max_pr_intensity)
def max_pr_intensity(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 1,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum precipitation intensity over time window.

    Maximum precipitation intensity over a given rolling time window.

    **Units:**

    - max_pr_intensity: mm h-1

    This function wraps `xclim.indicators.atmos.max_pr_intensity
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_pr_intensity>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Hourly precipitation values.
    window : int
        Window size in hours.
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
    return xclim.indicators.atmos.max_pr_intensity(
        pr=pr,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.precip_average)
def precip_average(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Averaged precipitation (solid and liquid).

    Averaged precipitation. If the average daily temperature is given, the phase parameter
    can be used to restrict the calculation to precipitation of only one phase (liquid or
    solid). Precipitation is considered solid if the average daily temperature is below 0°C
    threshold (and vice versa).

    **Units:**

    - prcpavg: mm

    This function wraps `xclim.indicators.atmos.precip_average
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.precip_average>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    thresh : Any
        Threshold of `tas` over which the precipication is assumed to be liquid rain.
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
    return xclim.indicators.atmos.precip_average(
        pr=pr,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.precip_accumulation)
def precip_accumulation(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Total accumulated precipitation (solid and liquid).

    Total accumulated precipitation. If the average daily temperature is given, the phase
    parameter can be used to restrict the calculation to precipitation of only one phase
    (liquid or solid). Precipitation is considered solid if the average daily temperature is
    below 0°C (and vice versa).

    **Units:**

    - prcptot: mm

    This function wraps `xclim.indicators.atmos.precip_accumulation
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.precip_accumulation>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
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
    return xclim.indicators.atmos.precip_accumulation(
        pr=pr,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.rain_on_frozen_ground_days)
def rain_on_frozen_ground_days(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/d",
    window: int = 7,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Number of rain on frozen ground days.

    The number of days with rain above a given threshold after a series of seven days with
    average daily temperature below 0°C. Precipitation is assumed to be rain when the daily
    average temperature is above 0°C.

    **Units:**

    - rain_frzgr: days

    This function wraps `xclim.indicators.atmos.rain_on_frozen_ground_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rain_on_frozen_ground_days>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean daily temperature.
    thresh : Any
        Precipitation threshold to consider a day as a rain event.
    window : int
        Minimum number of days below freezing temperature needed to consider the ground
        frozen.
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
    return xclim.indicators.atmos.rain_on_frozen_ground_days(
        pr=pr,
        tas=tas,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.rain_season)
def rain_season(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh_wet_start: Any = "25.0 mm",
    window_wet_start: int = 3,
    window_not_dry_start: int = 30,
    thresh_dry_start: Any = "1.0 mm",
    window_dry_start: int = 7,
    method_dry_start: str = "per_day",
    date_min_start: str = "05-01",
    date_max_start: str = "12-31",
    thresh_dry_end: Any = "0.0 mm",
    window_dry_end: int = 20,
    method_dry_end: str = "per_day",
    date_min_end: str = "09-01",
    date_max_end: str = "12-31",
    freq: Any = "YS-JAN",
    **kwargs: Any,
) -> Any:
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

    This function wraps `xclim.indicators.atmos.rain_season
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rain_season>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Precipitation data.
    thresh_wet_start : Any
        Accumulated precipitation threshold associated with `window_wet_start`.
    window_wet_start : int
        Number of days when accumulated precipitation is above `thresh_wet_start`. Defines
        the first condition to start the rain season.
    window_not_dry_start : int
        Number of days, after `window_wet_start` days, during which no dry period must be
        found as a second and last condition to start the rain season. A dry sequence is
        defined with `thresh_dry_start`, `window_dry_start` and `method_dry_start`.
    thresh_dry_start : Any
        Threshold length defining a dry day in the sequence related to `window_dry_start`.
    window_dry_start : int
        Number of days used to define a dry sequence in the start of the season. Daily
        precipitations lower than `thresh_dry_start` during `window_dry_start` days are
        considered a dry sequence. The precipitations must be lower than `thresh_dry_start`
        for either every day in the sequence (`method_dry_start == "per_day"`) or for the
        total (`method_dry_start == "total"`).
    method_dry_start : str
        Method used to define a dry sequence associated with `window_dry_start`. The
        threshold `thresh_dry_start` is either compared to every daily precipitation
        (`method_dry_start == "per_day"`) or to total precipitations (`method_dry_start ==
        "total"`) in the sequence `window_dry_start` days.
    date_min_start : str
        First day of year when season can start ("mm-dd").
    date_max_start : str
        Last day of year when season can start ("mm-dd").
    thresh_dry_end : Any
        Threshold length defining a dry day in the sequence related to `window_dry_end`.
    window_dry_end : int
        Number of days used to define a dry sequence in the end of the season. Daily
        precipitations lower than `thresh_dry_end` during `window_dry_end` days are
        considered a dry sequence. The precipitations must be lower than `thresh_dry_end`
        for either every day in the sequence (`method_dry_end == "per_day"`) or for the
        total (`method_dry_end == "total"`).
    method_dry_end : str
        Method used to define a dry sequence associated with `window_dry_end`. The threshold
        `thresh_dry_end` is either compared to every daily precipitation (`method_dry_end ==
        "per_day"`) or to total precipitations (`method_dry_end == "total"`) in the sequence
        `window_dry` days.
    date_min_end : str
        First day of year when season can end ("mm-dd").
    date_max_end : str
        Last day of year when season can end ("mm-dd").
    freq : Any
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
    return xclim.indicators.atmos.rain_season(
        pr=pr,
        thresh_wet_start=thresh_wet_start,
        window_wet_start=window_wet_start,
        window_not_dry_start=window_not_dry_start,
        thresh_dry_start=thresh_dry_start,
        window_dry_start=window_dry_start,
        method_dry_start=method_dry_start,
        date_min_start=date_min_start,
        date_max_start=date_max_start,
        thresh_dry_end=thresh_dry_end,
        window_dry_end=window_dry_end,
        method_dry_end=method_dry_end,
        date_min_end=date_min_end,
        date_max_end=date_max_end,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.rprctot)
def rprctot(
    pr: xarray.DataArray | str = "pr",
    prc: xarray.DataArray | str = "prc",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm/day",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Proportion of accumulated precipitation arising from convective processes.

    The proportion of total precipitation due to convective processes. Only days with
    surpassing a minimum precipitation flux are considered.

    **Units:**

    - rprctot: dimensionless

    This function wraps `xclim.indicators.atmos.rprctot
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.rprctot>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    prc : xarray.DataArray | str
        Daily convective precipitation.
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.rprctot(
        pr=pr,
        prc=prc,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.max_1day_precipitation_amount)
def max_1day_precipitation_amount(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Maximum 1-day total precipitation.

    Maximum total daily precipitation for a given period.

    **Units:**

    - rx1day: mm/day

    This function wraps `xclim.indicators.atmos.max_1day_precipitation_amount
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.max_1day_precipitation_amount>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation values.
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
    return xclim.indicators.atmos.max_1day_precipitation_amount(
        pr=pr,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.daily_pr_intensity)
def daily_pr_intensity(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Simple daily intensity index.

    Average precipitation for days with daily precipitation above a given threshold.

    **Units:**

    - sdii: mm d-1

    This function wraps `xclim.indicators.atmos.daily_pr_intensity
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.daily_pr_intensity>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.daily_pr_intensity(
        pr=pr,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.snowfall_frequency)
def snowfall_frequency(
    prsn: xarray.DataArray | str = "prsn",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snowfall frequency.

    Percentage of days with snowfall above a given threshold (either a snowfall flux or a
    liquid water equivalent snowfall rate).

    **Units:**

    - snowfall_frequency: %

    This function wraps `xclim.indicators.atmos.snowfall_frequency
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.snowfall_frequency>`_.

    Parameters
    ----------
    prsn : xarray.DataArray | str
        Snowfall flux.
    thresh : Any
        Threshold snowfall flux or liquid water equivalent snowfall rate (default: 1
        mm/day).
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
    return xclim.indicators.atmos.snowfall_frequency(
        prsn=prsn,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.snowfall_intensity)
def snowfall_intensity(
    prsn: xarray.DataArray | str = "prsn",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snowfall intensity.

    Mean daily liquid water equivalent snowfall rate above threshold (either a snowfall flux
    or a liquid water equivalent snowfall rate)

    **Units:**

    - snowfall_intensity: mm/day

    This function wraps `xclim.indicators.atmos.snowfall_intensity
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.snowfall_intensity>`_.

    Parameters
    ----------
    prsn : xarray.DataArray | str
        Snowfall flux.
    thresh : Any
        Threshold snowfall flux or liquid water equivalent snowfall rate (default: 1
        mm/day).
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
    return xclim.indicators.atmos.snowfall_intensity(
        prsn=prsn,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.solid_precip_average)
def solid_precip_average(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Averaged solid precipitation.

    Averaged solid precipitation. Precipitation is considered solid when the average daily
    temperature is at or below a given threshold.

    **Units:**

    - solidprcpavg: mm

    This function wraps `xclim.indicators.atmos.solid_precip_average
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.solid_precip_average>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean, maximum or minimum daily temperature.
    thresh : Any
        Threshold of `tas` over which the precipication is assumed to be liquid rain.
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
    return xclim.indicators.atmos.solid_precip_average(
        pr=pr,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.solid_precip_accumulation)
def solid_precip_accumulation(
    pr: xarray.DataArray | str = "pr",
    tas: xarray.DataArray | str = "tas",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "0 degC",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Total accumulated solid precipitation.

    Total accumulated solid precipitation. Precipitation is considered solid when the
    average daily temperature is at or below a given threshold.

    **Units:**

    - solidprcptot: mm

    This function wraps `xclim.indicators.atmos.solid_precip_accumulation
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.solid_precip_accumulation>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Mean daily precipitation flux.
    tas : xarray.DataArray | str
        Mean, maximum or minimum daily temperature.
    thresh : Any
        Threshold of `tas` over which the precipication is assumed to be liquid rain.
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
    return xclim.indicators.atmos.solid_precip_accumulation(
        pr=pr,
        tas=tas,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.warm_and_dry_days)
def warm_and_dry_days(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    tas_per: xarray.DataArray | str = "tas_per",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Warm and dry days.

    Number of days with temperature above a given percentile and precipitation below a given
    percentile.

    **Units:**

    - warm_and_dry_days: days

    This function wraps `xclim.indicators.atmos.warm_and_dry_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.warm_and_dry_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature values.
    pr : xarray.DataArray | str
        Daily precipitation.
    tas_per : xarray.DataArray | str
        Third quartile of daily mean temperature computed by month.
    pr_per : xarray.DataArray | str
        First quartile of daily total precipitation computed by month.
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
    return xclim.indicators.atmos.warm_and_dry_days(
        tas=tas,
        pr=pr,
        tas_per=tas_per,
        pr_per=pr_per,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.warm_and_wet_days)
def warm_and_wet_days(
    tas: xarray.DataArray | str = "tas",
    pr: xarray.DataArray | str = "pr",
    tas_per: xarray.DataArray | str = "tas_per",
    pr_per: xarray.DataArray | str = "pr_per",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Warm and wet days.

    Number of days with temperature above a given percentile and precipitation above a given
    percentile.

    **Units:**

    - warm_and_wet_days: days

    This function wraps `xclim.indicators.atmos.warm_and_wet_days
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.warm_and_wet_days>`_.

    Parameters
    ----------
    tas : xarray.DataArray | str
        Mean daily temperature values.
    pr : xarray.DataArray | str
        Daily precipitation.
    tas_per : xarray.DataArray | str
        Third quartile of daily mean temperature computed by month.
    pr_per : xarray.DataArray | str
        Third quartile of daily total precipitation computed by month.
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
    return xclim.indicators.atmos.warm_and_wet_days(
        tas=tas,
        pr=pr,
        tas_per=tas_per,
        pr_per=pr_per,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.water_cycle_intensity)
def water_cycle_intensity(
    pr: xarray.DataArray | str = "pr",
    evspsbl: xarray.DataArray | str = "evspsbl",
    ds: xarray.Dataset | Any = None,
    *,
    freq: Any = "YS",
    **kwargs: Any,
) -> Any:
    """
    Water cycle intensity.

    The sum of precipitation and actual evapotranspiration.

    **Units:**

    - water_cycle_intensity: mm

    This function wraps `xclim.indicators.atmos.water_cycle_intensity
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.water_cycle_intensity>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Precipitation flux.
    evspsbl : xarray.DataArray | str
        Actual evapotranspiration flux.
    freq : Any
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
    return xclim.indicators.atmos.water_cycle_intensity(
        pr=pr,
        evspsbl=evspsbl,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wet_precip_accumulation)
def wet_precip_accumulation(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1 mm/day",
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Total accumulated precipitation (solid and liquid) during wet days.

    Total accumulated precipitation on days with precipitation. A day is considered to have
    precipitation if the precipitation is greater than or equal to a given threshold.

    **Units:**

    - wet_prcptot: mm

    This function wraps `xclim.indicators.atmos.wet_precip_accumulation
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_precip_accumulation>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Total precipitation flux [mm d-1], [mm week-1], [mm month-1] or similar.
    thresh : Any
        Threshold over which precipitation starts being cumulated.
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
    return xclim.indicators.atmos.wet_precip_accumulation(
        pr=pr,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wet_spell_frequency)
def wet_spell_frequency(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 3,
    freq: str = "YS",
    resample_before_rl: bool = True,
    op: Literal["sum", "min", "max", "mean"] = "sum",
    **kwargs: Any,
) -> Any:
    """
    Wet spell frequency.

    The frequency of wet periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_frequency: dimensionless

    This function wraps `xclim.indicators.atmos.wet_spell_frequency
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_frequency>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Precipitation amount over which a period is considered dry. The value against which
        the threshold is compared depends on `op`.
    window : int
        Minimum length of the spells.
    freq : str
        Resampling frequency.
    resample_before_rl : bool
        Determines if the resampling should take place before or after the run length
        encoding (or a similar algorithm) is applied to runs.
    op : Literal['sum', 'min', 'max', 'mean']
        Operation to perform on the window. Default is "sum", which checks that the sum of
        accumulated precipitation over the whole window is more than the threshold. "min"
        checks that the maximal daily precipitation amount within the window is more than
        the threshold. This is the same as verifying that each individual day is above the
        threshold.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.atmos.wet_spell_frequency(
        pr=pr,
        thresh=thresh,
        window=window,
        freq=freq,
        resample_before_rl=resample_before_rl,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wet_spell_max_length)
def wet_spell_max_length(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 1,
    op: Literal["min", "sum", "max", "mean"] = "sum",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Wet spell maximum length.

    The maximum length of a wet period of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_max_length: days

    This function wraps `xclim.indicators.atmos.wet_spell_max_length
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_max_length>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Accumulated precipitation value over which a period is considered wet.
    window : int
        Number of days when the maximum or accumulated precipitation is over threshold.
    op : Literal['min', 'sum', 'max', 'mean']
        Reduce operation. `min` means that all days within the minimum window must exceed
        the threshold. `sum` means that the accumulated precipitation within the window must
        exceed the threshold. In all cases, the whole window is marked a part of a wet
        spell.
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
    return xclim.indicators.atmos.wet_spell_max_length(
        pr=pr,
        thresh=thresh,
        window=window,
        op=op,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wet_spell_total_length)
def wet_spell_total_length(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm",
    window: int = 3,
    op: Literal["min", "sum", "max", "mean"] = "sum",
    freq: str = "YS",
    resample_before_rl: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Wet spell total length.

    The total length of dry periods of `N` days or more, during which the accumulated or
    maximum precipitation over a given time window of days is equal or above a given
    threshold.

    **Units:**

    - wet_spell_total_length: days

    This function wraps `xclim.indicators.atmos.wet_spell_total_length
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wet_spell_total_length>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Accumulated precipitation value over which a period is considered wet.
    window : int
        Number of days when the maximum or accumulated precipitation is over the threshold.
    op : Literal['min', 'sum', 'max', 'mean']
        Reduce operation. `min` means that all days within the minimum window must exceed
        the threshold. `sum` means that the accumulated precipitation within the window must
        exceed the threshold. In all cases, the whole window is marked a part of a wet
        spell.
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
    return xclim.indicators.atmos.wet_spell_total_length(
        pr=pr,
        thresh=thresh,
        window=window,
        op=op,
        freq=freq,
        resample_before_rl=resample_before_rl,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wetdays)
def wetdays(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm/day",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Number of wet days.

    The number of days with daily precipitation at or above a given threshold.

    **Units:**

    - wetdays: days

    This function wraps `xclim.indicators.atmos.wetdays
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wetdays>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.wetdays(
        pr=pr,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.atmos.wetdays_prop)
def wetdays_prop(
    pr: xarray.DataArray | str = "pr",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "1.0 mm/day",
    freq: str = "YS",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Proportion of wet days.

    The proportion of days with daily precipitation at or above a given threshold.

    **Units:**

    - wetdays_prop: 1

    This function wraps `xclim.indicators.atmos.wetdays_prop
        <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.atmos.wetdays_prop>`_.

    Parameters
    ----------
    pr : xarray.DataArray | str
        Daily precipitation.
    thresh : Any
        Precipitation value over which a day is considered wet.
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
    return xclim.indicators.atmos.wetdays_prop(
        pr=pr,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )
