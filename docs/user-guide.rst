.. SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

User guide
==========

Example usage:

.. code-block:: python

   from earthkit.climate.indicators import precipitation, temperature
   from earthkit.climate.utils import conversions

   # Example: compute a precipitation index
   pr = precipitation.simple_daily_intensity(precip_data, freq="monthly")
