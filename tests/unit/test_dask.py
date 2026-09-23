# SPDX-FileCopyrightText: 2026 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import os

import dask
import pytest

import earthkit.climate as ekc


def test_presets_are_available_from_public_module() -> None:
    assert ekc.dask.PRESETS == {
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


def test_preset_applies_and_restores_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    config_key = "distributed.worker.memory.target"
    env_key = "DASK_DISTRIBUTED__WORKER__MEMORY__TARGET"
    missing = object()
    previous_config = dask.config.get(config_key, default=missing)
    monkeypatch.delenv(env_key, raising=False)

    with ekc.dask.preset("low-memory") as config:
        assert config is ekc.dask.PRESETS["low-memory"]
        assert dask.config.get(config_key) == 0.50
        assert os.environ[env_key] == "0.5"

    restored_config = dask.config.get(config_key, default=missing)
    if previous_config is missing:
        assert restored_config is missing
    else:
        assert restored_config == previous_config
    assert env_key not in os.environ


def test_preset_restores_existing_environment_value(monkeypatch: pytest.MonkeyPatch) -> None:
    env_key = "DASK_DISTRIBUTED__ADMIN__TICK__LIMIT"
    monkeypatch.setenv(env_key, "5s")

    with ekc.dask.preset("high-memory"):
        assert os.environ[env_key] == "30s"

    assert os.environ[env_key] == "5s"


def test_unknown_preset_lists_available_names() -> None:
    with pytest.raises(ValueError, match="Available presets: high-memory, low-memory"):
        # Deliberately bypass the static Literal constraint to test runtime validation.
        with ekc.dask.preset("unknown"):  # type: ignore[arg-type]
            pass
