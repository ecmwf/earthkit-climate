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


def generate_sample_dataset(
    start_date: str,
    end_date: str,
    *,
    tas_value: float = 20.0,
    hurs_value: float = 70.0,
    pr_value: float = 0.0,
) -> xr.Dataset:
    """Generate a daily sample dataset for climate-indicator examples.

    Parameters
    ----------
    start_date : str
        First date in the dataset, in a format accepted by
        :func:`xarray.date_range`.
    end_date : str
        Last date in the dataset, in a format accepted by
        :func:`xarray.date_range`. The date is included in the dataset.
    tas_value : float, default: 20.0
        Constant daily mean near-surface air temperature, in degrees Celsius.
    hurs_value : float, default: 70.0
        Constant daily mean relative humidity, in percent.
    pr_value : float, default: 0.0
        Constant daily precipitation rate, in millimetres per day.

    Returns
    -------
    xarray.Dataset
        Dataset containing daily ``tas``, ``hurs``, and ``pr`` variables with
        units, standard names, and cell methods.
    """
    time = xr.date_range(start=start_date, end=end_date, freq="D")
    shape = time.size

    tas = xr.DataArray(
        np.full(shape, tas_value),
        coords={"time": time},
        dims="time",
        name="tas",
        attrs={
            "units": "degC",
            "standard_name": "air_temperature",
            "cell_methods": "time: mean within days",
        },
    )
    hurs = xr.DataArray(
        np.full(shape, hurs_value),
        coords={"time": time},
        dims="time",
        name="hurs",
        attrs={
            "units": "%",
            "standard_name": "relative_humidity",
            "cell_methods": "time: mean within days",
        },
    )
    pr = xr.DataArray(
        np.full(shape, pr_value),
        coords={"time": time},
        dims="time",
        name="pr",
        attrs={
            "units": "mm/day",
            "standard_name": "precipitation_flux",
            "cell_methods": "time: mean within days",
        },
    )

    return xr.Dataset({"tas": tas, "hurs": hurs, "pr": pr})


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


def _generate_fusarium_input_timeseries(
    start_date: str = "2020-01-01",
    end_date: str = "2021-12-31",
    **kwargs: Any,
) -> xr.Dataset:
    """
    Generate synthetic daily time series for the Fusarium head blight indicator tutorial.

    Creates a two-year daily time series (2020-2021) with temperature, relative humidity,
    and precipitation. Days that satisfy all FHB-conducive conditions (3 days in 2020,
    4 days in 2021) as well as controlled near-miss days are baked into the dataset.

    Parameters
    ----------
    start_date : str, default: "2020-01-01"
        First date in the dataset, in a format accepted by
        :func:`xarray.date_range`.
    end_date : str, default: "2021-12-31"
        Last date in the dataset, in a format accepted by
        :func:`xarray.date_range`.
    **kwargs : Any
        Additional keyword arguments forwarded to :func:`generate_sample_dataset`.

    Returns
    -------
    xr.Dataset
        Dataset containing daily ``tas``, ``hurs``, and ``pr`` variables with
        FHB-conducive conditions and near misses baked in.
    """
    ds = generate_sample_dataset(start_date=start_date, end_date=end_date, **kwargs)

    fhb_dates_2020 = ["2020-06-10", "2020-06-11", "2020-06-20"]
    fhb_dates_2021 = ["2021-05-15", "2021-05-16", "2021-05-17", "2021-05-30"]
    fhb_dates = fhb_dates_2020 + fhb_dates_2021

    time_strings = ds.indexes["time"].strftime("%Y-%m-%d")
    valid_fhb = [d for d in fhb_dates if d in time_strings]
    if valid_fhb:
        ds["hurs"].loc[{"time": valid_fhb}] = 95.0
        ds["pr"].loc[{"time": valid_fhb}] = 1.0

    if "2020-06-25" in time_strings:
        ds["tas"].loc[{"time": "2020-06-25"}] = 31.0
        ds["hurs"].loc[{"time": "2020-06-25"}] = 95.0
        ds["pr"].loc[{"time": "2020-06-25"}] = 1.0
    if "2021-06-01" in time_strings:
        ds["tas"].loc[{"time": "2021-06-01"}] = 20.0
        ds["hurs"].loc[{"time": "2021-06-01"}] = 85.0
        ds["pr"].loc[{"time": "2021-06-01"}] = 1.0
    if "2021-06-02" in time_strings:
        ds["tas"].loc[{"time": "2021-06-02"}] = 20.0
        ds["hurs"].loc[{"time": "2021-06-02"}] = 95.0
        ds["pr"].loc[{"time": "2021-06-02"}] = 0.0

    return ds


_SYNTHETIC_DATASETS: dict[str, Any] = {
    "synthetic-daily-temperature": _generate_synthetic_daily_temperature,
    "synthetic-daily-dask-temperature": _generate_synthetic_daily_dask_temperature,
    "synthetic-daily-station-temperature": _generate_synthetic_daily_station_temperature,
    "fusarium-input-timeseries": _generate_fusarium_input_timeseries,
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

    def to_xarray(self, **kwargs: Any) -> xr.DataArray | xr.Dataset:
        """
        Convert source dataset to an xarray DataArray or Dataset.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to xarray or synthetic generator.

        Returns
        -------
        xr.DataArray | xr.Dataset
            Synthetic or loaded xarray DataArray or Dataset.
        """
        if self._name in _SYNTHETIC_DATASETS:
            call_kwargs = {**self._kwargs, **kwargs}
            generator = _SYNTHETIC_DATASETS[self._name]
            try:
                return generator(**call_kwargs)
            except TypeError:
                return generator()
        return super().to_xarray(**kwargs)

    def to_dataframe(self, **kwargs: Any) -> pd.DataFrame:
        """
        Convert source dataset to a pandas DataFrame.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to :meth:`to_xarray`.

        Returns
        -------
        pd.DataFrame
            Synthetic or loaded dataset converted to a pandas DataFrame.
        """
        obj = self.to_xarray(**kwargs)
        return obj.to_dataframe()

    def to_pandas(self, **kwargs: Any) -> pd.DataFrame:
        """
        Convert source dataset to a pandas DataFrame.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to :meth:`to_dataframe`.

        Returns
        -------
        pd.DataFrame
            Synthetic or loaded dataset converted to a pandas DataFrame.
        """
        return self.to_dataframe(**kwargs)


source = SampleSource
