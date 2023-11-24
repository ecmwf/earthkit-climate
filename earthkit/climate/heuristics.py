"""Heuristics methods for climate indicators."""
import typing as T

import numpy as np


def growing_degree_days(
    tas_mean: T.Union[None, np.ndarray] = None,
    tas_max: T.Union[None, np.ndarray] = None,
    tas_min: T.Union[None, np.ndarray] = None,
    tas_base: float = 0.0,
    time_axis: int = 0,
    time_start_index: int = 0,
    time_stop_index: T.Union[None, int] = None,
) -> np.ndarray:
    """Return the Growing Degree Days (GDD) index calculated from daily Near-Surface Air Temperature data.

    Growing degrees days (GDD) is defined as the mean daily temperature (`tas_mean`), or the average of daily
    maximum and minimum temperatures (`tas_max` and `tas_min`), above a certain tas_base base temperature
    (`tas_base`) accumulated on a daily basis over a period of time. https://doi.org/10.1002/joc.4535

    Parameters
    ----------
    tas_mean : numpy.ndarray
        Daily mean Near-Surface Air Temperature. Required if tas_min and tax_max not provided.
    tas_max : numpy.ndarray
        Daily maximum Near-Surface Air Temperature. Required if tas_mean not provided.
    tas_min : numpy.ndarray
        Daily minimum Near-Surface Air Temperature. Must be same units and dimensions as tas_max.
        Required if tas_mean not provided.
    tas_base : float
        Threshold temperature for the GDD index calculation, must be in same units as the tas array[s].
    time_axis : int (optional)
        axis of the time dimension in the tas array, default is 0
    time_start_index : int (optional)
        Start index to start accumulating degree days, default is 0
    time_stop_index : int (optional)
        Stop index to start accumulating degree days, default is None, i.e. end of array

    Returns
    -------
        numpy.ndarray: Growing Degree Days index.

    """
    # Check we have either tas_mean, or tas_min and tax_max
    l_tas_mean = tas_mean is not None
    l_tas_minmax = tas_min is not None and tas_max is not None

    if l_tas_mean and not l_tas_minmax:
        gdu = tas_mean - tas_base
    elif l_tas_minmax and not l_tas_mean:
        gdu = (tas_max + tas_min) / 2 - tas_base
    elif l_tas_mean and l_tas_minmax:
        raise AssertionError("Please provide tas_mean OR tas_min+tas_max.")
    else:
        raise AssertionError("Insufficient arguments provided.")

    gdu[gdu < 0.0] = 0.0
    _gdu = np.rollaxis(gdu, time_axis)

    gdd = np.zeros_like(gdu)
    _gdd = np.rollaxis(gdd, time_axis)

    if time_stop_index is not None:
        _gdd[time_start_index:time_stop_index] = np.cumsum(_gdu[time_start_index:time_stop_index], axis=0)
    else:
        _gdd[time_start_index:] = np.cumsum(_gdu[time_start_index:], axis=0)

    return gdd


def heating_degree_days(
    tas_max: np.ndarray,
    tas_mean: np.ndarray,
    tas_min: np.ndarray,
    tas_base: float,
) -> np.ndarray:
    """Return daily heating degree days.

    The heating degree days are computed using Spinoni's method which is used by the European
    Environmental Agency (EEA). The method is described in the following
    `paper (Spinoni et al., 2018) <https://doi.org/10.1002/joc.5362>`_.

    Parameters
    ----------
    tas_max : numpy.ndarray
        Daily maximum Near-Surface Air Temperature. Must be same units and dimensions as tas_mean and tas_min.
    tas_mean : numpy.ndarray
        Daily mean Near-Surface Air Temperature. Must be same units and dimensions as tas_max and tas_min.
    tas_min : numpy.ndarray
        Daily minimum Near-Surface Air Temperature. Must be same units and dimensions as tas_max and tas_mean.
    tas_base: float
        Threshold temperature for the HDD index calculation, must be in same units as the tas arrays.

    Returns
    -------
        numpy.ndarray: Daily heating degree days.


    """
    hdd = np.zeros_like(tas_mean)
    _mask = tas_base >= tas_max
    hdd[_mask] = tas_base - tas_mean[_mask]
    _mask = (tas_base < tas_max) & (tas_base >= tas_mean)
    hdd[_mask] = (tas_base - tas_min[_mask]) / 2 - (tas_max[_mask] - tas_base) / 4
    _mask = (tas_base < tas_mean) & (tas_base >= tas_min)
    hdd[_mask] = (tas_base - tas_min[_mask]) / 4

    return hdd


def cooling_degree_days(
    tas_max: np.ndarray,
    tas_mean: np.ndarray,
    tas_min: np.ndarray,
    tas_base: float,
) -> np.ndarray:
    """Return daily cooling degree days.

    The cooling degree days are computed using Spinoni's method which is used by the European
    Environmental Agency (EEA). The method is described in the following
    `paper (Spinoni et al., 2018) <https://doi.org/10.1002/joc.5362>`_.

    Parameters
    ----------
    tas_max : numpy.ndarray
        Daily maximum Near-Surface Air Temperature. Must be same units and dimensions as tas_mean and tas_min.
    tas_mean : numpy.ndarray
        Daily mean Near-Surface Air Temperature. Must be same units and dimensions as tas_max and tas_min.
    tas_min : numpy.ndarray
        Daily minimum Near-Surface Air Temperature. Must be same units and dimensions as tas_max and tas_mean.
    tas_base: float
        Threshold temperature for the CDD index calculation, must be in same units as the tas arrays.

    Returns
    -------
        numpy.ndarray: Daily cooling degree days.


    """
    cdd = np.zeros_like(tas_mean)
    _mask = tas_base < tas_max
    cdd[_mask] = tas_mean[_mask] - tas_base
    _mask = (tas_base < tas_max) & (tas_base >= tas_mean)
    cdd[_mask] = (tas_max[_mask] - tas_base) / 4
    _mask = (tas_base < tas_mean) & (tas_base >= tas_min)
    cdd[_mask] = (tas_max[_mask] - tas_base) / 2 - (tas_base - tas_min[_mask]) / 4

    return cdd
