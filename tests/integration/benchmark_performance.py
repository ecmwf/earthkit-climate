# (C) Copyright 2025 - ECMWF and individual contributors.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

"""
Performance analysis script for climate indicators.

This script migrates the benchmarking and profiling logic from
docs/notebooks/performance_analysis.ipynb. It allows for repeatable
performance measurements of Earthkit-Climate indicators compared to Xclim.

Features:
- Timing statistics (mean, median, std).
- Memory profiling (peak Induced RAM usage using psutil).
- Comparative analysis between Earthkit (Lazy/Optimized) and Xclim.
- CLI interface to run specific indicators and configuration.

Run with:
    export PYTHONPATH="."
    pixi run -e dev python tests/integration/benchmark_performance.py --help
"""

import argparse
import gc
import os
import threading
import time
import warnings
from contextlib import nullcontext
from typing import Any, Callable, Optional

import earthkit.data
import pandas as pd
import psutil
import xarray as xr
from tqdm import tqdm

import earthkit.climate.indicators.precipitation as ek_pr
import earthkit.climate.indicators.temperature as ek_temp
from earthkit.climate.utils.percentile import percentile_doy

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Constants & Dataset URLs
# ---------------------------------------------------------------------------

_URLS: dict[str, str] = {
    "tasmax_hist": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmax_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_historical.nc"
    ),
    "tasmax_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmax_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
    "tasmin_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "tasmin_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
    "pr_ssp": (
        "https://sites.ecmwf.int/repository/earthkit-climate/"
        "pr_gridded_day_CMIP6_ACCESS-CM2_r1i1p1f1_deepESD_day_ssp585.nc"
    ),
}

# ---------------------------------------------------------------------------
# Resource Monitor
# ---------------------------------------------------------------------------


class ResourceMonitor(threading.Thread):
    """
    Background thread to monitor system resource usage during execution.

    ## Parameters

    interval : float, default 0.1
        Sampling interval in seconds.
    """

    def __init__(self, interval: float = 0.1) -> None:
        self.interval: float = interval
        self.stop_event: threading.Event = threading.Event()
        self.memory_usage: list[float] = []
        self.process: psutil.Process = psutil.Process()
        super().__init__()

    def run(self) -> None:
        """
        Periodically record resident set size (RSS) memory in MiB.

        ## Returns

        None
        """
        while not self.stop_event.is_set():
            try:
                # RSS Memory in MiB
                mem: float = self.process.memory_info().rss / (1024 * 1024)
                self.memory_usage.append(mem)
            except Exception:
                pass
            time.sleep(self.interval)

    def stop(self) -> None:
        """
        Signal the monitor to stop sampling.

        ## Returns

        None
        """
        self.stop_event.set()


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------


def load_datasets() -> dict[str, xr.Dataset]:
    """
    Download or use cached CMIP6 datasets required for benchmarking.

    Uses earthkit-data's URL source with a user-level cache.

    ## Returns

    dict[str, xr.Dataset]
        Mapping from short name to xarray Dataset.
    """
    cache_dir: str = os.path.expanduser("~/.cache/earthkit/data")
    os.makedirs(cache_dir, exist_ok=True)
    earthkit.data.config.set(
        {
            "cache-policy": "user",
            "temporary-directory-root": cache_dir,
        }
    )

    datasets: dict[str, xr.Dataset] = {}
    print(f"Loading {len(_URLS)} datasets via earthkit-data...")
    for key, url in _URLS.items():
        ds = earthkit.data.from_source("url", url).to_xarray()
        datasets[key] = ds
    return datasets


# ---------------------------------------------------------------------------
# Benchmark Engine
# ---------------------------------------------------------------------------


def benchmark_function(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    n_repeats: int = 5,
    warmup: bool = True,
    label: str = "Function",
) -> dict[str, float]:
    """
    Execute a function multiple times and profile time and memory usage.

    ## Parameters

    func : Callable
        The function to benchmark.
    kwargs : dict[str, Any]
        Arguments to pass to func.
    n_repeats : int, default 5
        Number of measurement runs.
    warmup : bool, default True
        Perform a silent initial run to avoid JIT/caching bias.
    label : str, default "Function"
        Human-readable label for logging.

    ## Returns

    dict[str, float]
        Statistics including 'mean_time', 'median_time', 'std_time', 'max_mem'.
    """
    # 1. Warm-up
    if warmup:
        try:
            res: Any = func(**kwargs)
            if hasattr(res, "compute"):
                res.compute()
        except Exception as e:
            print(f"  Warm-up failed for {label}: {e}")
        gc.collect()

    times: list[float] = []
    mem_peaks: list[float] = []

    for _ in range(n_repeats):
        gc.collect()
        monitor: ResourceMonitor = ResourceMonitor(interval=0.1)
        baseline_mem: float = psutil.Process().memory_info().rss / (1024 * 1024)
        monitor.start()

        start_time: float = time.perf_counter()
        try:
            res = func(**kwargs)
            if hasattr(res, "compute"):
                res.compute()
        except Exception as e:
            print(f"  Execution failed for {label}: {e}")
            monitor.stop()
            continue
        end_time: float = time.perf_counter()

        monitor.stop()
        monitor.join()

        duration: float = end_time - start_time
        observed_mems: list[float] = monitor.memory_usage
        peak_delta: float = 0.0
        if observed_mems:
            peak_delta = max(max(observed_mems) - baseline_mem, 0.0)

        times.append(duration)
        mem_peaks.append(peak_delta)

    if not times:
        return {"mean_time": 0.0, "median_time": 0.0, "std_time": 0.0, "max_mem": 0.0}

    import numpy as np

    return {
        "mean_time": float(np.mean(times)),
        "median_time": float(np.median(times)),
        "std_time": float(np.std(times)),
        "max_mem": float(np.max(mem_peaks)),
    }


