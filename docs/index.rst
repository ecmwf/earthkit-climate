Welcome to the eaRthkIt-climate documentation!
======================================================

.. warning::

    This project is **BETA** and will be **Experimental** for the foreseeable future. Interfaces and functionality are likely to change, and the project itself may be scrapped. **DO NOT** use this software in any project/software that is operational.

.. warning::

    This documentation is still work in progress and can only be regarded as a **DRAFT**.


**earthkit-climate** is a library of software tools to support people working with climate and meteorology data


**earthkit-climate** includes methods for aggregating data in time and space, and future versions will include
tools for bias correcting, downscaling climate data and standard caculations for climate metrics 
(e.g. indicators and risk factors).
It has been design following the philosphy of Earthkit, hence the methods should be interoperable with any
data object understood by earthkit-data.

.. code-block:: python

    data = earthkit.data.from_source("file", "my-data.nc")
    processed_data = earthkit.climate.method(data)


.. toctree::
   :maxdepth: 1
   :caption: Examples
   :titlesonly:

   examples

.. toctree::
   :maxdepth: 1
   :caption: Installation

   install


Indices and tables
==================

* :ref:`genindex`

.. * :ref:`modindex`
.. * :ref:`search`
