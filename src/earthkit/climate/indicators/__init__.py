# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""
:py:mod:`earthkit.climate.indicators` leverages indicator definitions from
``xclim``, which provide metadata and validation facilities (health checks) of
the input and include attributes for CF metadata (cell methods), references,
keywords, and more.
"""

from .atmos import precipitation, synoptic, temperature, wind
from .land import hydrology, land, snow
from .ocean import sea_ice

__all__ = [
    "precipitation",
    "synoptic",
    "temperature",
    "wind",
    "hydrology",
    "land",
    "snow",
    "sea_ice",
]
