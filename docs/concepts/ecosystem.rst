.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_ecosystem:

Software ecosystem and positioning
==================================

This page describes where **earthkit-climate** fits within the wider climate data software ecosystem, its relationship to other **earthkit** packages, and how it compares to established climate indicator libraries such as **xclim** and **Climpact**.


What earthkit-climate provides
------------------------------

**earthkit-climate** is designed as ECMWF's primary Python package for computing climate indicators, climate indices, and climate change analysis/attribution workflows. It provides:

* **High-level, domain-aware APIs**: Clean entry points organized by atmospheric, land, ocean, and sea-ice submodules (:py:mod:`earthkit.climate.indicators`).
* **ECMWF and C3S data pipeline integration**: Built to work natively with data structures output by Copernicus Climate Change Service (C3S), ERA5 reanalysis, CMIP6, and CORDEX datasets.
* **Automatic format handling via @format_handler**: Accepts **earthkit-data** :code:`Field` and :code:`FieldList` objects directly without requiring manual :code:`.to_xarray()` conversions.
* **Standardized CF metadata preservation**: Ensures that computed climate indices retain complete CF-convention attributes, physical units, and cell methods.
* **Robust defaults and extensibility**: Simplifies common indicator configurations while permitting full custom parameter tuning.


Role in the earthkit ecosystem
------------------------------

The **earthkit** framework is a modular suite of open-source Python components developed by ECMWF:

.. code-block:: text

   [ earthkit-data ] ----> [ earthkit-transforms ] ----> [ earthkit-climate ] ----> [ earthkit-plots ]
   (FieldList Ingestion)   (Climatology/Baselines)       (Climate Indicators)        (Visualization)

1. **earthkit-data**: Ingests data from CDS, MARS, local GRIB/NetCDF/Zarr files as :code:`Field` and :code:`FieldList` objects.
2. **earthkit-transforms**: Handles general spatial/temporal transformations, baseline period slicing, and percentile/climatology computations.
3. **earthkit-climate**: Computes climate indicator metrics (e.g. heatwave duration, heavy precipitation, drought indices). Thanks to `@format_handler`, indicators accept `FieldList` objects natively.
4. **earthkit-plots**: Produces publication-ready maps, charts, and geospatial figures.


Comparison with xclim and Climpact
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Package
     - Primary focus
     - Relationship to earthkit-climate
   * - **xclim**
     - Low-level library providing 100+ climate index definitions, unit conversions, and calendar checks based on xarray and Pint.
     - **earthkit-climate uses xclim as its core underlying backend engine.** earthkit-climate wraps xclim indicators with `@format_handler` to provide seamless integration with ECMWF data models and earthkit workflows.
   * - **Climpact**
     - R/GUI-focused software for calculating ET-SCI climate extreme indices, primarily designed for weather station series.
     - **earthkit-climate** provides Python-native, gridded, parallelized implementations of standard ET-SCI indices (and more) suitable for large spatial datasets.


When to choose earthkit-climate
-------------------------------

You should choose **earthkit-climate** when:

* You are building Python workflows that ingest ECMWF, CDS, or C3S climate datasets via **earthkit-data** :code:`Field` or :code:`FieldList` inputs.
* You want transparent format handling without needing manual data array conversions before calling indicator functions.
* You need end-to-end integration across data retrieval (`earthkit-data`), transformations (`earthkit-transforms`), and plotting (`earthkit-plots`).
* You want high-level climate index calculations with minimal setup overhead while maintaining access to advanced Dask scalability and xclim backend customization.
