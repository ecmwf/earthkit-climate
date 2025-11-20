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

For full documentation, including API reference and example notebooks, visit the
[earthkit-climate ReadTheDocs page](https://earthkit-climate.readthedocs.io)

## Development & Contribution Workflow

### 1. Setup environment (with Pixi)

This project uses [**Pixi**](https://pixi.sh) for dependency and environment management.
It provides fast, reproducible environments and replaces Conda-based workflows.

Install Pixi following the [official instructions](https://pixi.sh/latest/#installation), then run:

```bash
pixi install --locked
pixi shell
```

This command installs all dependencies as defined in `pyproject.toml` and `pixi.lock`.

### 2. Install the package

Inside the Pixi environment:

```bash
pip install -e .
```

### 3. Quality checks and tests

Before pushing to GitHub, run:

```bash
make qa
make unit-tests
```

You can also perform type checking and integration tests:

```bash
make type-check
make integration-tests
```

### 4. Documentation

To build the documentation locally (using Sphinx):

```bash
make docs-build
```

### 5. Optional: Sync with ECMWF template

```bash
make template-update
```

## Project Structure

```
earthkit-climate/
├── src/earthkit/
│   ├── climate/
│   │   ├── indicators/        # Climate indices (precipitation, temperature, etc.)
│   │   └── utils/             # Type conversions, percentiles, provenance
│   └── __init__.py
├── tests/
│   ├── integration/           # Integration tests
│   └── unit/                  # Unit tests for indicators and utils
├── docs/                      # Sphinx documentation
├── ci/                        # Continuous integration configs
├── .github/workflows/         # GitHub Actions (push/release)
├── .pixi/                     # Pixi configuration
├── pixi.lock                  # Locked dependency versions
├── Dockerfile                 # Pixi-based container
├── pyproject.toml             # Project configuration
├── Makefile                   # Developer utilities (Pixi integrated)
└── README.md
```

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
