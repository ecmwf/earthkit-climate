# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import pytest

from earthkit.climate.sample_source import SampleSource


def test_sample_source_with_valid_name():
    with pytest.warns(UserWarning):
        SampleSource("tasmax_ACCESS-CM2_historical_reference")


def test_sample_source_with_invalid_name():
    with pytest.raises(ValueError):
        SampleSource("foobar")
