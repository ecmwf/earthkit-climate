.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_climate_indicators:

Climate indicators in earthkit
==============================

This page explains what **earthkit-climate** understands as a climate indicator and outlines where to start when calculating climate indicators within the broader **earthkit** ecosystem.


What is a climate indicator?
----------------------------

In climate science, meteorological variables (such as 2-metre temperature, precipitation, or surface wind speed) describe instantaneous or high-frequency atmospheric states. A **climate indicator** transforms these variables into meaningful metrics that characterize climate variability, extremes, and long-term trends, as well as their potential impacts. Many indicators are designed to quantify climate conditions relevant to specific impacts in sectors such as health, agriculture, ecosystems, energy, and water resources.

In **earthkit-climate**, indicators follow standardized definitions (e.g., WMO/ETCCDI) and provide a unified interface for processing both multidimensional gridded datasets (e.g., ERA5, CMIP6, CORDEX) and 1D in-situ / station time series. They accept **earthkit-data** or **xarray** objects and return indicator datasets with enriched CF-compliant metadata (e.g., standard names, cell methods, and updated units).


Anatomy of a climate indicator
------------------------------

Rather than rigid output categories, a climate indicator is best understood in terms of the fundamental **ingredients** that compose it:

* **Input variables**:

  * *Single-variable*: Process a single meteorological field (e.g., daily maximum temperature for :code:`tx_days_above`).
  * *Multi-variable*: Combine multiple fields (e.g., temperature and precipitation/evapotranspiration for drought indicators like SPEI, or wind and temperature for wildfire or heat-stress metrics).

* **Thresholds and conditions**:

  * *Fixed thresholds*: Constant physical values (e.g., frost days with :code:`thresh="0 degC"` or hot days with :code:`thresh="300 K"`).
  * *Adaptive / climatological thresholds*: Percentile-based values calculated relative to a baseline reference period (e.g., warm days :code:`tx90p` counting days exceeding the 90th percentile).
  * *Sequence and duration conditions*: Multi-day persistent conditions (e.g., heatwave duration indices).

* **Reduction and aggregation**:

  * *Threshold counts*: Counting the number of days or events meeting a specified condition within a target period (e.g., annual, seasonal, monthly).
  * *Cumulative metrics*: Accumulation of values over time (e.g., growing degree days, heating/cooling degree days).
  * *Extremes and statistics*: Extracting maximum, minimum, or percentile values over temporal windows (e.g., maximum 5-day precipitation :code:`rx5day`).


Building blocks vs. domain indicators
-------------------------------------

Understanding these ingredients helps clarify how functionality is divided across the **earthkit** ecosystem:

* **earthkit-transforms** provides generic, low-level building blocks and operations (e.g., computing climatological baselines, percentiles, or generic spatial and temporal aggregations).
* **earthkit-climate** provides domain-specific, preconfigured, and standardized climate indicators (such as ETCCDI or WMO indices) with rich CF-compliant metadata out of the box.

Use **earthkit-transforms** when building custom calculation pipelines from low-level generic steps, and use **earthkit-climate** when you need standardized, domain-specific climate indicator functions.


Format handling
---------------

**earthkit-climate** indicators seamlessly handle native **earthkit-data** objects alongside **xarray** objects, performing automatic type inspection and format conversion behind the scenes.


Recommended workflow
--------------------

A typical climate indicator calculation follows a 4-step pipeline:

1. **Fetch and load**: Retrieve raw input data via :py:mod:`earthkit.data`.
2. **Preprocess / transform**: If working with percentiles or climatologies, apply :py:mod:`earthkit-transforms`.
3. **Compute indicator**: Pass the data directly to :py:mod:`earthkit.climate.indicators` (e.g. :py:func:`earthkit.climate.indicators.tx_days_above`). Format conversion is handled automatically.
4. **Visualize and export**: Plot the resulting index maps or time series using :py:mod:`earthkit.plots` or export the results.


.. seealso::

   * :doc:`../tutorials/quickstart_climate_indicators`
   * :doc:`../how-tos/station_data_indicators`
   * `earthkit-transforms Documentation <https://earthkit-transforms.readthedocs.io/en/latest/>`_
