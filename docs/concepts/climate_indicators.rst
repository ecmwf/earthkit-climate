.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_climate_indicators:

Climate indicators in earthkit
==============================

This page explains what **earthkit-climate** understands as a climate indicator and outlines where to start when calculating climate indicators within the broader **earthkit** ecosystem.


What is a climate indicator?
----------------------------

In climate science, raw meteorological variables (such as 2-metre temperature, precipitation, or surface wind speed) describe instantaneous or high-frequency atmospheric states. A **climate indicator** (or climate index) transforms these raw variables into meaningful metrics that characterize climate variability, extremes, and long-term trends.

Examples of climate indicators include:

* **Threshold counts**: Number of hot days (:code:`tx_days_above`), frost days (:code:`frost_days`), or tropical nights (:code:`tropical_nights`).
* **Cumulative metrics**: Growing degree days (:code:`growing_degree_days`), heating/cooling degree days.
* **Percentile-based indices**: Warm days (:code:`tx90p`), wet days (:code:`r95p`), relative to a historical baseline period.
* **Complex multi-variable indices**: Heatwave magnitude index, drought indicators (SPI, SPEI), or wildfire danger metrics.

In **earthkit-climate**, indicators are standardized functions that take :py:class:`xarray.DataArray`, :py:class:`xarray.Dataset`, or **earthkit-data** objects and return indicator DataArrays with enriched CF-compliant metadata (e.g., standard names, cell methods, and updated units).


Where to start in the earthkit ecosystem
----------------------------------------

The **earthkit** suite of libraries provides a modular end-to-end pipeline for climate data processing. Each package handles a specific stage of the workflow:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Package
     - Role in climate indicator workflows
   * - **earthkit-data**
     - Data retrieval and ingestion from CDS, MARS, URL, or local GRIB/NetCDF files as `Field` or `FieldList` objects.
   * - **earthkit-transforms**
     - General spatial and temporal operations, including baseline climatology calculations and percentile estimation.
   * - **earthkit-climate**
     - Domain-specific climate indicators (temperature, precipitation, land, ocean, sea ice) and attribution utilities, wrapping `xclim <https://xclim.readthedocs.io/>`_ with sensible defaults and automatic format handling.
   * - **earthkit-plots**
     - Production-ready visualization of indicator maps, time series, and spatial figures.


Native format handling with @format_handler
-------------------------------------------

In **earthkit-data**, retrieved data is represented as **Field** (a single 2D spatial slice) and **FieldList** (a sequence or collection of 2D fields) objects.

Users do **not** need to manually convert `Field` or `FieldList` objects to xarray DataArrays before calling **earthkit-climate** indicators. All indicator functions in **earthkit-climate** are decorated with `@format_handler` from `earthkit.utils.decorators`.

The `@format_handler` decorator automatically inspects and converts input types behind the scenes:

* **Direct Field / FieldList inputs**: You can pass an `earthkit-data` `FieldList` directly into any indicator function.
* **Seamless xarray and NumPy support**: Accepts `xarray.DataArray`, `xarray.Dataset`, or `FieldList` interchangeably.
* **Output format preservation**: Returns appropriately formatted outputs with complete CF metadata.

Example passing an earthkit `FieldList` directly to an indicator:

.. code-block:: python

   import earthkit.data as ekd
   import earthkit.climate as ekc

   # Retrieve temperature fields as an earthkit FieldList
   fields = ekd.from_source("cds", "reanalysis-era5-single-levels", ...)  # returns FieldList

   # Compute climate indicator directly on the FieldList (no manual .to_xarray() required!)
   hot_days = ekc.indicators.tx_days_above(fields, thresh="300 K")


Recommended workflow
--------------------

A typical climate indicator calculation follows a 4-step pipeline:

1. **Fetch and load**: Retrieve raw input fields via :py:mod:`earthkit.data` as a :code:`FieldList` or :code:`Field`.
2. **Compute indicator**: Pass the :code:`FieldList` directly to :py:mod:`earthkit.climate.indicators` (e.g. :py:func:`earthkit.climate.indicators.tx_days_above`). The `@format_handler` decorator handles conversion automatically.
3. **Preprocess / transform**: If working with percentiles or climatologies, apply :py:mod:`earthkit-transforms`.
4. **Visualize and export**: Plot the resulting index maps or time series using :py:mod:`earthkit.plots` or export to NetCDF/Zarr.

.. seealso::

   * :doc:`../tutorials/quickstart_climate_indicators`
   * `earthkit-transforms Climatology Concept <https://earthkit-transforms.readthedocs.io/en/latest/concepts/climatology.html>`_
