# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOK_PATHS = [
    "docs/how-tos/intro_precipitation_indices.ipynb",
    "docs/how-tos/intro_temperature_indices.ipynb",
    # "docs/tutorials/frost_days_pyrenees.ipynb",  # data from CDS
    # "docs/tutorials/era5_decadal_warming.ipynb",  # data from CDS
    "docs/tutorials/tropical_nights_cooling_demand.ipynb",
    "docs/tutorials/heatwave_evolution.ipynb",
]


@pytest.mark.parametrize("path", NOTEBOOK_PATHS)
def test_notebook_run_to_completion(path, tmpdir):
    with open(path, "r") as f:
        notebook = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=300)
    ep.preprocess(notebook, {"metadata": {"path": tmpdir}})
