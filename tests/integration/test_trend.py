# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest

from earthkit.climate.utils import linear_trend


@pytest.mark.integration
def test_linear_trend_on_sample_dataset(data_cache):
    tasmax = data_cache["tasmax_ACCESS-CM2_historical_reference"]["tasmax"]
    trend, p_values = linear_trend(tasmax, return_p_values=True)
    trend, p_values = trend.compute(), p_values.compute()
    values = tasmax.compute().values.reshape(tasmax.sizes["time"], -1)
    valid = np.isfinite(values)
    valid_points = np.flatnonzero(valid.sum(axis=0) >= 2)
    assert valid_points.size > 0, "sample dataset has no grid point with at least two valid time steps"
    spatial_dims = ["lat", "lon"]
    assert trend.dims == tuple(spatial_dims)
    assert p_values.dims == tuple(spatial_dims)
    assert trend.attrs["units"] == f"{tasmax.attrs['units']} year-1"
    assert p_values.attrs["units"] == "1"
