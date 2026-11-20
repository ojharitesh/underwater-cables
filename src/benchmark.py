"""Benchmark the minimum-spanning-tree implementation.

Run this file directly from the repository root with, for example:

    python src/benchmark.py --sizes 10 100 500

The generated graphs always contain a spanning tree, so the benchmark measures
the normal successful path of ``underwaterCablesGreedy``.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from .methods import underwaterCablesGreedy
except ImportError:
    from methods import underwaterCablesGreedy


Edge = tuple[int, int, int]
Graph = tuple[list[int], list[Edge]]


@dataclass(frozen=True)
class BenchmarkResult:
    """Timing and size information for one graph size."""

    vertices: int
    edges: int
    average_milliseconds: float
    total_cost: int
    trial_milliseconds: tuple[float, ...]


def generate_graph(
    vertex_count: int,
    extra_edges: int,
    rng: random.Random,
) -> Graph:
    """Create a connected weighted graph with a reproducible random layout."""
    if vertex_count < 0:
        raise ValueError("vertex_count must be non-negative")
    if extra_edges < 0:
        raise ValueError("extra_edges must be non-negative")

    vertices = list(range(vertex_count))
    edges: list[Edge] = [
        (vertex, vertex + 1, rng.randint(1, 1_000))
        for vertex in range(max(0, vertex_count - 1))
    ]
    existing_pairs = {(u, v) for u, v, _ in edges}
    maximum_edges = vertex_count * (vertex_count - 1) // 2
    target_edges = min(vertex_count - 1 + extra_edges, maximum_edges)

    while len(edges) < target_edges:
        u, v = sorted(rng.sample(vertices, 2))
        if (u, v) not in existing_pairs:
            existing_pairs.add((u, v))
            edges.append((u, v, rng.randint(1, 1_000)))

    return vertices, edges


def benchmark(
    sizes: Sequence[int],
    *,
    extra_edges: int = 0,
    trials: int = 3,
    seed: int = 202,
) -> list[BenchmarkResult]:
    """Benchmark Kruskal's algorithm for each requested vertex count."""
    if trials < 1:
        raise ValueError("trials must be at least 1")

    rng = random.Random(seed)
    results: list[BenchmarkResult] = []
    for size in sizes:
        graph = generate_graph(size, extra_edges, rng)
        durations: list[int] = []
        total_cost: int | None = None

        for _ in range(trials):
            start = time.perf_counter_ns()
            mst_result = underwaterCablesGreedy(graph)
            durations.append(time.perf_counter_ns() - start)

            if not isinstance(mst_result, tuple):
                raise RuntimeError(
                    f"generated graph with {size} vertices is disconnected"
                )
            _, total_cost = mst_result

        assert total_cost is not None
        average_milliseconds = sum(durations) / trials / 1_000_000
        results.append(
            BenchmarkResult(
                vertices=size,
                edges=len(graph[1]),
                average_milliseconds=average_milliseconds,
                total_cost=total_cost,
                trial_milliseconds=tuple(
                    duration / 1_000_000 for duration in durations
                ),
            )
        )

    return results