def _run_indicator(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    use_flox: Optional[bool] = None,
) -> Any:
    """
    Wrapper to set xarray options while running an indicator.

    ## Parameters

    func : Callable
        Target function.
    kwargs : dict[str, Any]
        Arguments.
    use_flox : bool or None
        Sets xarray's use_flox option.

    ## Returns

    Any
        Result of the indicator call.
    """
    ctx = xr.set_options(use_flox=use_flox) if use_flox is not None else nullcontext()
    with ctx:
        return func(**kwargs)


# ---------------------------------------------------------------------------
# Define Benchmarks
# ---------------------------------------------------------------------------


def get_benchmarks(
    data_cache: dict[str, xr.Dataset],
) -> list[dict[str, Any]]:
    """
    Construct the list of benchmarks as defined in the performance analysis notebook.

    ## Parameters

    data_cache : dict[str, xr.Dataset]
        Dictionary of loaded datasets.

    ## Returns

    list[dict[str, Any]]
        List of benchmark configurations.
    """
    import xclim.indicators

    tasmax_ssp = data_cache["tasmax_ssp"]["tasmax"]
    tasmin_ssp = data_cache["tasmin_ssp"]["tasmin"]
    pr_ssp = data_cache["pr_ssp"]["pr"]

    # Pre-calculate percentile for WSDI
    per_90: xr.DataArray = percentile_doy(data_cache["tasmax_hist"]["tasmax"], per=90)
    per_90.name = "tasmax_per"

    # Optimized views (Chunk -1)
    tasmax_opt = tasmax_ssp.chunk({"time": -1})
    tasmin_opt = tasmin_ssp.chunk({"time": -1})
    pr_opt = pr_ssp.chunk({"time": -1})

    benchmarks: list[dict[str, Any]] = [
        {
            "name": "WSDI",
            "ek_func": ek_temp.warm_spell_duration_index,
            "xi_func": xclim.indicators.atmos.warm_spell_duration_index,
            "ek_args": {
                "lazy": {"ds": xr.merge([tasmax_ssp, per_90]), "freq": "MS"},
                "optimized": {
                    "ds": xr.merge([tasmax_opt, per_90]).chunk({"time": -1}),
                    "freq": "MS",
                },
            },
            "xi_args": {
                "lazy": {"tasmax": tasmax_ssp, "tasmax_per": per_90, "freq": "MS"},
                "optimized": {
                    "tasmax": tasmax_opt,
                    "tasmax_per": per_90,
                    "freq": "MS",
                },
            },
        },
        {
            "name": "CWD",
            "ek_func": ek_pr.maximum_consecutive_wet_days,
            "xi_func": xclim.indicators.atmos.maximum_consecutive_wet_days,
            "ek_args": {
                "lazy": {"ds": pr_ssp, "freq": "MS"},
                "optimized": {"ds": pr_opt, "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"pr": pr_ssp, "freq": "MS"},
                "optimized": {"pr": pr_opt, "freq": "MS"},
            },
        },
        {
            "name": "DTR",
            "ek_func": ek_temp.daily_temperature_range,
            "xi_func": xclim.indicators.atmos.daily_temperature_range,
            "ek_args": {
                "lazy": {"ds": xr.merge([tasmax_ssp, tasmin_ssp]), "freq": "MS"},
                "optimized": {"ds": xr.merge([tasmax_opt, tasmin_opt]), "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"tasmax": tasmax_ssp, "tasmin": tasmin_ssp, "freq": "MS"},
                "optimized": {"tasmax": tasmax_opt, "tasmin": tasmin_opt, "freq": "MS"},
            },
        },
        {
            "name": "HDD",
            "ek_func": ek_temp.heating_degree_days,
            "xi_func": xclim.indicators.atmos.heating_degree_days,
            "ek_args": {
                "lazy": {"ds": ((tasmax_ssp + tasmin_ssp) / 2).to_dataset(name="tas"), "freq": "MS"},
                "optimized": {
                    "ds": ((tasmax_opt + tasmin_opt) / 2).to_dataset(name="tas"),
                    "freq": "MS",
                },
            },
            "xi_args": {
                "lazy": {"tas": (tasmax_ssp + tasmin_ssp) / 2, "freq": "MS"},
                "optimized": {"tas": (tasmax_opt + tasmin_opt) / 2, "freq": "MS"},
            },
        },
        {
            "name": "SDII",
            "ek_func": ek_pr.daily_pr_intensity,
            "xi_func": xclim.indicators.atmos.daily_pr_intensity,
            "ek_args": {
                "lazy": {"ds": pr_ssp, "freq": "MS"},
                "optimized": {"ds": pr_opt, "freq": "MS"},
            },
            "xi_args": {
                "lazy": {"pr": pr_ssp, "freq": "MS"},
                "optimized": {"pr": pr_opt, "freq": "MS"},
            },
        },
    ]
    return benchmarks


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------


def run_benchmarks(
    indicators: Optional[list[str]] = None,
    n_repeats: int = 5,
) -> None:
    """
    Execute the performance analysis loop.

    ## Parameters

    indicators : list[str] or None
        Subset of indicators to run (e.g. ['WSDI', 'CWD']).
        If None, all 5 are run.
    n_repeats : int, default 5
        Number of repeats per configuration.

    ## Returns

    None
    """
    data_cache: dict[str, xr.Dataset] = load_datasets()
    all_benchmarks: list[dict[str, Any]] = get_benchmarks(data_cache)

    if indicators:
        benchmarks: list[dict[str, Any]] = [b for b in all_benchmarks if b["name"] in indicators]
    else:
        benchmarks = all_benchmarks

    results: list[dict[str, Any]] = []

    for b in tqdm(benchmarks, desc="Indicators"):
        name: str = b["name"]

        # Define configurations
        configs: list[dict[str, Any]] = [
            {
                "lib": "Earthkit",
                "mode": "1. No Flox (Lazy)",
                "func": b["ek_func"],
                "args": b["ek_args"]["lazy"],
                "use_flox": False,
            },
            {
                "lib": "Earthkit",
                "mode": "2. Flox (Lazy)",
                "func": b["ek_func"],
                "args": b["ek_args"]["lazy"],
                "use_flox": True,
            },
            {
                "lib": "Earthkit",
                "mode": "3. Flox + Opt",
                "func": b["ek_func"],
                "args": b["ek_args"]["optimized"],
                "use_flox": True,
            },
            {
                "lib": "Xclim",
                "mode": "1. No Flox (Lazy)",
                "func": b["xi_func"],
                "args": b["xi_args"]["lazy"],
                "use_flox": False,
            },
            {
                "lib": "Xclim",
                "mode": "2. Flox (Lazy)",
                "func": b["xi_func"],
                "args": b["xi_args"]["lazy"],
                "use_flox": True,
            },
            {
                "lib": "Xclim",
                "mode": "3. Flox + Opt",
                "func": b["xi_func"],
                "args": b["xi_args"]["optimized"],
                "use_flox": True,
            },
        ]

        for cfg in configs:
            label: str = f"{name} / {cfg['lib']} / {cfg['mode']}"
            stats: dict[str, float] = benchmark_function(
                _run_indicator,
                {"func": cfg["func"], "kwargs": cfg["args"], "use_flox": cfg["use_flox"]},
                n_repeats=n_repeats,
                label=label,
            )
            res: dict[str, Any] = {
                "Indicator": name,
                "Library": cfg["lib"],
                "Mode": cfg["mode"],
                **stats,
            }
            results.append(res)

    # Summarize with Pandas
    df: pd.DataFrame = pd.DataFrame(results)

    # Add speedup relative to Xclim No Flox for each indicator
    def calculate_speedup(group: pd.DataFrame) -> pd.DataFrame:
        reference_time: float = group[
            (group["Library"] == "Xclim") & (group["Mode"] == "1. No Flox (Lazy)")
        ]["mean_time"].values[0]
        group["Speedup"] = reference_time / group["mean_time"]
        return group

    df = df.groupby("Indicator", group_keys=False).apply(calculate_speedup)

    print("\n" + "=" * 80)
    print(" PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 80)
    print(df.to_string(index=False, formatters={"mean_time": "{:.3f}s".format, "Speedup": "{:.2f}x".format}))
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Earthkit-Climate indicator performance analysis")
    parser.add_argument(
        "--indicators",
        nargs="+",
        help="Sub-list of indicators to run (WSDI CWD DTR HDD SDII)",
    )
    parser.add_argument(
        "-n",
        "--n-repeats",
        type=int,
        default=5,
        help="Number of iterations per test",
    )

    args = parser.parse_args()
    run_benchmarks(indicators=args.indicators, n_repeats=args.n_repeats)
