.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_scalability_performance:

Scalability and performance
===========================

This page outlines the key principles for scaling **earthkit-climate** indicator calculations to multi-gigabyte or multi-terabyte datasets using **Dask** and **xarray**.


Core principles of scalable execution
-------------------------------------

Computing climate indices over long time series (e.g. 50+ years of hourly or daily ERA5 reanalysis) or high-resolution spatial grids (e.g. CORDEX / CMIP6) requires parallel processing and memory-efficient out-of-core evaluation.

When loading large datasets using **earthkit-data** (e.g. from GRIB/NetCDF files via a :code:`FieldList`), calling :code:`.to_xarray(chunks=...)` loads the data lazily backed by Dask arrays:

1. **Lazy operations**: Index calculations construct a task graph without loading entire datasets into RAM.
2. **Chunking**: Data is split into smaller rectangular blocks (chunks) processed independently or in parallel across Dask workers.
3. **Delayed compute**: Execution is triggered only when explicitly requesting :code:`.compute()`, saving to Zarr/NetCDF, or generating plots.


Optimal chunking strategies
---------------------------

The structure of Dask chunks strongly influences performance, memory overhead, and computational speed.

Spatial vs. temporal chunking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Time-reduction indices** (e.g. annual maximum temperature, consecutive dry days, percentiles): These operations require full unchunked time series for each grid point.
  
  * **Recommended chunking**: Keep the time dimension **unchunked** (or chunked by full years/decades, e.g., :code:`chunks={'time': -1, 'latitude': 50, 'longitude': 50}`).
  * **Why?**: Resampling across time boundary chunks forces Dask to perform expensive cross-worker shuffling.

* **Annual / Groupby resampling**: When performing annual grouping operations (e.g. with :py:class:`xarray.groupers.TimeResampler("YS")`), chunking along spatial axes (:code:`latitude`, :code:`longitude`) while maintaining contiguous time chunks avoids graph bloating.


Rechunking methods: task vs. p2p
--------------------------------

When transitioning from disk layout (which is often time-slice chunked, e.g. 1 day per chunk across space) to indicator calculation layout (full time series per spatial block), data must be **rechunked**.

Dask offers two primary rechunking engines:

1. **Task-based rechunking (`method='task'`)**:
   
   * Standard Dask task graph construction.
   * Efficient for small to medium datasets.
   * Can lead to massive task graph overhead (million+ tasks) on large datasets.

2. **Peer-to-peer rechunking (`method='p2p'`)**:
   
   * Distributed shuffle engine using direct worker-to-worker memory transfer.
   * Highly recommended for large multi-GB or TB rechunking operations on Dask Distributed clusters.
   * Reduces task graph size and prevents scheduler bottlenecks.


Worker memory management
------------------------

During complex indicator calculations (such as rolling percentile thresholds across 30-year baselines):

* **Avoid overly small chunks**: Chunks smaller than 10–50 MB lead to excessive task overhead. Target chunk sizes between **100 MB and 500 MB**.
* **Avoid overly large chunks**: Chunks exceeding worker memory limits cause spill-to-disk or out-of-memory (OOM) worker kills.
* **Trim unneeded variables**: Load only the specific variables required for the indicator (e.g. `tasmax`) before starting calculations.


Step-by-step hands-on guide
---------------------------

For concrete code examples demonstrating how to apply Dask chunking, initialize cluster clients, and calculate indicators on lazy arrays:

.. seealso::

   * :doc:`../tutorials/dask_large_datasets`