def write_empirical_results(
    results: Sequence[BenchmarkResult],
    output_path: Path,
) -> None:
    """Write benchmark measurements to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    trial_count = max(
        (len(result.trial_milliseconds) for result in results),
        default=0,
    )
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        header = [
            "vertices",
            "edges",
            "edge_density_percent",
            "mst_total_cost",
            "average_runtime_ms",
        ]
        header.extend(
            f"trial_{trial_number}_runtime_ms"
            for trial_number in range(1, trial_count + 1)
        )
        writer.writerow(header)
        for result in results:
            density = (
                result.edges
                / (result.vertices * (result.vertices - 1) / 2)
                * 100
                if result.vertices >= 2
                else 0.0
            )
            row = [
                result.vertices,
                result.edges,
                f"{density:.2f}",
                result.total_cost,
                f"{result.average_milliseconds:.6f}",
            ]
            row.extend(
                f"{duration:.6f}"
                for duration in result.trial_milliseconds
            )
            row.extend(
                "" for _ in range(trial_count - len(result.trial_milliseconds))
            )
            writer.writerow(row)


def write_plots_notebook(output_path: Path) -> None:
    """Create a Jupyter notebook that loads and plots the empirical results."""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Underwater Cables Empirical Results\n",
                    "\n",
                    "Run this notebook to visualize the benchmark measurements written by "
                    "`src/benchmark.py`.",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import csv\n",
                    "from pathlib import Path\n",
                    "\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "csv_path = next(\n",
                    "    path for path in (\n",
                    "        Path(\"empirical_results.csv\"),\n",
                    "        Path(\"assets/empirical_results.csv\"),\n",
                    "    )\n",
                    "    if path.exists()\n",
                    ")\n",
                    "with csv_path.open(\"r\", newline=\"\", encoding=\"utf-8\") as csv_file:\n",
                    "    results = list(csv.DictReader(csv_file))\n",
                    "\n",
                    "vertices = [int(row[\"vertices\"]) for row in results]\n",
                    "edge_counts = [int(row[\"edges\"]) for row in results]\n",
                    "times = [float(row[\"average_runtime_ms\"]) for row in results]\n",
                    "costs = [int(row[\"mst_total_cost\"]) for row in results]\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "plt.figure(figsize=(8, 5))\n",
                    "plt.plot(vertices, times, marker=\"o\")\n",
                    "plt.xlabel(\"Number of vertices\")\n",
                    "plt.ylabel(\"Average runtime (milliseconds)\")\n",
                    "plt.title(\"Underwater Cables Benchmark Runtime\")\n",
                    "plt.grid(True, alpha=0.3)\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "plt.figure(figsize=(8, 5))\n",
                    "plt.plot(vertices, edge_counts, marker=\"o\")\n",
                    "plt.xlabel(\"Number of vertices\")\n",
                    "plt.ylabel(\"Number of edges\")\n",
                    "plt.title(\"Generated Graph Size\")\n",
                    "plt.grid(True, alpha=0.3)\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "plt.figure(figsize=(8, 5))\n",
                    "plt.plot(vertices, costs, marker=\"o\", color=\"green\")\n",
                    "plt.xlabel(\"Number of vertices\")\n",
                    "plt.ylabel(\"Minimum spanning tree cost\")\n",
                    "plt.title(\"Minimum Cable Cost\")\n",
                    "plt.grid(True, alpha=0.3)\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(notebook, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def _parse_args(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
            150,
            200,
            300,
            400,
            500,
            750,
            1_000,
        ],
        help="vertex counts to benchmark",
    )
    parser.add_argument(
        "--extra-edges",
        type=int,
        default=0,
        help="additional random edges per graph",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=5,
        help="timed runs per graph",
    )
    parser.add_argument("--seed", type=int, default=202, help="random seed")
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the benchmark and create CSV and notebook deliverables."""
    args = _parse_args(arguments)
    if any(size < 1 for size in args.sizes):
        raise SystemExit("All benchmark sizes must be at least 1.")

    results = benchmark(
        args.sizes,
        extra_edges=args.extra_edges,
        trials=args.trials,
        seed=args.seed,
    )

    project_root = Path(__file__).resolve().parent.parent
    assets_directory = project_root / "assets"
    csv_path = assets_directory / "empirical_results.csv"
    notebook_path = assets_directory / "plots.ipynb"

    write_empirical_results(results, csv_path)
    write_plots_notebook(notebook_path)

    print("vertices | edges | edge density | average (ms) | MST cost")
    print("-" * 57)
    for result in results:
        density = (
            result.edges
            / (result.vertices * (result.vertices - 1) / 2)
            * 100
            if result.vertices >= 2
            else 0.0
        )
        print(
            f"{result.vertices:8d} | {result.edges:5d} | "
            f"{density:11.2f}% | "
            f"{result.average_milliseconds:12.6f} | "
            f"{result.total_cost:8d}"
        )
    print(f"\nCSV: {csv_path}")
    print(f"Notebook: {notebook_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())