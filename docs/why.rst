.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

Why earthkit-climate?
=====================

**earthkit-climate** is a Python package providing climate indicator calculations and climate change analysis workflows within the **earthkit** `ecosystem <https://earthkit.ecmwf.int/>`_.


Main features
-------------

* **High-level, domain-aware API** to climate indicator computations.
* **Scalable parallel execution** with dask and xarray to ensure efficient processing of large datasets.
* **Support for gridded fields and time series** from ERA5, CMIP6, CORDEX, and point/station observations.
* Works natively with data formats returned by the Climate Data Store (CDS) and ECMWF data services.
* Computed climate indicators retain complete CF-convention attributes, physical units, and cell methods.


Earthkit ecosystem integration
------------------------------

**earthkit-climate** integrates with other earthkit packages for the creation of climate data processing pipelines:

1. **earthkit-data** to ingest data from CDS, MARS, local files and many other sources.
2. **earthkit-transforms**: for spatial/temporal transformations and computation of baseline climatologies.
3. **earthkit-climate** to compute climate indicators (e.g. heatwave duration, heavy precipitation, drought indices).
4. **earthkit-plots** to produce publication-ready visualisations.


Scientific Python ecosystem integration
---------------------------------------

**earthkit-climate** will delegate computations to established packages where possible instead of reimplementing existing functionality from scratch:

* `xclim <https://xclim.readthedocs.io/en/stable/>`_ :cite:p:`bourgault2023xclim` provides 100+ robust, unit-aware climate indicator definitions and utilities.
