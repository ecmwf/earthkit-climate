import gc
import os
import sys
import threading
import time
import warnings
from typing import Any, Callable, Optional

import fire
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
import seaborn as sns
import xarray as xr
from tqdm import tqdm

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conftest import _run_indicator, get_indicator_configs

from earthkit.climate.datasets import load_sample_datasets

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Hardware & Resource Detection
# ---------------------------------------------------------------------------


def get_cpu_info() -> str:
    """
    Extract the CPU model name from the system resources.

    Returns
    -------
    str
        The name of the CPU model.
    """
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
    except Exception:
        return "Unknown CPU"
    return "Unknown CPU"


def get_ram_info() -> str:
    """
    Extract the total system RAM from /proc/meminfo.

    Returns
    -------
    str
        A formatted string representing total RAM in GB.
    """
    try:
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        total_kb = int(line.split()[1])
                        return f"{total_kb / 1024 / 1024:.1f} GB"
    except Exception:
        return "Unknown RAM"
    return "Unknown RAM"


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
        tqdm.write(f"  [Warm-up] Initializing {label}...")
        try:
            res: Any = func(**kwargs)
            if hasattr(res, "compute"):
                res.compute()
            elif hasattr(res, "to_xarray"):
                res.to_xarray().compute()
        except Exception as e:
            tqdm.write(f"  [Warm-up] FAILED for {label}: {e}")
        gc.collect()

    times: list[float] = []
    mem_peaks: list[float] = []

    tqdm.write(f"  [Execution] Running {n_repeats} repeats for {label}...")
    for i in range(n_repeats):
        gc.collect()
        monitor: ResourceMonitor = ResourceMonitor(interval=0.1)
        baseline_mem: float = psutil.Process().memory_info().rss / (1024 * 1024)
        monitor.start()

        start_time: float = time.perf_counter()
        try:
            res = func(**kwargs)
            if hasattr(res, "compute"):
                res.compute()
            elif hasattr(res, "to_xarray"):
                res.to_xarray().compute()
        except Exception as e:
            tqdm.write(f"    - Repeat {i + 1}/{n_repeats}: FAILED: {e}")
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
        tqdm.write(f"    - Repeat {i + 1}/{n_repeats}: {duration:.4f}s | Peak Mem Delta: {peak_delta:.2f} MiB")

    return {
        "mean_time": float(np.mean(times)),
        "median_time": float(np.median(times)),
        "std_time": float(np.std(times)),
        "max_mem": float(np.max(mem_peaks)),
        "mean_mem": float(np.mean(mem_peaks)),
    }


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------


