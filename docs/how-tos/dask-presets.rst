.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

Configure Dask for climate workloads
====================================

``earthkit-climate`` uses xarray to handle array-based data. Although optional, xarray is commonly
used together with Dask, a library that enables computations to be distributed and datasets larger
than available memory to be processed. This is a common use case in climate science,
particularly as spatial resolution increases and datasets grow larger. However, the default dask
configuration very often increases the memory pressure excessively until the process is killed by the
Out Of Memory daemon.

To support processing large datasets with limited resources, earthkit-climate provides
Dask a low-memory configuration preset, and also a high-memory preset for the opposite case.
These presets require the Dask Distributed backend, which provides more configuration options than
the default scheduler. To run a Dask Distributed cluster, install the optional dependency:

.. code-block:: bash

   pip install "earthkit-climate[distributed]"

Available presets
-----------------

``high-memory``
   Keeps Dask's default memory-management behaviour and sets the administrative
   tick limit to 30 seconds.

``low-memory``
   Starts spilling data earlier, pauses workers before memory is exhausted,
   and reduces scheduler worker saturation.

Both presets are defined in :data:`earthkit.climate.dask.PRESETS`:

.. literalinclude:: ../../src/earthkit/climate/dask.py
   :language: python
   :start-at: PRESETS:
   :end-before: """Named Dask configuration presets

Size the cluster
----------------

The presets configure Dask's scheduler and worker memory-management behaviour,
but they do not size the cluster. The number of workers, the number of threads
per worker, and the per-worker memory limit also affect task concurrency and
peak memory pressure. For memory-constrained workloads, start with fewer
workers and one thread per worker, then adjust these values to the available
resources and workload.

Apply a preset
--------------

Enter the preset context before creating the cluster so that worker processes
inherit its environment variables:

.. code-block:: python

   import earthkit.climate as ekc
   from distributed import Client, LocalCluster

   with ekc.dask.preset("low-memory"):
       with LocalCluster(
           n_workers=2,
           threads_per_worker=1,
           memory_limit="4 GiB",
       ) as cluster, Client(cluster) as client:
           sdii = ekc.indicators.daily_pr_intensity(
               precip_data.chunk({"time": 31})
           ).compute()

The context applies the preset to the current Dask configuration and restores
both the configuration and environment variables when it exits.

Understanding what is going on
------------------------------
Dask is not simple, and understanding how dask is processing your data and the bottlenecks it may be hitting can be difficult. Here we provide a more detailed explanation of what are the challenges when setting up dask and what these presets are doing.

Dask divides a workflow into several smaller tasks which form a dependency graph. T and A task can run once its inputs are available, and the scheduler generally favors advancing work already underway. These tasks are sent to the workers, which have several threads and processes available for running them. Workers retain completed results as long as a downstream task or client still needs them. Root-task queuing limits how much new work gets dispatched at the entrance to the graph, this is precisely what is controlled by the scheduler worker saturation parameter. There are two common places for a bottleneck to form.

* Inside the graph. A rechunk or reduction may need several upstream chunks before it can produce one downstream chunk. Some inputs can finish quickly and sit on workers while the slowest input is still being read, transferred, or computed. A rechunk that changes both time and spatial boundaries can create many such dependencies at once.

* At the output. Workers may finish indicator chunks faster than the destination can encode, compress, and write them. A serialized writer, a shared-filesystem bottleneck, or slow object-store requests can all reduce the rate at which completed chunks are released. If computation produces 400 MiB/s and the write stage consumes 200 MiB/s, the unwritten backlog grows by roughly 200 MiB/s while those rates persist, measured in the same units. Adding workers can make the backlog grow faster if write throughput stays flat.

At the output. Workers may finish indicator chunks faster than the destination can encode, compress, and write them. A serialized writer, a shared-filesystem bottleneck, or slow object-store requests can all reduce the rate at which completed chunks are released. If computation produces 400 MiB/s and the write stage consumes 200 MiB/s, the unwritten backlog grows by roughly 200 MiB/s while those rates persist, measured in the same units. Adding workers can make the backlog grow faster if write throughput stays flat.

Important I/O considerations
----------------------------

The dask tasks typically include the I/O, this is, the read and write actions from the disk or the network. As the climate data is often stored in chunks (netCDF, zarr) or messages (GRIB2), the number of reads and writes can be very large, making the graph size grow a lot. They also include compression, which increases the CPU load. The shape of the chunks of data in the I/O can dramatically influence the time it takes to compute a workflow, even with a lot of computational resources available.

Even if input storage chunks and Dask chunks serve different purposes. The storage format determines what must be fetched and decoded. The Dask chunk determines how much array data a task handles at once. For chunked NetCDF4/HDF5 or Zarr, it usually makes sense to align Dask chunk boundaries with storage chunk boundaries and, where useful, group several whole storage chunks into one Dask chunk. If two Dask tasks each touch part of the same compressed storage chunk, both may have to fetch and decode it. Grouping whole storage chunks reduces Dask task overhead and avoids splitting a storage chunk across tasks. The number of storage requests still depends on how those chunks are laid out physically. It is also important to consider than, even if the I/O bandwith is large, often the reads and writes suffer from latency (when they go through a network). This is often the case in HPC clusters or S3 object storages. Concurrency can mitigate this latency, but dependent requests, a serialized writer, or a cap on outstanding requests can put them directly on the critical path. For example it is well known that netCDF/HDF5 libraries do not support concurrent writes. Thus, we encourage using Zarr whenever possible, especially if the volume of data is large.

References
----------

https://distributed.dask.org/en/stable/scheduling-state.html
