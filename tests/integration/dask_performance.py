# SPDX-FileCopyrightText: 2022 European Centre for Medium-Range Weather Forecasts (ECMWF)
# SPDX-License-Identifier: Apache-2.0

import gc
import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional, cast

import dask
import earthkit.data as ekd
import fire
import numpy as np
import pandas as pd
import psutil
import xarray as xr

import earthkit.climate as ekc

try:
    from distributed import Client, LocalCluster, Worker
except ImportError as exc:  # pragma: no cover - exercised by CLI use
    raise SystemExit("This benchmark requires dask distributed. Install the test-benchmark extra.") from exc

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conftest import _run_indicator


def run_indicator(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    use_flox: Optional[bool],
) -> Any:
    return _run_indicator(func, kwargs, use_flox=use_flox)


def without_time_chunks(chunks: Optional[dict[str, int]]) -> dict[str, int]:
    return {key: value for key, value in (chunks or {}).items() if key != "time"}


def chunk_with_time_resampler(obj: xr.Dataset, freq: str) -> xr.Dataset:
    from xarray.groupers import TimeResampler

    return obj.chunk({"time": TimeResampler(freq)})


_CLUSTER_PRESETS: dict[str, dict[str, Any]] = {
    "high-memory": {
        "worker_scale": 1.0,
    },
    "low-memory": {
        "worker_scale": 0.5,
        "threads_per_worker": 1,
    },
}

DEFAULT_READ_CHUNKS = {
    "time": 31,
    "lat": 120,
    "lon": 120,
}

TASMAX_SAMPLE_DATASET = "tasmax_ACCESS-CM2_ssp585_far_future"


class ResourceMonitor(threading.Thread):
    """Background memory monitor including child Dask worker processes."""

    def __init__(self, interval: float = 0.1) -> None:
        self.interval = interval
        self.stop_event = threading.Event()
        self.memory_usage: list[float] = []
        self.process = psutil.Process()
        super().__init__()

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                self.memory_usage.append(self.memory_usage_mib())
            except Exception:
                pass
            time.sleep(self.interval)

    def memory_usage_mib(self) -> float:
        rss = self.process.memory_info().rss
        for child in self.process.children(recursive=True):
            try:
                rss += child.memory_info().rss
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        return rss / (1024 * 1024)

    def stop(self) -> None:
        self.stop_event.set()


def cluster_options_for_preset(
    preset: str,
    n_workers: int,
    threads_per_worker: int,
    processes: bool,
    memory_limit: str,
    use_nanny: bool,
) -> dict[str, Any]:
    preset_cluster = _CLUSTER_PRESETS[preset]
    worker_scale = float(preset_cluster.get("worker_scale", 1.0))
    preset_threads = int(preset_cluster.get("threads_per_worker", threads_per_worker))

    options = {
        "n_workers": max(1, int(n_workers * worker_scale)),
        "threads_per_worker": preset_threads,
        "processes": processes,
        "memory_limit": memory_limit,
        "dashboard_address": None,
    }
    if not use_nanny:
        options["worker_class"] = Worker
    return options


def parse_presets(presets: Optional[str | list[str]]) -> list[str]:
    if presets is None:
        return list(ekc.dask.PRESETS)
    if isinstance(presets, str):
        return [p.strip() for p in presets.split(",") if p.strip()]
    return presets


def parse_indicators(indicators: Optional[str | list[str]]) -> Optional[list[str]]:
    if indicators is None:
        return None
    if isinstance(indicators, str):
        return [i.strip() for i in indicators.split(",") if i.strip()]
    return indicators


def parse_modes(modes: Optional[str | list[str]]) -> Optional[list[str]]:
    if modes is None:
        return None
    if isinstance(modes, str):
        return [m.strip() for m in modes.split(",") if m.strip()]
    return modes


def graph_task_count(obj: Any) -> int:
    graph_getter = getattr(obj, "__dask_graph__", None)
    if graph_getter is not None:
        graph = graph_getter()
        return len(graph) if graph is not None else 0

    data = getattr(obj, "data", None)
    graph_getter = getattr(data, "__dask_graph__", None)
    if graph_getter is not None:
        graph = graph_getter()
        return len(graph) if graph is not None else 0

    return 0


