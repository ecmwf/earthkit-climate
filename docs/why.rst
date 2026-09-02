.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

Why earthkit-climate?
=====================

**earthkit-climate** is the primary ECMWF Python package responsible for climate indicator calculations and climate change analysis workflows within the **earthkit** ecosystem.


What earthkit-climate provides
------------------------------

* **High-level, domain-aware APIs**: Clean entry points organized by atmospheric, land, ocean, and sea-ice submodules (:py:mod:`earthkit.climate.indicators`).
* **Support for both gridded and in-situ data**: Seamlessly handles 2D/3D gridded datasets (ERA5 reanalysis, CMIP6, CORDEX) as well as 1D point/station in-situ observations.
* **ECMWF and C3S data pipeline integration**: Built to work natively with data structures output by Copernicus Climate Change Service (C3S) and ECMWF data services.
* **Automatic format handling via @format_handler**: Accepts **earthkit-data** :code:`Field` and :code:`FieldList` objects directly without requiring manual :code:`.to_xarray()` conversions.
* **Standardized CF metadata preservation**: Ensures that computed climate indices retain complete CF-convention attributes, physical units, and cell methods.
* **Scalable parallel execution**: Leverages Dask and xarray for memory-efficient out-of-core calculations across large multi-gigabyte spatial grids.


Role in the earthkit ecosystem
------------------------------

The **earthkit** framework is a modular suite of open-source Python components developed by ECMWF:

.. code-block:: text

   [ earthkit-data ] ----> [ earthkit-transforms ] ----> [ earthkit-climate ] ----> [ earthkit-plots ]
   (FieldList Ingestion)   (Climatology/Baselines)       (Climate Indicators)        (Visualization)

1. **earthkit-data**: Ingests data from CDS, MARS, local GRIB/NetCDF/Zarr files as :code:`FieldList` objects.
2. **earthkit-transforms**: Handles general spatial/temporal transformations, baseline period slicing, and climatology computations.
3. **earthkit-climate**: Computes climate indicator metrics (e.g. heatwave duration, heavy precipitation, drought indices). Thanks to :code:`@format_handler`, indicators accept :code:`FieldList` objects natively.
4. **earthkit-plots**: Produces publication-ready maps, charts, and geospatial figures.


Relationship to xclim
---------------------

Rather than replacing existing climate index engines, **earthkit-climate leverages `xclim <https://xclim.readthedocs.io/en/stable/>`_ as its underlying calculation engine.**

* **xclim** provides 100+ robust, unit-aware climate indicator algorithms and calendar check utilities based on xarray and Pint.
* **earthkit-climate** wraps xclim indicators with :code:`@format_handler` and ECMWF data model mappings, providing seamless compatibility with ECMWF/C3S data structures, GRIB files, and earthkit workflows without requiring users to write manual conversion boilerplate.
