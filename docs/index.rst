earthkit-climate
================

.. important::

   This software is **Emerging** and subject to ECMWF's guidelines on `Software Maturity <https://github.com/ecmwf/codex/raw/refs/heads/main/Project%20Maturity>`_.


**earthkit-climate** is the package responsible for climate index calculations within the earthkit ecosystem. It includes a wrapper prototype that allows the use of the `xclim <https://xclim.readthedocs.io/en/stable/>`_ Python package to compute a large amount of pre-defined climate indices used by the climate science community, and to define new ones.

``xclim`` relies heavily on the ``xarray`` python library and the ``numpy`` & ``scipy`` ecosystem. Its main elements are:

- **Climate indices**: available to be directly computed with python functions. The input and output units are defined in these functions by using a decorator and are validated during runtime.
- **Climate indicators**: climate indices wrapped in an object that provides more metadata and validation facilities (health checks) of the input. it includes attributes for CF metadata (cell methods), references, keywords, and more.
- **Lower level process functions**: these include aggregation, computation spell length and counting, optimized computation of reference percentiles, bias correction methods and ensemble statistics. These functions are used by the implemented indices and can also be used to build new indices not included in the library.


Quickstart
==========

Install the package from PyPI:


.. code-block:: bash

   pip install earthkit-climate


Compute a precipitation indicator from xclim:

.. code-block:: python

   from earthkit.climate.indicators import precipitation
   pr = precipitation.simple_daily_intensity(precip_data, freq="monthly")



.. toctree::
   :caption: Examples
   :maxdepth: 1

   tutorials
   gallery


.. toctree::
   :caption: Documentation
   :maxdepth: 1

   user-guide
   API Reference <_api/index>


.. toctree::
   :caption: Package
   :maxdepth: 1

   installation
   development
   release-notes/index
   license


.. toctree::
   :caption: Projects
   :maxdepth: 1

   earthkit <https://earthkit.readthedocs.io/en/latest/>
