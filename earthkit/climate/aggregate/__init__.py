"""
Aggregation tools for meteorological and climate data..

.. automodule:: earthkit.climate.aggregate.temporal
  :noindex:
"""

from earthkit.climate.aggregate import climatology, spatial, temporal

try:
    from earthkit.data.utils.module_inputs_wrapper import (
        transform_function_inputs,
        transform_module_inputs,
    )
except ImportError:
    pass
else:
    temporal = transform_module_inputs(temporal)

    climatology = transform_module_inputs(climatology)

    spatial = transform_module_inputs(spatial)

from earthkit.climate.aggregate.general import reduce, resample, rolling_reduce

reduce = transform_function_inputs(reduce)
rolling_reduce = transform_function_inputs(rolling_reduce)
resample = transform_function_inputs(resample)

__all__ = [
    "__version__",
    "temporal",
    "climatology",
    "spatial",
    "reduce",
    "resample",
    "rolling_reduce",
]