def plot_results(df: pd.DataFrame, output_dir: str = "tests/integration/benchmark_results") -> None:
    """
    Generate and save benchmark performance plots using Seaborn.

    Parameters
    ----------
    df : pd.DataFrame
        Benchmark results.
    output_dir : str, default "tests/integration/benchmark_results"
        Directory to save the plots.

    Returns
    -------
    None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare data for plotting
    plot_df = df.copy()
    plot_df["Configuration"] = plot_df["Library"] + ": " + plot_df["Mode"]

    # Use a consistent color palette matching the documentation/notebooks
    palette = {
        "Earthkit: 1. No Flox (Standard)": "#A2C4E4",
        "Earthkit: 2. Flox (Standard)": "#3B719F",
        "Earthkit: 3. Flox + Opt (Manual)": "#9ECB8A",
        "Xclim: 1. No Flox (Standard)": "#4B8F4B",
        "Xclim: 2. Flox (Standard)": "#ECA4A6",
        "Xclim: 3. Flox + Opt (Manual)": "#C9302C",
    }

    sns.set_theme(style="whitegrid")

    # --- Figure 1: Speedup ---
    plt.figure(figsize=(12, 7))
    ax1 = sns.barplot(
        data=plot_df,
        x="Indicator",
        y="Speedup",
        hue="Configuration",
        palette=palette,
    )
    ax1.axhline(1.0, ls="--", color="gray", alpha=0.7)

    plt.title(
        "Figure 1: Relative Speedup (via Median Time)\n(Baseline: Xclim: 1. No Flox (Standard))",
        fontsize=14,
        pad=15,
    )
    plt.ylabel("Speedup", fontsize=12)
    plt.xlabel("Indicator", fontsize=12)
    plt.legend(title="Configuration")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "benchmark_speedup.png"), dpi=300)
    plt.close()

    # --- Figure 2: Peak Memory ---
    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=plot_df,
        x="Indicator",
        y="max_mem",
        hue="Configuration",
        palette=palette,
    )

    plt.title("Figure 2: Peak Memory Usage (MiB)\n(Lower is better)", fontsize=14, pad=15)
    plt.ylabel("max_mem (MiB)", fontsize=12)
    plt.xlabel("Indicator", fontsize=12)
    plt.legend(title="Configuration")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "benchmark_memory.png"), dpi=300)
    plt.close()

    print(f"\n[Plotting] Benchmark plots saved to: {output_dir}")


def run_benchmarks(
    indicators: Optional[list[str]] = None,
    n_repeats: int = 5,
    plot: bool = True,
) -> None:
    """
    Execute the performance analysis loop.

    ## Parameters

    indicators : list[str] or None
        Subset of indicators to run (e.g. ['WSDI', 'CWD']).
        If None, all 5 are run.
    n_repeats : int, default 5
        Number of repeats per configuration.
    plot : bool, default True
        Whether to generate performance plots.

    ## Returns

    None
    """
    n_repeats = int(n_repeats)
    print("\n" + "=" * 80)
    print(" STARTING CLIMATE INDICATOR PERFORMANCE BENCHMARK")
    print("=" * 80)
    print(f" - Physics: {get_cpu_info()} | {get_ram_info()}")
    print(f" - Runtime: Python {sys.version.split()[0]}")
    print("-" * 80)

    print("\n[1/3] Loading and Inspecting Sample Datasets...")
    data_cache: dict[str, xr.Dataset] = load_sample_datasets()

    print(f"\n{'Dataset Identifier':<40} | {'Size':<10} | {'Dimensions'}")
    print("-" * 80)
    for key, ds in data_cache.items():
        mem: str = f"{ds.nbytes / (1024 * 1024):.1f} MiB"
        dims: str = str(dict(ds.dims))
        print(f"{key:<40} | {mem:<10} | {dims}")

    print("\n[2/3] Configuring indicator benchmarks...")
    all_benchmarks: list[dict[str, Any]] = get_indicator_configs(data_cache)

    if indicators:
        benchmarks: list[dict[str, Any]] = [b for b in all_benchmarks if b["name"] in indicators]
        print(f"      - Filtering for: {', '.join(indicators)}")
    else:
        benchmarks = all_benchmarks
        print(f"      - Running all {len(benchmarks)} registered indicators.")

    print("\n[3/3] Running benchmarks...")
    results: list[dict[str, Any]] = []

    for b in tqdm(benchmarks, desc="Indicators"):
        name: str = b["name"]

        # Define configurations
        configs: list[dict[str, Any]] = [
            {
                "lib": "Earthkit",
                "mode": "1. No Flox (Standard)",
                "func": b["ek_func"],
                "args": b["ek_args"]["lazy"],
                "use_flox": False,
            },
            {
                "lib": "Earthkit",
                "mode": "2. Flox (Standard)",
                "func": b["ek_func"],
                "args": b["ek_args"]["lazy"],
                "use_flox": True,
            },
            {
                "lib": "Earthkit",
                "mode": "3. Flox + Opt (Manual)",
                "func": b["ek_func"],
                "args": b["ek_args"]["optimized"],
                "use_flox": True,
            },
            {
                "lib": "Xclim",
                "mode": "1. No Flox (Standard)",
                "func": b["xi_func"],
                "args": b["xi_args"]["lazy"],
                "use_flox": False,
            },
            {
                "lib": "Xclim",
                "mode": "2. Flox (Standard)",
                "func": b["xi_func"],
                "args": b["xi_args"]["lazy"],
                "use_flox": True,
            },
            {
                "lib": "Xclim",
                "mode": "3. Flox + Opt (Manual)",
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

    # Add speedup relative to Xclim No Flox (Standard) for each indicator
    try:
        reference_times = (
            df[(df["Library"] == "Xclim") & (df["Mode"] == "1. No Flox (Standard)")]
            .set_index("Indicator")["mean_time"]
            .to_dict()
        )
        df["Speedup"] = df.apply(
            lambda row: reference_times.get(row["Indicator"], 1.0) / row["mean_time"] if row["mean_time"] > 0 else 1.0,
            axis=1,
        )
    except Exception as e:
        print(f"Warning: Could not calculate speedup: {e}")
        df["Speedup"] = 1.0

    print("\n" + "=" * 80)
    print(" PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 80)
    print(
        df.to_string(
            index=False,
            formatters={"mean_time": "{:.3f}s".format, "Speedup": "{:.2f}x".format},
        )
    )
    print("=" * 80)

    if plot:
        plot_results(df)


if __name__ == "__main__":
    fire.Fire(run_benchmarks)
