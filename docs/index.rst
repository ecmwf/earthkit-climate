earthkit-climate
================

.. important::

   This software is **Emerging** and subject to ECMWF's guidelines on `Software Maturity <https://github.com/ecmwf/codex/raw/refs/heads/main/Project%20Maturity>`_.


.. admonition:: Help us improve!
   :class: important survey

   Share your experience and needs (3-5 minutes survey)

   .. raw:: html

      <a href="https://ec.europa.eu/eusurvey/runner/user_feedback_integration" class="survey-button">Start Survey</a>


**earthkit-climate** is the package responsible for climate index calculations within the earthkit ecosystem. It includes a wrapper prototype that allows the use of the `xclim <https://xclim.readthedocs.io/en/stable/>`_ Python package to compute a large amount of pre-defined climate indices used by the climate science community, and to define new ones.



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
