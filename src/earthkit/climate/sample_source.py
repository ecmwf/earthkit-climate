# SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

"""Source plugin for earthkit-data to access sample data of earthkit-climate."""

import warnings
from typing import Any

import numpy as np
import pandas as pd
import xarray as xr
from earthkit.data.sources import Source, _from_source_internal

# ---------------------------------------------------------------------------
# Dataset URLs
# ---------------------------------------------------------------------------
_SITES_URL = "https://sites.ecmwf.int/repository/earthkit-climate"

_SAMPLE_DATA_URLS: dict[str, str] = {
    # Main descriptive keys
    "tasmax_ACCESS-CM2_historical_reference": f"{_SITES_URL}/tasmax_ACCESS-CM2_historical_reference.nc",
    "tasmin_ACCESS-CM2_historical_reference": f"{_SITES_URL}/tasmin_ACCESS-CM2_historical_reference.nc",
    "tasmax_ACCESS-CM2_ssp585_far_future": f"{_SITES_URL}/tasmax_ACCESS-CM2_ssp585_far_future.nc",
    "tasmin_ACCESS-CM2_ssp585_far_future": f"{_SITES_URL}/tasmin_ACCESS-CM2_ssp585_far_future.nc",
    "pr_ACCESS-CM2_historical_reference": f"{_SITES_URL}/pr_ACCESS-CM2_historical_reference.nc",
    "pr_ACCESS-CM2_ssp585_far_future": f"{_SITES_URL}/pr_ACCESS-CM2_ssp585_far_future.nc",
}


def _generate_synthetic_daily_temperature() -> xr.DataArray:
    """
    Generate synthetic 1D daily maximum temperature DataArray.

    Creates a multi-year daily time series (1991-2023) of maximum air temperature
    in Kelvin with seasonal variation and reproducible noise, containing complete
    CF metadata and cell methods.

    Returns
    -------
    xr.DataArray
        Synthetic daily maximum temperature DataArray.
    """
    dates = pd.date_range("1991-01-01", "2023-12-31", freq="D")
    rng = np.random.default_rng(42)
    temp_values = 285.0 + 15.0 * np.sin(2 * np.pi * dates.dayofyear / 365.25) + rng.normal(0, 3, len(dates))

    return xr.DataArray(
        temp_values,
        coords={"time": dates},
        dims=["time"],
        name="tasmax",
        attrs={
            "units": "K",
            "standard_name": "air_temperature",
            "cell_methods": "time: maximum",
        },
    )


def _generate_synthetic_daily_dask_temperature() -> xr.DataArray:
    """
    Generate synthetic 3D dask-backed daily maximum temperature DataArray.

    Creates a 10-year daily spatial grid (time, lat, lon) backed by Dask arrays
    for scalability demonstrations, containing complete CF metadata and cell methods.

    Returns
    -------
    xr.DataArray
        Synthetic spatial-temporal maximum temperature DataArray backed by Dask.
    """
    try:
        import dask.array as da
    except ImportError as err:
        raise ImportError(
            "The 'dask' package is required to generate the 'synthetic-daily-dask-temperature' sample dataset."
        ) from err

    dates = pd.date_range("2010-01-01", "2019-12-31", freq="D")
    lats = np.linspace(35, 60, 20)
    lons = np.linspace(-10, 30, 20)

    dask_data = da.random.normal(285.0, 10.0, size=(len(dates), len(lats), len(lons)), chunks=(365, 10, 10))

    return xr.DataArray(
        dask_data,
        coords={"time": dates, "lat": lats, "lon": lons},
        dims=["time", "lat", "lon"],
        name="tasmax",
        attrs={
            "units": "K",
            "standard_name": "air_temperature",
            "cell_methods": "time: maximum",
        },
    )