def format_chunks(obj: Any) -> str:
    chunks = getattr(obj, "chunks", None)
    if chunks is not None:
        return str(chunks)

    data = getattr(obj, "data", None)
    chunks = getattr(data, "chunks", None)
    return str(chunks) if chunks is not None else "not chunked"


def summarize_xarray_object(obj: Any) -> list[str]:
    if isinstance(obj, xr.Dataset):
        return [
            f"{name}: chunks={format_chunks(var)}, tasks={graph_task_count(var)}" for name, var in obj.data_vars.items()
        ]
    if isinstance(obj, xr.DataArray):
        name = obj.name or "<unnamed>"
        return [f"{name}: chunks={format_chunks(obj)}, tasks={graph_task_count(obj)}"]
    return [f"{type(obj).__name__}: chunks={format_chunks(obj)}, tasks={graph_task_count(obj)}"]


def print_graph_summary(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    use_flox: Optional[bool],
) -> tuple[int, str]:
    print("    inputs:")
    for arg_name, arg_value in kwargs.items():
        if isinstance(arg_value, (xr.Dataset, xr.DataArray)):
            for line in summarize_xarray_object(arg_value):
                print(f"      {arg_name}.{line}")

    res = run_indicator(
        func,
        kwargs,
        use_flox=use_flox,
    )
    summary_lines = summarize_xarray_object(res)
    print("    result:")
    for line in summary_lines:
        print(f"      {line}")

    total_tasks = graph_task_count(res)
    return total_tasks, "; ".join(summary_lines)


def result_to_dataset(result: Any) -> xr.Dataset:
    if isinstance(result, xr.Dataset):
        return result
    if isinstance(result, xr.DataArray):
        name = result.name or "result"
        return result.to_dataset(name=name)
    if hasattr(result, "to_xarray"):
        converted = result.to_xarray()
        if isinstance(converted, xr.Dataset):
            return converted
        if isinstance(converted, xr.DataArray):
            name = converted.name or "result"
            return converted.to_dataset(name=name)
    raise TypeError(f"Cannot convert result of type {type(result).__name__} to an xarray Dataset")


def safe_filename(value: str) -> str:
    return (
        value
        .replace(" ", "_")
        .replace("/", "_")
        .replace("+", "plus")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
    )


def open_sample_tasmax(chunks: dict[str, Any]) -> xr.Dataset:
    ds = ekd.from_source("earthkit-climate-sample", TASMAX_SAMPLE_DATASET).to_xarray()
    ds = ds[["tasmax"]].rename({"tasmax": "tas"})
    return ds.chunk(chunks) if chunks else ds


def load_sample_tasmax_data(chunks: Optional[dict[str, int]]) -> dict[str, xr.Dataset]:
    ds = open_sample_tasmax(chunks or {})

    return {
        TASMAX_SAMPLE_DATASET: ds,
        f"{TASMAX_SAMPLE_DATASET}_time_resampler": chunk_with_time_resampler(
            open_sample_tasmax(without_time_chunks(chunks)),
            "YS",
        ),
    }


def get_dask_indicator_configs(
    data_cache: dict[str, xr.Dataset],
) -> list[dict[str, Any]]:
    tas = data_cache[TASMAX_SAMPLE_DATASET]["tas"]
    tas_time_resampler = data_cache[f"{TASMAX_SAMPLE_DATASET}_time_resampler"]["tas"]
    return [
        {
            "name": "DDED",
            "ek_func": ekc.indicators.degree_days_exceedance_date,
            "ek_args": {
                "lazy": {"ds": tas.to_dataset(name="tas"), "freq": "YS"},
                "time_resampler": {"ds": tas_time_resampler.to_dataset(name="tas"), "freq": "YS"},
            },
        },
    ]


def parse_chunks(chunks: Optional[str]) -> Optional[dict[str, int]]:
    if not chunks:
        return None

    parsed: dict[str, int] = {}
    for item in chunks.split(","):
        dim, value = item.split("=", maxsplit=1)
        parsed[dim.strip()] = int(value.strip())
    return parsed


