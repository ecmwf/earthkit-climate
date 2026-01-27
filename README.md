<p align="center">
  <picture>
    <source srcset="https://github.com/ecmwf/logos/raw/refs/heads/main/logos/earthkit/earthkit-climate-dark.svg" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/ecmwf/logos/raw/refs/heads/main/logos/earthkit/earthkit-climate-light.svg" height="120">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/ecmwf/codex/raw/refs/heads/main/ESEE">
    <img src="https://github.com/ecmwf/codex/raw/refs/heads/main/ESEE/foundation_badge.svg" alt="ECMWF Software EnginE">
  </a>
  <a href="https://github.com/ecmwf/codex/raw/refs/heads/main/Project Maturity">
    <img src="https://github.com/ecmwf/codex/raw/refs/heads/main/Project Maturity/emerging_badge.svg" alt="Maturity Level">
  </a>
  <a href="https://opensource.org/licenses/apache-2-0">
    <img src="https://img.shields.io/badge/Licence-Apache 2.0-blue.svg" alt="Licence">
  </a>
  <a href="https://github.com/ecmwf/earthkit-climate/releases">
    <img src="https://img.shields.io/github/v/release/ecmwf/earthkit-climate?color=purple&label=Release" alt="Latest Release">
  </a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a>
  •
  <a href="https://earthkit-climate.readthedocs.io/en/latest/">Documentation</a>
</p>

> [!IMPORTANT]
> This software is **Emerging** and subject to ECMWF's guidelines on [Software Maturity](https://github.com/ecmwf/codex/raw/refs/heads/main/Project%20Maturity).

# earthkit-climate

**earthkit-climate** is the package responsible for the climate index calculation within the earthkit ecosystem. It includes a wrapper prototype that allows the use of the `xclim` python package to compute a large amount of pre-defined climate indices used by the climate science community, and to define new ones.

`xclim` relies heavily on the `xarray` python library and the `numpy` & `scipy` ecosystem. Its main elements are:

- **Climate indices**: available to be directly computed with python functions. The input and output units are defined in these functions by using a decorator and are validated during runtime.
- **Climate indicators**: climate indices wrapped in an object that provides more metadata and validation facilities (health checks) of the input. it includes attributes for CF metadata (cell methods), references, keywords, and more.
- **Lower level process functions**: these include aggregation, computation spell length and counting, optimized computation of reference percentiles, bias correction methods and ensemble statistics. These functions are used by the implemented indices and can also be used to build new indices not included in the library.

______________________________________________________________________

## Disclaimer

This project is currently in **BETA** and **experimental**.
Interfaces, structure, and functionality are subject to change without notice.
Do **not** use this software in any operational or production system.

______________________________________________________________________

## Quick Start

Install the package in editable mode:

```bash
pip install -e .
```

Example usage:

```python
from earthkit.climate.indicators import precipitation, temperature
from earthkit.climate.utils import conversions

# Example: compute a precipitation index
pr = precipitation.simple_daily_intensity(precip_data, freq="monthly")
```

______________________________________________________________________

## Documentation

For full documentation, including API reference and example notebooks, visit the
[earthkit-climate ReadTheDocs page](https://earthkit-climate.readthedocs.io)

______________________________________________________________________

## Development & Contribution Workflow

### 1. Setup environment (with Pixi)

This project uses [**Pixi**](https://pixi.sh) for dependency and environment management.
It provides fast, reproducible environments and replaces Conda-based workflows.

Install Pixi following the [official instructions](https://pixi.sh/latest/#installation), then run:

```bash
pixi install
```

This command installs all dependencies as defined in `pyproject.toml` and `pixi.lock`.

### 2. Common Tasks

This project uses `pixi` tasks to manage development workflows, replacing the legacy `Makefile`.

- **Quality Assurance**: Run pre-commit hooks to ensure code quality.

  ```bash
  pixi run qa
  ```

- **Unit Tests**: Run the test suite using pytest.

  ```bash
  ```

pixi run -e dev unit-tests

````

- **Type Checking**: Run static type analysis with mypy.

```bash
pixi run -e dev type-check
````

- **Build Documentation**: Build the Sphinx documentation. Note that this task runs in the `docs` environment.

  ```bash
  pixi run -e docs docs-build
  ```

- **Docker**: Build and run the docker container.

  ```bash
  pixi run docker-build
  pixi run docker-run
  ```

- **Sync with ECMWF template**:

  ```bash
  pixi run template-update
  ```

______________________________________________________________________

## Project Structure

```
earthkit-climate/
├── src/earthkit/
│   ├── climate/
│   │   ├── api/               # API wrapper logic
│   │   ├── indicators/        # Climate indices (precipitation, temperature, etc.)
│   │   └── utils/             # Type conversions, percentiles, provenance
│   └── __init__.py
├── tests/
│   ├── unit/                  # Unit tests for indicators and utils
│   └── test_00_version.py     # Version check
├── docs/                      # Sphinx documentation
├── ci/                        # Continuous integration configs
├── .github/workflows/         # GitHub Actions (push/release)
├── .pixi/                     # Pixi configuration
├── pixi.lock                  # Locked dependency versions
├── Dockerfile                 # Pixi-based container
├── pyproject.toml             # Project configuration
└── README.md
```

______________________________________________________________________

## License

```
Copyright 2022, European Centre for Medium Range Weather Forecasts.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation
nor does it submit to any jurisdiction.
```
