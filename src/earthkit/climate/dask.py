# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

"""Dask configuration presets for climate workloads."""

import os
from contextlib import contextmanager
from typing import Any, Iterator, Literal, TypeAlias

import dask

PresetName: TypeAlias = Literal["high-memory", "low-memory"]
"""Names accepted by :func:`preset`."""

PRESETS: dict[PresetName, dict[str, Any]] = {
    "high-memory": {
        "distributed.admin.tick.limit": "30s",
    },
    "low-memory": {
        "distributed.scheduler.worker-saturation": 0.7,
        "distributed.worker.memory.target": 0.50,
        "distributed.worker.memory.spill": 0.60,
        "distributed.worker.memory.pause": 0.80,
        "distributed.admin.tick.limit": "30s",
    },
}
"""Named Dask configuration presets provided by earthkit-climate."""


@contextmanager
def preset(name: PresetName) -> Iterator[dict[str, Any]]:
    """Temporarily apply a named Dask configuration preset.

    The configuration is applied both to the current process and through
    environment variables inherited by workers created inside the context.
    Previous configuration and environment values are restored on exit.

    Parameters
    ----------
    name : PresetName
        Name of a preset in :data:`PRESETS`.

    Yields
    ------
    dict[str, Any]
        The Dask configuration values applied by the preset.

    Raises
    ------
    ValueError
        If *name* is not an available preset.
    """
    try:
        config = PRESETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PRESETS))
        raise ValueError(f"Unknown Dask preset {name!r}. Available presets: {available}") from exc

    env_config = {
        f"DASK_{key.replace('.', '__').replace('-', '_').upper()}": str(value) for key, value in config.items()
    }
    previous_env = {key: os.environ.get(key) for key in env_config}

    try:
        os.environ.update(env_config)
        with dask.config.set(config):
            yield config
    finally:
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


__all__ = ["PRESETS", "PresetName", "preset"]
