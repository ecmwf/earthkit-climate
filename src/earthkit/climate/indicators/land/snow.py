# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Snow indices."""

from typing import Any, Literal

import xarray
import xclim.indicators.land
from earthkit.utils.decorators.format_handlers import format_handler

# from earthkit.climate.utils.decorators import metadata_handler


@format_handler()
# @metadata_handler(xclim.indicators.land.blowing_snow)
def blowing_snow(
    snd: xarray.DataArray | str = "snd",
    sfcWind: xarray.DataArray | str = "sfcWind",
    ds: xarray.Dataset | Any = None,
    *,
    snd_thresh: Any = "5 cm",
    sfcWind_thresh: Any = "15 km/h",
    window: int = 3,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Blowing snow days.

    The number of days with snowfall, snow depth, and windspeed over given thresholds for a
    period of days.

    **Units:**

    - {freq}_blowing_snow: days

    This function wraps `xclim.indicators.land.blowing_snow <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.blowing_snow>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow depth.
    sfcWind : xarray.DataArray | str
        Wind velocity.
    snd_thresh : Any
        Threshold on net snowfall accumulation over the last `window` days.
    sfcWind_thresh : Any
        Wind speed threshold.
    window : int
        Period over which snow is accumulated before comparing against threshold.
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
    return xclim.indicators.land.blowing_snow(
        snd=snd,
        sfcWind=sfcWind,
        snd_thresh=snd_thresh,
        sfcWind_thresh=sfcWind_thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.holiday_snow_and_snowfall_days)
def holiday_snow_and_snowfall_days(
    snd: xarray.DataArray | str = "snd",
    prsn: xarray.DataArray | str | None = None,
    ds: xarray.Dataset | Any = None,
    *,
    snd_thresh: Any = "20 mm",
    prsn_thresh: Any = "1 mm",
    snd_op: Literal[">", "gt", ">=", "ge"] = ">=",
    prsn_op: Literal[">", "gt", ">=", "ge"] = ">=",
    date_start: str = "12-25",
    date_end: str | None = None,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Perfect christmas snow days.

    The total number of days where there is a significant amount of snow on the ground and a
    measurable snowfall occurring on December 25th.

    **Units:**

    - holiday_snow_and_snowfall_days: days

    This function wraps `xclim.indicators.land.holiday_snow_and_snowfall_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.holiday_snow_and_snowfall_days>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow depth.
    prsn : xarray.DataArray | str | None
        Snowfall flux.
    snd_thresh : Any
        Threshold snow amount. Default: 20 mm.
    prsn_thresh : Any
        Threshold daily snowfall liquid-water equivalent thickness. Default: 1 mm.
    snd_op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation for snow depth. Default: ">=".
    prsn_op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation for snowfall flux. Default: ">=".
    date_start : str
        Beginning of analysis period. Default: "12-25" (December 25th).
    date_end : str | None
        End of analysis period. If not provided, `date_start` is used. Default: None.
    freq : str
        Resampling frequency. Default: "YS-JUL". The default value is chosen for the
        northern hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.holiday_snow_and_snowfall_days(
        snd=snd,
        prsn=prsn,
        snd_thresh=snd_thresh,
        prsn_thresh=prsn_thresh,
        snd_op=snd_op,
        prsn_op=prsn_op,
        date_start=date_start,
        date_end=date_end,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.holiday_snow_days)
def holiday_snow_days(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    snd_thresh: Any = "20 mm",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    date_start: str = "12-25",
    date_end: str | None = None,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Christmas snow days.

    The total number of days where there is a significant amount of snow on the ground on
    December 25th.

    **Units:**

    - holiday_snow_days: days

    This function wraps `xclim.indicators.land.holiday_snow_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.holiday_snow_days>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow depth.
    snd_thresh : Any
        Threshold snow amount. Default: 20 mm.
    op : Literal['>', 'gt', '>=', 'ge']
        Comparison operation. Default: ">=".
    date_start : str
        Beginning of the analysis period. Default: "12-25" (December 25th).
    date_end : str | None
        End of analysis period. If not provided, `date_start` is used. Default: None.
    freq : str
        Resampling frequency. Default: "YS". The default value is chosen for the northern
        hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.holiday_snow_days(
        snd=snd,
        snd_thresh=snd_thresh,
        op=op,
        date_start=date_start,
        date_end=date_end,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_days_above)
def snd_days_above(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "2 cm",
    freq: str = "YS-JUL",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Days with snow (depth).

    Number of days when the snow depth is greater than or equal to a given threshold.

    **Units:**

    - snd_days_above: days

    This function wraps `xclim.indicators.land.snd_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_days_above>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow thickness.
    thresh : Any
        Threshold snow thickness.
    freq : str
        Resampling frequency. The default value is chosen for the Northern Hemisphere.
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
    return xclim.indicators.land.snd_days_above(
        snd=snd,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_max_doy)
def snd_max_doy(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Day of year of maximum snow depth.

    Day of the year when snow depth reaches its maximum value.

    **Units:**

    - {freq}_snd_max_doy: dimensionless

    This function wraps `xclim.indicators.land.snd_max_doy <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_max_doy>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow depth.
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
    return xclim.indicators.land.snd_max_doy(
        snd=snd,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_season_end)
def snd_season_end(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "2 cm",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover end date (depth).

    The first date on which snow depth is below a given threshold for a given number of
    consecutive days.

    **Units:**

    - snd_season_end: dimensionless

    This function wraps `xclim.indicators.land.snd_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_season_end>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow thickness.
    thresh : Any
        Threshold snow thickness.
    window : int
        Minimum number of days with snow depth below the threshold.
    freq : str
        Resampling frequency. Default: "YS-JUL". The default value is chosen for the
        northern hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.snd_season_end(
        snd=snd,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_season_length)
def snd_season_length(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "2 cm",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover duration (depth).

    The season starts when snow depth is above a threshold for at least `N` consecutive days
    and stops when it drops below the same threshold for the same number of days.

    **Units:**

    - snd_season_length: days

    This function wraps `xclim.indicators.land.snd_season_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_season_length>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow thickness.
    thresh : Any
        Threshold snow thickness.
    window : int
        Minimum number of days with snow depth above and below threshold.
    freq : str
        Resampling frequency. The default value is chosen for the northern hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.snd_season_length(
        snd=snd,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_season_start)
def snd_season_start(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "2 cm",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover start date (depth).

    The first date on which snow depth is greater than or equal to a given threshold for a
    given number of consecutive days.

    **Units:**

    - snd_season_start: dimensionless

    This function wraps `xclim.indicators.land.snd_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_season_start>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow thickness.
    thresh : Any
        Threshold snow thickness.
    window : int
        Minimum number of days with snow depth above or equal to the threshold.
    freq : str
        Resampling frequency. The default value is chosen for the Northern Hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.snd_season_start(
        snd=snd,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snd_storm_days)
def snd_storm_days(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "25 cm",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Winter storm days.

    Number of days with snowfall depth accumulation greater or equal to threshold (default:
    25 cm).

    **Units:**

    - {freq}_snd_storm_days: days

    This function wraps `xclim.indicators.land.snd_storm_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snd_storm_days>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Surface snow depth.
    thresh : Any
        Threshold on snowfall depth accumulation require to label an event a `snd storm`.
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
    return xclim.indicators.land.snd_storm_days(
        snd=snd,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snow_depth)
def snow_depth(
    snd: xarray.DataArray | str = "snd",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS",
    **kwargs: Any,
) -> Any:
    """
    Mean snow depth.

    Mean of daily snow depth.

    **Units:**

    - snow_depth: cm

    This function wraps `xclim.indicators.land.snow_depth <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snow_depth>`_.

    Parameters
    ----------
    snd : xarray.DataArray | str
        Mean daily snow depth.
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
    return xclim.indicators.land.snow_depth(
        snd=snd,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snow_melt_we_max)
def snow_melt_we_max(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    window: int = 3,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Maximum snow melt.

    The water equivalent of the maximum snow melt.

    **Units:**

    - {freq}_snow_melt_we_max: kg m-2

    This function wraps `xclim.indicators.land.snow_melt_we_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snow_melt_we_max>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Snow amount (mass per area).
    window : int
        Number of days during which the melt is accumulated.
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
    return xclim.indicators.land.snow_melt_we_max(
        snw=snw,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_days_above)
def snw_days_above(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "4 kg m-2",
    freq: str = "YS-JUL",
    op: Literal[">", "gt", ">=", "ge"] = ">=",
    **kwargs: Any,
) -> Any:
    """
    Days with snow (amount).

    Number of days when the snow amount is greater than or equal to a given threshold.

    **Units:**

    - snw_days_above: days

    This function wraps `xclim.indicators.land.snw_days_above <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_days_above>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
    thresh : Any
        Threshold snow amount.
    freq : str
        Resampling frequency. The default value is chosen for the Northern hemisphere.
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
    return xclim.indicators.land.snw_days_above(
        snw=snw,
        thresh=thresh,
        freq=freq,
        op=op,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_max)
def snw_max(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Maximum snow amount.

    The maximum snow amount equivalent on the surface.

    **Units:**

    - {freq}_snw_max: kg m-2

    This function wraps `xclim.indicators.land.snw_max <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_max>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Snow amount (mass per area).
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
    return xclim.indicators.land.snw_max(
        snw=snw,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_max_doy)
def snw_max_doy(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Day of year of maximum snow amount.

    The day of year when snow amount equivalent on the surface reaches its maximum.

    **Units:**

    - {freq}_snw_max_doy: dimensionless

    This function wraps `xclim.indicators.land.snw_max_doy <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_max_doy>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
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
    return xclim.indicators.land.snw_max_doy(
        snw=snw,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_season_end)
def snw_season_end(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "4 kg m-2",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover end date (amount).

    The first date on which snow amount is below a given threshold for a given number of
    consecutive days.

    **Units:**

    - snw_season_end: dimensionless

    This function wraps `xclim.indicators.land.snw_season_end <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_season_end>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
    thresh : Any
        Threshold snow amount.
    window : int
        Minimum number of days with snow water below the threshold.
    freq : str
        Resampling frequency. The default value is chosen for the Northern Hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.snw_season_end(
        snw=snw,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_season_length)
def snw_season_length(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "4 kg m-2",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover duration (amount).

    The season starts when the snow amount is above a threshold for at least `N` consecutive
    days and stops when it drops below the same threshold for the same number of days.

    **Units:**

    - snw_season_length: days

    This function wraps `xclim.indicators.land.snw_season_length <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_season_length>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
    thresh : Any
        Threshold snow amount.
    window : int
        Minimum number of days with snow amount above and below threshold.
    freq : str
        Resampling frequency. The default value is chosen for the northern hemisphere.
    ds : xarray.Dataset | Any
        Input dataset.
    **kwargs : Any
        Additional keyword arguments.

    Returns
    -------
    Any
        The computed index.
    """
    return xclim.indicators.land.snw_season_length(
        snw=snw,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_season_start)
def snw_season_start(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "4 kg m-2",
    window: int = 14,
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Snow cover start date (amount).

    The first date on which snow amount is greater than or equal to a given threshold for a
    given number of consecutive days.

    **Units:**

    - snw_season_start: dimensionless

    This function wraps `xclim.indicators.land.snw_season_start <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_season_start>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
    thresh : Any
        Threshold snow amount.
    window : int
        Minimum number of days with snow amount above or equal to the threshold.
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
    return xclim.indicators.land.snw_season_start(
        snw=snw,
        thresh=thresh,
        window=window,
        freq=freq,
        ds=ds,
        **kwargs,
    )


@format_handler()
# @metadata_handler(xclim.indicators.land.snw_storm_days)
def snw_storm_days(
    snw: xarray.DataArray | str = "snw",
    ds: xarray.Dataset | Any = None,
    *,
    thresh: Any = "10 kg m-2",
    freq: str = "YS-JUL",
    **kwargs: Any,
) -> Any:
    """
    Winter storm days.

    Number of days with snowfall amount accumulation greater or equal to threshold (default:
    10 kg m-2).

    **Units:**

    - {freq}_snw_storm_days: days

    This function wraps `xclim.indicators.land.snw_storm_days <https://xclim.readthedocs.io/en/stable/api_indicators.html#xclim.indicators.land.snw_storm_days>`_.

    Parameters
    ----------
    snw : xarray.DataArray | str
        Surface snow amount.
    thresh : Any
        Threshold on snowfall amount accumulation require to label an event a `snw storm`.
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
    return xclim.indicators.land.snw_storm_days(
        snw=snw,
        thresh=thresh,
        freq=freq,
        ds=ds,
        **kwargs,
    )
