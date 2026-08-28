.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_missing_values:

Missing values and calendar handling
====================================

This concept page describes how missing data, NaN values, incomplete time series, and leap years are handled in **earthkit-climate** indicator computations.


Handling missing data in indicators
-----------------------------------

When computing climate indicators over time periods (such as annual or monthly aggregations), input datasets derived from an **earthkit-data** :code:`FieldList` or NetCDF files often contain missing values due to sensor failures, masked ocean/land grid points, or incomplete records.

**earthkit-climate** delegates missing value handling to underlying **xclim** missing check mechanisms. By default, indicators check whether missing values in an aggregation interval exceed tolerable thresholds before returning a valid value.

Missing check strategies
~~~~~~~~~~~~~~~~~~~~~~~~

The missing data behavior can be controlled using the :code:`missing` keyword argument available on xclim-based indicators:

* **'any'** (default for many indices): If *any* NaN value occurs within an aggregation period (e.g. within a year), the output for that period is marked as :code:`NaN`.
* **'wmo'**: Follows World Meteorological Organization guidelines. A period is marked invalid if more than 3 consecutive days or more than 5 total days are missing in a month.
* **'at_least_n'**: Requires a minimum number of valid observations per period.
* **'pct'**: Requires a minimum percentage (e.g. 90%) of valid data points in the period.
* **'ignore'**: Ignores missing values and performs the reduction over available valid data.


Behavior with sparse or empty slices
------------------------------------

What happens when computing a daily climatology or annual index over a period with very few or zero valid data points?

1. **Zero valid values**: If an entire aggregation slice (e.g. a year or a day of year) contains only :code:`NaN` or zero observations, the indicator result for that slice evaluates to :code:`NaN`. No exception is raised, allowing batch grid processing to complete cleanly.
2. **Sparse observations**: Under the default missing strategy (:code:`'any'`), sparse observations within a period trigger a :code:`NaN` output for that period to prevent biased indicator estimates (e.g. underestimating total annual precipitation or hot days).
3. **Warnings**: When xclim missing checks invalidate a period, runtime warnings may be emitted if configured in python's warning filters, but the computation proceeds by setting invalid slices to :code:`NaN`.


Leap years and day-of-year alignment
------------------------------------

Handling leap years consistently is critical for daily climatologies and percentile thresholds across multi-year time series.

Day-of-year coordinates (`dayofyear`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In **earthkit-climate** (and standard CF/xarray conventions):

* Day of year coordinates run from **1 to 366**.
* **Day 60 is strictly reserved for February 29** in leap years.
* For non-leap years (365 days), day 59 corresponds to February 28, and day 61 corresponds to March 1. Day 60 is omitted in non-leap year data arrays.

When computing daily climatologies or rolling percentiles over mixed calendars (e.g. standard Gregorian containing both leap and non-leap years):

* **Day 60 (Feb 29)**: Only receives contributions from leap years in the input dataset. If a dataset contains no leap years, day 60 in a 366-day upsampled climatology will be filled or interpolated depending on upsampling settings (e.g. :py:func:`earthkit.climate.utils.climatology.upsample`).
* **Non-standard calendars**: For 360-day or `noleap` (365-day) calendars common in climate model outputs (CMIP), xarray and xclim preserve the native calendar without forcing a 366-day axis unless explicitly converted.


Best practices
--------------

* **Inspect input masks**: Ensure grid points over non-target domains (e.g. ocean points for land indices) are intentionally masked before calculation.
* **Select appropriate missing strategy**: For observational datasets with sporadic missing days, set :code:`indexer={'missing': 'pct', 'missing_options': {'pct': 0.9}}` to allow calculation when 90%+ data is present.
* **Harmonize calendars**: When comparing reanalysis (Gregorian) with climate models (`noleap`), align calendar types prior to percentile comparison.
