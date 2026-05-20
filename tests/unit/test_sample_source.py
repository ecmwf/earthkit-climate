# (C) Copyright 2026- ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.


import pytest

from earthkit.climate.sample_source import SampleSource


def test_sample_source_with_valid_name():
    with pytest.warns(UserWarning):
        SampleSource("tasmax_ACCESS-CM2_historical_reference")


def test_sample_source_with_invalid_name():
    with pytest.raises(ValueError):
        SampleSource("foobar")