def read_chunks_or_default(chunks: Optional[dict[str, int]]) -> dict[str, int]:
    return chunks or DEFAULT_READ_CHUNKS


def benchmark_indicator(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    use_flox: Optional[bool],
    n_repeats: int,
    sink: str,
    output_dir: Path,
    output_prefix: str,
    netcdf_engine: Optional[str],
) -> dict[str, float]:
    times: list[float] = []
    memory_peaks: list[float] = []

    for repeat in range(n_repeats):
        gc.collect()
        monitor = ResourceMonitor(interval=0.1)
        baseline = monitor.memory_usage_mib()
        monitor.start()

        start = time.perf_counter()
        res = run_indicator(
            func,
            kwargs,
            use_flox=use_flox,
        )
        if sink == "compute":
            if hasattr(res, "compute"):
                res.compute()
            elif hasattr(res, "to_xarray"):
                res.to_xarray().compute()
        elif sink == "netcdf":
            output_path = output_dir / f"{output_prefix}_repeat-{repeat + 1}.nc"
            dataset = result_to_dataset(res)
            to_netcdf_kwargs = {"compute": False}
            if netcdf_engine:
                to_netcdf_kwargs["engine"] = netcdf_engine
            write_task = dataset.to_netcdf(output_path, **to_netcdf_kwargs)
            dask.compute(write_task)
        else:
            raise ValueError("sink must be 'compute' or 'netcdf'")
        duration = time.perf_counter() - start

        monitor.stop()
        monitor.join()

        observed = monitor.memory_usage
        peak = max(max(observed) - baseline, 0.0) if observed else 0.0
        times.append(duration)
        memory_peaks.append(peak)
        print(f"      repeat {repeat + 1}: {duration:.3f}s | peak delta {peak:.1f} MiB")

    return {
        "mean_time": float(np.mean(times)),
        "median_time": float(np.median(times)),
        "max_mem": float(np.max(memory_peaks)),
        "mean_mem": float(np.mean(memory_peaks)),
    }


def indicator_runtime_configs(
    benchmark: dict[str, Any],
    modes: Optional[list[str]],
) -> list[dict[str, Any]]:
    configs = [
        {
            "Library": "Earthkit",
            "Mode": "1. No Flox (Standard)",
            "func": benchmark["ek_func"],
            "kwargs": benchmark["ek_args"]["lazy"],
            "use_flox": False,
        },
        {
            "Library": "Earthkit",
            "Mode": "2. Flox (Standard)",
            "func": benchmark["ek_func"],
            "kwargs": benchmark["ek_args"]["lazy"],
            "use_flox": True,
        },
    ]
    if "time_resampler" in benchmark["ek_args"]:
        configs.append(
            {
                "Library": "Earthkit",
                "Mode": "2b. Flox + TimeResampler",
                "func": benchmark["ek_func"],
                "kwargs": benchmark["ek_args"]["time_resampler"],
                "use_flox": True,
            },
        )
    if modes is not None:
        configs = [cfg for cfg in configs if cfg["Mode"] in modes]
    return configs


