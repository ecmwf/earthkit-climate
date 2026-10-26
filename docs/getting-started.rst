.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

Installation and Getting Started
================================

Installing from PyPI
--------------------

earthkit-climate is available on PyPI.

.. code-block:: bash

   pip install earthkit-climate


Import and use
--------------

Compute a precipitation indicator from xclim:

.. code-block:: python

   import earthkit.climate as ekc
   sdii = ekc.indicators.daily_pr_intensity(precip_data)
