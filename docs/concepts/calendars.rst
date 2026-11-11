.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_calendars:

Calendar handling
=================

How leap years are handled in **earthkit-climate** indicator computations.


Leap years and day-of-year alignment
------------------------------------

Handling leap years consistently is critical for daily climatologies and percentile thresholds across multi-year time series.

In **earthkit-climate** (following standard xarray and pandas datetime conventions on the :code:`time` dimension):

* For non-leap years (365 days), :code:`dayofyear` ranges from **1 to 365** (where Day 59 is Feb 28 and Day 60 is Mar 1).
* For leap years (366 days), :code:`dayofyear` ranges from **1 to 366** (where Day 59 is Feb 28, Day 60 is Feb 29, and Day 61 is Mar 1).
* **Day 366** occurs only in leap years (December 31 of leap years).

When computing daily climatologies or rolling percentiles over time series containing both leap and non-leap years:

* **Rolling percentile calculation** (:py:func:`earthkit.climate.utils.climatology.rolling_percentiles`): **earthkit-climate** handles day-of-year alignment over leap years by applying rolling time windows (e.g. 5-day window centered on each day) and interpolating percentile thresholds to guarantee continuous daily coverage.
* **Non-standard calendars**: For 360-day or `noleap` (365-day) calendars common in climate model outputs (CMIP), xarray and xclim preserve the native calendar without forcing a 366-day axis unless explicitly converted.


Best practices
--------------

* **Harmonize calendars**: When comparing reanalysis (Gregorian) with climate models (`noleap`), align calendar types prior to percentile comparison.
