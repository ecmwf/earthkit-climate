.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_scalability_performance:

Scalability and performance
===========================

This page outlines the key principles for scaling **earthkit-climate** indicator calculations to larger-than-memory datasets using **Dask** and **xarray**.


Core principles of scalable execution
-------------------------------------

Computing climate indices over long time series (e.g. 50+ years of hourly or daily ERA5 reanalysis) or high-resolution spatial grids (e.g. CORDEX / CMIP6) requires parallel processing and memory-efficient out-of-core evaluation (processing data larger than available system RAM by streaming smaller chunks from disk).

To achieve this, **earthkit-climate** relies on **Dask**, a parallel computing library integrated with **xarray**. Dask addresses scalability and performance through three interconnected concepts:

* **Chunking**: Datasets are partitioned into smaller sub-arrays called *chunks* (e.g. rectangular blocks of spatial or temporal data). Instead of loading an entire dataset into memory at once, operations process one chunk at a time.
* **Lazy evaluation**: Indicator calculations do not compute results immediately; instead, they construct a lightweight *task graph* representing the required computational steps.
* **Parallel and out-of-core execution**: Tasks in the graph are executed independently and in parallel across CPU cores or cluster workers. Memory remains bounded because workers stream chunk by chunk, triggering actual execution only when explicitly requesting :code:`.compute()`, writing to disk, or plotting.

When working with datasets from **earthkit-data** (e.g. GRIB/NetCDF files loaded as a :code:`FieldList`), **earthkit-climate** indicators accept these objects directly—automatically converting them to xarray objects. For large-scale data, custom Dask chunking can also be explicitly specified prior to calculation (e.g. via :code:`data.to_xarray(chunks=...)` or :code:`ds.chunk(...)`):

.. code-block:: python

   import earthkit.climate as ekc
   import earthkit.data as ekd

   # Automatic format conversion
   data = ekd.from_source("file", "temperature.grib")
   hot_days = ekc.indicators.tx_days_above(data, thresh="30 degC")

   # Explicit Dask chunking for large-scale datasets
   ds_chunked = data.to_xarray(chunks={"time": -1, "latitude": 50, "longitude": 50})
   hot_days_lazy = ekc.indicators.tx_days_above(ds_chunked, thresh="30 degC")


Optimal chunking strategies
---------------------------

The structure of Dask chunks strongly influences performance, memory overhead, and computational speed.

Spatial vs. temporal chunking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Time-reduction indices** (e.g. annual maximum temperature, consecutive dry days, percentiles): These operations require full contiguous time series for each grid point.

  * **Recommended chunking**: Keep the time dimension **contiguous** (a single chunk along time, e.g., :code:`chunks={'time': -1, 'latitude': 50, 'longitude': 50}`).
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
   * Highly recommended for larger-than-memory rechunking operations on Dask Distributed clusters.
   * Reduces task graph size and prevents scheduler bottlenecks.

.. note::

   **Recommendation**:
   * For **local execution or small/medium datasets**: Default task-based rechunking (:code:`method='task'`) is fast and sufficient.
   * For **distributed or larger-than-memory workloads**: Explicitly specify peer-to-peer rechunking (e.g., :code:`ds.chunk(..., method='p2p')`) when using a Dask Distributed cluster to prevent task graph explosion and scheduler bottlenecks.


Worker memory management
------------------------

To ensure efficient memory usage and maintain performance during Dask calculations:

* **Avoid overly small chunks**: Chunks smaller than 10–50 MB lead to excessive task overhead. Target chunk sizes between **100 MB and 500 MB**.
* **Avoid overly large chunks**: Chunks exceeding worker memory limits cause spill-to-disk or out-of-memory (OOM) worker kills.
* **Trim unneeded variables**: Load only the specific variables required for the indicator (e.g. `tasmax`) before starting calculations.


Step-by-step hands-on guide
---------------------------

For concrete code examples demonstrating how to apply Dask chunking, initialize cluster clients, and calculate indicators on lazy arrays:

.. seealso::

   * :doc:`../tutorials/dask_large_datasets`
