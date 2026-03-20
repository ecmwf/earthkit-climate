# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""
Utility for loading sample CMIP6 datasets for testing and benchmarking.

This module provides a centralized source for dataset URLs and a loading
function that uses earthkit-data's caching mechanism.
"""

import os

import earthkit.data
import xarray as xr

# ---------------------------------------------------------------------------
# Dataset URLs
# ---------------------------------------------------------------------------

SAMPLE_DATA_URLS: dict[str, str] = {
    # Main descriptive keys
    "tasmax_ACCESS-CM2_historical_reference": (
        "https://sites.ecmwf.int/repository/earthkit-climate/tasmax_ACCESS-CM2_historical_reference.nc"
    ),
    "tasmin_ACCESS-CM2_historical_reference": (
        "https://sites.ecmwf.int/repository/earthkit-climate/tasmin_ACCESS-CM2_historical_reference.nc"
    ),
    "tasmax_ACCESS-CM2_ssp585_far_future": (
        "https://sites.ecmwf.int/repository/earthkit-climate/tasmax_ACCESS-CM2_ssp585_far_future.nc"
    ),
    "tasmin_ACCESS-CM2_ssp585_far_future": (
        "https://sites.ecmwf.int/repository/earthkit-climate/tasmin_ACCESS-CM2_ssp585_far_future.nc"
    ),
    "pr_ACCESS-CM2_historical_reference": (
        "https://sites.ecmwf.int/repository/earthkit-climate/pr_ACCESS-CM2_historical_reference.nc"
    ),
    "pr_ACCESS-CM2_ssp585_far_future": (
        "https://sites.ecmwf.int/repository/earthkit-climate/pr_ACCESS-CM2_ssp585_far_future.nc"
    ),
}


def load_sample_datasets(
    keys: list[str] | None = None,
    cache_dir: str | None = None,
) -> dict[str, xr.Dataset]:
    """
    Download or use cached CMIP6 datasets required for testing.

    Uses earthkit-data's URL source with a user-level cache.

    Parameters
    ----------
    keys : list[str], optional
        Subset of dataset keys to load. If None, all are loaded.
    cache_dir : str, optional
        Custom cache directory. Defaults to ~/.cache/earthkit/data.

    Returns
    -------
    dict[str, xr.Dataset]
        Mapping from short name to xarray Dataset.
    """
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/earthkit/data")

    os.makedirs(cache_dir, exist_ok=True)
    earthkit.data.config.set({
        "cache-policy": "user",
        "temporary-directory-root": cache_dir,
    })

    target_keys = keys if keys is not None else list(SAMPLE_DATA_URLS.keys())
    datasets: dict[str, xr.Dataset] = {}

    for key in target_keys:
        if key not in SAMPLE_DATA_URLS:
            raise ValueError(f"Unknown sample dataset key: {key}")
        url = SAMPLE_DATA_URLS[key]
        ds = earthkit.data.from_source("url", url).to_xarray()
        datasets[key] = ds

    return datasets