def _generate_synthetic_daily_station_temperature() -> xr.DataArray:
    """
    Generate synthetic daily maximum temperature DataArray for multiple in-situ stations.

    Creates a multi-year daily time series (1991-2023) across 5 weather stations
    with station coordinates (latitude, longitude, elevation), seasonal variations,
    and station-specific temperature offsets, containing complete CF metadata.

    Returns
    -------
    xr.DataArray
        Synthetic station daily maximum temperature DataArray.
    """
    dates = pd.date_range("1991-01-01", "2023-12-31", freq="D")
    station_ids = ["ST01", "ST02", "ST03", "ST04", "ST05"]
    lats = np.array([42.5, 43.1, 41.8, 42.9, 43.5])
    lons = np.array([1.5, 2.1, 0.9, 1.8, 2.4])
    heights = np.array([1050.0, 450.0, 150.0, 1850.0, 800.0])

    base_temps = 288.0 - (heights / 1000.0) * 6.5
    rng = np.random.default_rng(42)

    seasonal = 14.0 * np.sin(2 * np.pi * (dates.dayofyear.values[:, None] - 80) / 365.25)
    noise = rng.normal(0, 2.5, size=(len(dates), len(station_ids)))
    temp_values = base_temps[None, :] + seasonal + noise

    return xr.DataArray(
        temp_values,
        coords={
            "time": dates,
            "station_id": station_ids,
            "lat": ("station_id", lats, {"standard_name": "latitude", "units": "degrees_north"}),
            "lon": ("station_id", lons, {"standard_name": "longitude", "units": "degrees_east"}),
            "height": ("station_id", heights, {"standard_name": "height", "units": "m"}),
        },
        dims=["time", "station_id"],
        name="tasmax",
        attrs={
            "units": "K",
            "standard_name": "air_temperature",
            "cell_methods": "time: maximum",
        },
    )


_SYNTHETIC_DATASETS: dict[str, Any] = {
    "synthetic-daily-temperature": _generate_synthetic_daily_temperature,
    "synthetic-daily-dask-temperature": _generate_synthetic_daily_dask_temperature,
    "synthetic-daily-station-temperature": _generate_synthetic_daily_station_temperature,
}


class SampleSource(Source):
    """
    Source plugin for retrieving sample datasets for earthkit-climate.

    Provides access to cached remote sample NetCDF files as well as on-the-fly
    generated synthetic datasets with CF-compliant metadata.
    """

    # Notify the user to not rely on these datasets once
    __has_notified = False

    def __init__(self, name: str, **kwargs: Any) -> None:
        """
        Initialize the SampleSource.

        Parameters
        ----------
        name : str
            Name of the sample or synthetic dataset to retrieve.
        **kwargs : Any
            Additional keyword arguments passed to earthkit-data.

        Returns
        -------
        None
        """
        super().__init__()
        self._kwargs = kwargs

        if name not in _SAMPLE_DATA_URLS and name not in _SYNTHETIC_DATASETS:
            raise ValueError(f"Unknown sample dataset: {name!r}")
        self._name = name

        if not self.__has_notified:
            self.__class__.__has_notified = True
            warnings.warn(
                "earthkit-climate-sample datasets are made available for demonstration purposes only. "
                "Files are not guaranteed to be available long-term and may change over time. "
                "Please use official channels to obtain the contained datasets reliably for other purposes."
            )

    def mutate(self) -> Any:
        """
        Mutate source to underlying URL source for remote datasets.

        Returns
        -------
        Any
            Mutated source object or self for synthetic datasets.
        """
        if self._name in _SYNTHETIC_DATASETS:
            return self
        return _from_source_internal("url", _SAMPLE_DATA_URLS[self._name], **self._kwargs)

    def to_xarray(self, **kwargs: Any) -> xr.DataArray:
        """
        Convert source dataset to an xarray DataArray.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to xarray.

        Returns
        -------
        xr.DataArray
            Synthetic or loaded xarray DataArray.
        """
        if self._name in _SYNTHETIC_DATASETS:
            return _SYNTHETIC_DATASETS[self._name]()
        return super().to_xarray(**kwargs)


source = SampleSource
