.. SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

.. _concept_format_handling:

Format handling with @format_handler
====================================

In **earthkit-data**, retrieved data is represented as **Field** (a single 2D spatial slice) and **FieldList** (a sequence or collection of 2D fields) objects.

Users do **not** need to manually convert `Field` or `FieldList` objects to xarray DataArrays before calling **earthkit-climate** indicators. All indicator functions in **earthkit-climate** are decorated with `@format_handler` from `earthkit.utils.decorators`.

The `@format_handler` decorator automatically inspects and converts input types behind the scenes:

* **Direct Field / FieldList inputs**: You can pass an `earthkit-data` `FieldList` directly into any indicator function.
* **Seamless xarray and NumPy support**: Accepts `xarray.DataArray`, `xarray.Dataset`, or `FieldList` interchangeably.
* **Output format preservation**: Returns appropriately formatted outputs with complete CF metadata.

Example passing an earthkit `FieldList` directly to an indicator:

.. code-block:: python

   import earthkit.data as ekd
   import earthkit.climate as ekc

   # Retrieve temperature fields as an earthkit FieldList
   fields = ekd.from_source("cds", "reanalysis-era5-single-levels", ...)  # returns FieldList

   # Compute climate indicator directly on the FieldList (no manual .to_xarray() required!)
   hot_days = ekc.indicators.tx_days_above(fields, thresh="300 K")
