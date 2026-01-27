Development
===========

The code is hosted on GitHub: `ecmwf/earthkit-climate <https://github.com/ecmwf/earthkit-climate>`_


Environment
-----------

This project uses `Pixi <https://pixi.sh>`_ for dependency and environment management.
It provides fast, reproducible environments and replaces Conda-based workflows.

Install Pixi following the `official instructions <https://pixi.sh/latest/#installation>`_, then run:

.. code-block:: bash

   pixi install

This command installs all dependencies as defined in ``pyproject.toml`` and ``pixi.lock``.

.. warning::

   We are not yet commited to maintaining a Pixi configuration long-term.


Task runners
------------

This project uses ``pixi`` tasks to manage development workflows, replacing the legacy ``Makefile``.

- **Quality Assurance**: Run pre-commit hooks to ensure code quality.

  .. code-block:: bash

     pixi run qa

- **Unit Tests**: Run the test suite using pytest.

  .. code-block:: bash

     pixi run unit-tests

- **Type Checking**: Run static type analysis with mypy.

  .. code-block:: bash

     pixi run type-check

- **Build Documentation**: Build the Sphinx documentation. Note that this task runs in the ``docs`` environment.

  .. code-block:: bash

     pixi run -e docs docs-build


- **Sync with ECMWF template**:

  .. code-block:: bash

     pixi run template-update