def run_benchmark(
    indicators: Optional[str | list[str]] = None,
    presets: Optional[str | list[str]] = None,
    chunks: Optional[str] = None,
    modes: Optional[str | list[str]] = None,
    n_workers: int = 4,
    threads_per_worker: int = 1,
    processes: bool = True,
    use_nanny: bool = False,
    memory_limit: str = "0",
    sink: str = "netcdf",
    netcdf_engine: Optional[str] = None,
    n_repeats: int = 3,
) -> None:
    """
    Run climate indicator benchmarks under Dask distributed scheduler presets.

    Examples
    --------
    python tests/integration/dask_performance.py --presets=high-memory,low-memory
    python tests/integration/dask_performance.py --chunks=time=75,lat=150,lon=300
    """
    selected_presets = parse_presets(presets)
    selected_indicators = parse_indicators(indicators)
    selected_modes = parse_modes(modes)
    read_chunks = read_chunks_or_default(parse_chunks(chunks))

    if sink not in {"compute", "netcdf"}:
        raise ValueError("sink must be 'compute' or 'netcdf'")

    validated_presets: list[ekc.dask.PresetName] = []
    for preset_name in selected_presets:
        if preset_name not in ekc.dask.PRESETS:
            available = ", ".join(sorted(ekc.dask.PRESETS))
            raise ValueError(f"Unknown Dask preset {preset_name!r}. Available presets: {available}")
        validated_presets.append(cast(ekc.dask.PresetName, preset_name))

    print("\nDASK INDICATOR PERFORMANCE BENCHMARK")
    print("=" * 80)
    print(f"data: earthkit-climate-sample/{TASMAX_SAMPLE_DATASET}")
    print(f"read chunks: {read_chunks}")
    print(f"modes: {', '.join(selected_modes) if selected_modes else 'all'}")
    print(
        f"base cluster: n_workers={n_workers}, threads_per_worker={threads_per_worker}, "
        f"processes={processes}, use_nanny={use_nanny}, memory_limit={memory_limit}"
    )
    print(f"sink: {sink}")
    print(f"netcdf_engine: {netcdf_engine or 'xarray default'}")
    print(f"presets: {', '.join(validated_presets)}")

    data_cache = load_sample_tasmax_data(read_chunks)

    print("\nDatasets")
    print("-" * 80)
    for key, ds in data_cache.items():
        print(f"{key}: size={ds.nbytes / (1024 * 1024):.1f} MiB dims={dict(ds.dims)}")

    benchmarks = get_dask_indicator_configs(data_cache)
    if selected_indicators:
        benchmarks = [b for b in benchmarks if b["name"] in selected_indicators]

    results: list[dict[str, Any]] = []
    for preset in validated_presets:
        print(f"\nPreset: {preset}")
        print("-" * 80)
        cluster_options = cluster_options_for_preset(
            preset,
            n_workers=n_workers,
            threads_per_worker=threads_per_worker,
            processes=processes,
            memory_limit=memory_limit,
            use_nanny=use_nanny,
        )
        with tempfile.TemporaryDirectory(prefix=f"earthkit-climate-dask-{preset}-") as tmpdir:
            output_dir = Path(tmpdir)
            print(f"temporary output directory: {output_dir}")
            with (
                ekc.dask.preset(preset) as config,
                LocalCluster(**cluster_options) as cluster,
                Client(cluster) as client,
            ):
                print(f"scheduler: {cluster.scheduler_address}")
                print(f"cluster options: {cluster_options}")
                print(f"workers: {len(client.scheduler_info()['workers'])}")
                print(f"config: {config if config else 'default'}")

                for benchmark in benchmarks:
                    for cfg in indicator_runtime_configs(benchmark, selected_modes):
                        label = f"{benchmark['name']} / {cfg['Library']} / {cfg['Mode']}"
                        print(f"\n  {label}")
                        tasks, graph_summary = print_graph_summary(
                            cfg["func"],
                            cfg["kwargs"],
                            cfg["use_flox"],
                        )
                        output_prefix = safe_filename(f"{preset}_{benchmark['name']}_{cfg['Library']}_{cfg['Mode']}")
                        stats = benchmark_indicator(
                            cfg["func"],
                            cfg["kwargs"],
                            cfg["use_flox"],
                            n_repeats=n_repeats,
                            sink=sink,
                            output_dir=output_dir,
                            output_prefix=output_prefix,
                            netcdf_engine=netcdf_engine,
                        )
                        results.append({
                            "Preset": preset,
                            "Indicator": benchmark["name"],
                            "Library": cfg["Library"],
                            "Mode": cfg["Mode"],
                            "Sink": sink,
                            "Tasks": tasks,
                            "Graph": graph_summary,
                            **stats,
                        })

    df = pd.DataFrame(results)
    print("\nSummary")
    print("=" * 80)
    print(
        df.drop(columns=["Graph"]).to_string(
            index=False,
            formatters={
                "mean_time": "{:.3f}s".format,
                "median_time": "{:.3f}s".format,
                "max_mem": "{:.1f} MiB".format,
                "mean_mem": "{:.1f} MiB".format,
            },
        )
    )


if __name__ == "__main__":
    fire.Fire(run_benchmark)
