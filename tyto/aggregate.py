import xarray as xr

from .options import HOW_DICT

#: Mapping from pandas frequency strings to xarray time groups
_PANDAS_FREQUENCIES = {
    "D": "dayofyear",
    "W": "weekofyear",
    "M": "month",
}

#: The maximum limit of climatology time groups
_BIN_MAXES = {
    "dayofyear": 366,
    "weekofyear": 53,
    "month": 12,
    "season": 4,
}


def daily_mean(datarray, **kwargs):
    """
    Calculate the daily mean.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(datarray, frequency="D", dim="time", how="mean", **kwargs)


def daily_max(datarray, **kwargs):
    """
    Calculate the daily max.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(datarray, frequency="D", dim="time", how="max", **kwargs)


def daily_min(datarray, **kwargs):
    """
    Calculate the daily min.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(datarray, frequency="D", dim="time", how="min", **kwargs)


def monthly_mean(datarray, **kwargs):
    """
    Calculate the monthly mean.

    Parameters
    ----------
    dataarray : xr.DataArray
        DataArray containing a `time` dimension.
    **kwargs
        Keyword arguments to be passed to :func:`resample`.

    Returns
    -------
    xr.DataArray
    """
    return resample(datarray, frequency="M", dim="time", how="mean", **kwargs)


def resample(
    dataarray: xr.DataArray,
    frequency: str,
    dim: str = "time",
    how: str = "mean",
    closed: str = "left",
    label: str = "left",
    skipna: bool = True,
    **kwargs,
) -> xr.DataArray:
    resample = dataarray.resample(
        label=label, closed=closed, skipna=skipna, **{dim: frequency}, **kwargs
    )
    result = resample.__getattribute__(how)(dim)
    return result


def groupby(
    dataarray: xr.DataArray,
    frequency: str = None,
    bin_widths: int = None,
    squeeze: bool = True,
):
    if frequency is None:
        try:
            frequency = xr.infer_freq(dataarray.time)
        except:  # noqa: E722
            raise ValueError(
                "Unable to infer time frequency from data; please pass the "
                "'frequency' argument explicitly"
            )
        frequency, possible_bins = _pandas_frequency_and_bins(frequency)
        bin_widths = bin_widths or possible_bins

    if bin_widths is not None:
        return _groupby_bins(dataarray, frequency, bin_widths, squeeze)

    try:
        grouped_data = dataarray.groupby(f"time.{frequency}", squeeze=squeeze)
    except AttributeError:
        raise ValueError(
            f"Invalid frequency '{frequency}' - see xarray documentation for "
            f"a full list of valid frequencies."
        )
    return grouped_data


def _groupby_bins(
    dataarray: xr.DataArray,
    frequency: str,
    bin_widths: int,
    squeeze: bool,
):
    if not isinstance(bin_widths, (list, tuple)):
        max_value = _BIN_MAXES[frequency]
        bin_widths = list(range(0, max_value + 1, bin_widths))
    try:
        grouped_data = dataarray.groupby_bins(
            f"time.{frequency}", bin_widths, squeeze=squeeze
        )
    except AttributeError:
        raise ValueError(
            f"Invalid frequency '{frequency}' - see xarray documentation for "
            f"a full list of valid frequencies."
        )
    return grouped_data


def _pandas_frequency_and_bins(
    frequency: str,
) -> tuple:
    freq = frequency.lstrip("0123456789")
    bins = frequency[: -len(freq)] or None
    freq = _PANDAS_FREQUENCIES.get(freq.lstrip(" "), frequency)
    return freq, bins



def rolling_reduce(
        dataarray: xr.DataArray,
        how='mean',
        q=[50],
        dropna_how=None,
        **kwargs
) -> xr.DataArray:
    """Return reduced data using a moving window over which to apply the reduction.

    Parameters
    ----------
    dataarray : xr.DataArray
        Data over which the moving window is applied according to the reduction method.
    min_periods (optional) : integer 
        The minimum number of observations in the window required to have a value
        (otherwise result is NaN). Default is to set **min_periods** equal to the size of the window.
    center (optional): bool
        Set the labels at the centre of the window.
    how (optional) : str,
        Function to be applied for reduction. Default is 'mean'.
    q (optional): float, 
        Value of percentile to be used if **how** == 'percentile'
    dropna_how (str, optional): Determine if dimension is removed from the output when we have at least one NaN or
        all NaN. **dropna_how** can be either 'any' or 'all'. Default is 'any'.
    **windows (dim=window): where **dim** is str dtype and corresponds to the dimension that the rolling
        iterator is created along (e.g., time), and **window** is int dtype corresponding to the size of the moving
        window.

    Returns
    -------
    xr.DataArray
    """
    window_dims = [
        _dim for _dim in list(dataarray.dims) if _dim in list(kwargs)
    ]
    accepted_rolling_kwargs = ['min_periods', 'center'] + window_dims
    rolling_kwargs {
        _kwarg: kwargs.pop(_kwarg) for _kwarg in kwargs
        if _kwarg in accepted_rolling_kwargs
    }

    dropna_how = kwargs.pop('dropna_how', None)

    how_reduce = kwargs.pop('how', 'mean')

    # Any kwargs left after above reductions are kwargs for reduction method
    reduce_kwargs = kwargs

    # Create rolling groups:
    data_rolling = dataarray.rolling(**rolling_kwargs)


    in_built_how_methods = [
        method for method in dir(data_rolling)
        if not method.startswith('_')
    ]
    if how_reduce in in_built_how_methods:
        data_windowed = data_rolling.__getattribute__(how)(**reduce_kwargs)
    else:
        data_windowed = data_rolling.reduce(
            HOW_DICT[how_reduce], reduce_kwargs
        )

    if 'dropna_how' is not None:
        for dim in window_dims:
            data_windowed = data_windowed.dropna(dim, how=dropna_how)

    data_windowed.attrs.update(dataarray.attrs)
    
    return data_windowed