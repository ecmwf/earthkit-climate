.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_missing_values:

Missing values
==============

How **missing data** are handled in **earthkit-climate** indicator computations.


Handling missing data in indicators
-----------------------------------

When computing climate indicators over time periods (such as annual or monthly aggregations), input datasets can contain **missing data** (represented as **NaN** values) due to masked grid points, sensor outages, or unrecorded periods.

**earthkit-climate** indicators based on **xclim** functions delegate missing data checks to the underlying xclim mechanisms.
By default, indicators check whether missing data in an aggregation interval exceeds acceptable threshold limits before returning a calculated result or a :code:`NaN`.

Missing check strategies
~~~~~~~~~~~~~~~~~~~~~~~~

The missing data behavior is controlled using **xclim's options context** via :code:`xclim.set_options(check_missing=...)` and :code:`missing_options`:

.. code-block:: python

   import earthkit.climate as ekc
   import xclim as xc

   # Set WMO missing strategy using context manager
   with xc.set_options(check_missing="wmo"):
       hot_days = ekc.indicators.tx_days_above(tasmax, thresh="30 degC")

   # Customize parameters (e.g. max 10% missing data)
   with xc.set_options(
       check_missing="pct", missing_options={"pct": {"tolerance": 0.1}}
   ):
       hot_days = ekc.indicators.tx_days_above(tasmax, thresh="30 degC")

Available strategies for :code:`check_missing` (see the `xclim missing value documentation <https://xclim.readthedocs.io/en/stable/apidoc/xclim.core.html#module-xclim.core.missing>`_):

* **'any'** (default for many indices): If *any* NaN value occurs within an aggregation period, the output for that period evaluates to :code:`NaN`.
* **'wmo'**: Follows World Meteorological Organization guidelines. By default, a period is marked missing if 11 or more days are missing, or if 5 or more consecutive days are missing in a month.
* **'at_least_n'**: Requires a minimum number of valid observations per period (default :code:`n=20`).
* **'pct'**: Requires a minimum percentage of valid data points in the period (controlled by :code:`tolerance`).
* **'some_but_not_all'**: A result evaluates to :code:`NaN` if some, but not all, input values are missing.
* **'skip'**: Skips missing data checks and performs the calculation over available data points.


.. note::

   The missing data check behavior described above reflects the current implementation inherited from xclim.
   **Earthkit-climate** may provide its own mechanism for setting the missing value policy in the future.


Behavior with missing data slices
---------------------------------

What happens when computing a daily climatology or annual index over a period containing missing data?

1. **Empty periods**: If an entire aggregation slice contains only :code:`NaN` values, the indicator result for that slice evaluates to :code:`NaN`. No exception is raised, allowing grid processing to complete cleanly.
2. **Partial missing data**: Under the default missing strategy (:code:`'any'`), any missing data point within a period triggers a :code:`NaN` output for that period to prevent biased indicator estimates (e.g. underestimating total annual precipitation).
3. **Warnings**: When missing checks invalidate a period, runtime warnings may be emitted if configured in Python's warning filters, setting affected outputs to :code:`NaN`.


Best practices
--------------

* **Inspect input masks**: Ensure grid points over non-target domains (e.g. ocean points for land indices) are intentionally masked before calculation.
* **Select appropriate missing strategy**: For observational datasets with missing data points, use :code:`xc.set_options(check_missing="pct", missing_options={"pct": {"tolerance": 0.1}})` to allow calculation when 90%+ data is present.
