# SPDX-FileCopyrightText: 2022 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import earthkit.climate as climate


def test_version() -> None:
    assert climate.__version__ != "999"


def test_py_typed_marker_present() -> None:
    assert Path(climate.__file__).with_name("py.typed").is_file()
