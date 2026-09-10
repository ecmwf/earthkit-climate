.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_earthkit_ecosystem:

The earthkit ecosystem
======================

The `**earthkit suite** of libraries <https://earthkit.ecmwf.int/>`_ provides a modular end-to-end pipeline for climate data processing. Each package handles a specific stage of the workflow:

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
