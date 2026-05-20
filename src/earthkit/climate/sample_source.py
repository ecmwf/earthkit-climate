# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""Source plugin for earthkit-data to access sample data of earthkit-climate."""

import warnings

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


class SampleSource(Source):
    # Notify the user to not rely on these datasets once
    __has_notified = False

    def __init__(self, name, **kwargs):
        super().__init__()
        self._kwargs = kwargs

        if name not in _SAMPLE_DATA_URLS:
            raise ValueError(f"Unknown sample dataset: {name!r}")
        self._name = name

        if not self.__has_notified:
            self.__class__.__has_notified = True
            warnings.warn(
                "earthkit-climate-sample datasets are made available for demonstration purposes only. "
                "Files are not guaranteed to be available long-term and may change over time. "
                "Please use official channels to obtain the contained datasets reliably for other purposes."
            )

    def mutate(self):
        return _from_source_internal("url", _SAMPLE_DATA_URLS[self._name], **self._kwargs)


source = SampleSource
