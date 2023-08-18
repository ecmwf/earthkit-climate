"""Statistical analysis tools for meteorological and climate data.."""

# Copyright 2022, European Centre for Medium Range Weather Forecasts.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    # NOTE: the `version.py` file must not be present in the git repository
    #   as it is generated by setuptools at install time
    from .version import __version__
except ImportError:  # pragma: no cover
    # Local copy or not installed with setuptools
    __version__ = "999"



from earthkit.climate import aggregate, climatology
try:
    from earthkit.data.utils.module_inputs_wrappers import transform_module_inputs
except:
    pass
else:
    import xarray as xr

    KWARG_TYPES = {
        "dataarray": xr.DataArray,
        "dataset": xr.Dataset,
    }

    aggregate = transform_module_inputs(aggregate, kwarg_types=KWARG_TYPES)

    climatology = transform_module_inputs(climatology, kwarg_types=KWARG_TYPES)


__all__ = [
    "__version__",
    "aggregate",
    "climatology",
]
