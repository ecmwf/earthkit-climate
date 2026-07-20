<!--
SPDX-FileCopyrightText: 2022 European Centre for Medium-Range Weather Forecasts (ECMWF)
SPDX-License-Identifier: Apache-2.0
-->

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

**earthkit-climate** is the package responsible for the climate index calculation within the earthkit ecosystem. It includes a wrapper prototype that allows the use of the [xclim](https://xclim.readthedocs.io/en/stable/) python package to compute a large amount of pre-defined climate indices used by the climate science community, and to define new ones.

## Quick Start

Install the package from PyPI:

```bash
pip install earthkit-climate
```

Example usage:

```python
from earthkit.climate.indicators import precipitation, temperature
from earthkit.climate.utils import conversions

# Example: compute a precipitation index
pr = precipitation.simple_daily_intensity(precip_data, freq="monthly")
```

## Documentation

For full documentation, including API reference and example notebooks, visit the
[earthkit-climate ReadTheDocs page](https://earthkit-climate.readthedocs.io)

## Development

See the [development guidelines](https://earthkit-climate.readthedocs.io/en/latest/development.html) in the documentation.

## Project Structure

```
earthkit-climate/
├── .github/
│   ├── workflows/             # GitHub Actions (push/release)
├── docs/                      # Sphinx-based documentation
├── src/earthkit/
│   ├── climate/
│   │   ├── indicators/        # Climate indicators
│   │   │   ├── xarray/        # xarray-based implementations
│   │   └── utils/             # Type conversions, percentiles, provenance
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
└── tools/                     # Scripts for code generation, etc.
```

## License

```
Copyright 2022-, European Centre for Medium Range Weather Forecasts.

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
