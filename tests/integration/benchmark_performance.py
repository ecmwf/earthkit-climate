import gc
import os
import sys
import threading
import time
import warnings
from typing import Any, Callable, Optional

import fire
import pandas as pd
import psutil
import xarray as xr
from tqdm import tqdm

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conftest import _run_indicator, get_indicator_configs

from earthkit.climate.datasets import load_sample_datasets

warnings.filterwarnings("ignore")


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
    n_repeats = int(n_repeats)
    print("Loading sample datasets via earthkit-data...")
    data_cache: dict[str, xr.Dataset] = load_sample_datasets()
    all_benchmarks: list[dict[str, Any]] = get_indicator_configs(data_cache)

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
        reference_time: float = group[(group["Library"] == "Xclim") & (group["Mode"] == "1. No Flox (Lazy)")][
            "mean_time"
        ].values[0]
        group["Speedup"] = reference_time / group["mean_time"]
        return group

    df = df.groupby("Indicator", group_keys=False).apply(calculate_speedup)

    print("\n" + "=" * 80)
    print(" PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 80)
    print(df.to_string(index=False, formatters={"mean_time": "{:.3f}s".format, "Speedup": "{:.2f}x".format}))
    print("=" * 80)


if __name__ == "__main__":
    fire.Fire(run_benchmarks)
