.. SPDX-FileCopyrightText: 2025 European Centre for Medium-Range Weather Forecasts (ECMWF)
.. SPDX-License-Identifier: Apache-2.0

Development
===========

The code is hosted on GitHub: `ecmwf/earthkit-climate <https://github.com/ecmwf/earthkit-climate>`_.
Testing, bug reports and contributions are highly welcomed and appreciated. Feel free to fork and submit your PRs against the **develop** branch.


Dependencies
------------

Install development dependencies by with **extras** during installation of earthkit-climate::

   pip install -e .[dev]

Available extras:

- ``dev``: Development utilities. Includes ``docs``, ``docs-notebooks``, ``test`` and ``test-benchmark`` dependencies.
- ``docs``: Building the documentation.
- ``docs-notebooks``: Running the notebooks included with the documentation.
- ``test``: Running the unit tests.
- ``test-benchmark``: Running the performance benchmark (part of the integration tests). Includes ``test`` dependencies.


Quality Assurance
-----------------

Run the suite of **unit tests**::

   pytest

Run the suite of **integration tests**::

   pytest tests/integration -m integration

Run the **type checker**::

   MYPYPATH=src python -m mypy src tests/unit/

Run the **pre-commit** hooks::

   pre-commit run --all-files


Documentation
-------------

Build the documentation::

   sphinx-build -M html docs docs/_build
