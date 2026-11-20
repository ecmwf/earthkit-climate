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
   Keeps Dask's default memory-management behaviour.

``low-memory``
   Starts spilling data earlier, pauses workers before memory is exhausted,
   and reduces scheduler worker saturation.

The configuration values can be inspected through
:data:`earthkit.climate.dask.PRESETS`.

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
