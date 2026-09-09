"""Generate rendered outputs for the docs/examples.md page.

Each block is a small, deterministic demonstration of one
example script in `examples/`. The output is written to
`docs/examples/outputs/` as both Markdown fragments and JSON for
the build to consume.

Run with:

    python scripts/build_examples_outputs.py
"""

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reachq.generators import (  # noqa: E402
    cycle_graph,
    layered_dag,
    path_graph,
    petersen_graph,
    random_dag,
)
from reachq.graph import Digraph, WeightedDigraph  # noqa: E402
from reachq.hopset import build_hopset_for_sssp  # noqa: E402
from reachq.invariants import (  # noqa: E402
    assert_distance_approximation,
    assert_reachability_preserved,
)
from reachq.reachability import bfs_reachability, parallel_bfs  # noqa: E402
from reachq.shortcut import build_shortcut_set_for_reachability  # noqa: E402
from reachq.shortest_paths import dijkstra, shortest_path_hopbound  # noqa: E402

OUT_DIR = ROOT / "docs" / "examples" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def citation_graph(n: int, density: float, seed: int) -> Digraph:
    rng = random.Random(seed)
    g = Digraph()
    for i in range(n):
        g.add_vertex(i)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                g.add_edge(i, j)
    return g


def gnn_preprocessing(n: int, density: float, seed: int) -> dict:
    g = citation_graph(n, density, seed)
    shortcuts, beta, realised = build_shortcut_set_for_reachability(
        g, omega=3.0, random_seed=seed
    )
    # Soundness for sampled sources.
    for src in (0, n // 4, n // 2, 3 * n // 4):
        assert parallel_bfs(g, src, shortcuts) == bfs_reachability(g, src)
    return {
        "n": g.num_vertices(),
        "m": g.num_edges(),
        "shortcuts": len(shortcuts),
        "beta": round(beta, 3),
        "realised_bound": round(realised, 3),
        "ratio_h_over_e": round(len(shortcuts) / max(1, g.num_edges()), 3),
    }


def rag_reranking(n_docs: int, density: float, seed: int) -> dict:
    rng = random.Random(seed)
    g = Digraph()
    for i in range(n_docs):
        g.add_vertex(f"d{i}")
    for i in range(n_docs):
        for j in range(n_docs):
            if i != j and rng.random() < density:
                g.add_edge(f"d{i}", f"d{j}")
    shortcuts, beta, _ = build_shortcut_set_for_reachability(
        g, omega=3.0, random_seed=seed
    )
    # Sample pivot-reach ranking: vertices reachable from d0 in 1 hop.
    seed_doc = "d0"
    direct = g.out_edges.get(seed_doc, set())
    return {
        "n_docs": n_docs,
        "shortcuts": len(shortcuts),
        "beta": round(beta, 3),
        "direct_citations": len(direct),
        "top_pivot_ranked_sample": sorted(direct)[:5],
    }


def compiler_inlining(n_blocks: int, density: float, seed: int) -> dict:
    g = random_dag(n=n_blocks, edge_probability=density, random_seed=seed)
    shortcuts, beta, _ = build_shortcut_set_for_reachability(
        g, omega=3.0, random_seed=seed
    )
    # Inlining candidates = vertices with many incoming edges.
    incoming = {v: len(g.in_edges.get(v, set())) for v in g.vertices()}
    top = sorted(incoming.items(), key=lambda kv: -kv[1])[:5]
    return {
        "n_blocks": g.num_vertices(),
        "shortcuts": len(shortcuts),
        "beta": round(beta, 3),
        "top_inlining_candidates": [(v, d) for v, d in top],
    }


def social_network(n: int, density: float, seed: int) -> dict:
    g = random_dag(n=n, edge_probability=density, random_seed=seed)
    shortcuts, beta, _ = build_shortcut_set_for_reachability(
        g, omega=3.0, random_seed=seed
    )
    return {
        "n": g.num_vertices(),
        "m": g.num_edges(),
        "shortcuts": len(shortcuts),
        "beta": round(beta, 3),
        "ratio_h_over_e": round(len(shortcuts) / max(1, g.num_edges()), 3),
    }


def bioinformatics(n_proteins: int, density: float, seed: int) -> dict:
    rng = random.Random(seed)
    g = Digraph()
    for i in range(n_proteins):
        g.add_vertex(f"P{i}")
    for i in range(n_proteins):
        for j in range(n_proteins):
            if i != j and rng.random() < density:
                g.add_edge(f"P{i}", f"P{j}")
    shortcuts, beta, _ = build_shortcut_set_for_reachability(
        g, omega=3.0, random_seed=seed
    )
    # Downstream hubs: vertices reachable from P0 in <= 2 hops.
    seed_v = "P0"
    reach_1 = parallel_bfs(g, seed_v, set()) | g.out_edges.get(seed_v, set())
    reach_2 = set(reach_1)
    for u in reach_1:
        reach_2 |= g.out_edges.get(u, set())
    return {
        "n_proteins": g.num_vertices(),
        "shortcuts": len(shortcuts),
        "beta": round(beta, 3),
        "downstream_2hop": len(reach_2 - {seed_v}),
    }


def hopset_demo() -> dict:
    g = WeightedDigraph()
    edges = [
        (0, 1, 1), (1, 2, 2), (2, 3, 3),
        (0, 3, 10), (3, 4, 1), (4, 5, 2),
        (0, 5, 12), (5, 6, 1), (1, 4, 5),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    hopset, beta = build_hopset_for_sssp(g, epsilon=0.1, random_seed=42)
    exact = dijkstra(g, 0)
    approx = shortest_path_hopbound(g, hopset, 0, max_hops=100)
    max_ratio = 0.0
    for v in g.vertices():
        if v in exact and v in approx and exact[v] > 0:
            r = approx[v] / exact[v]
            if r > max_ratio:
                max_ratio = r
    return {
        "n": g.num_vertices(),
        "m": g.num_edges(),
        "hopset_size": len(hopset),
        "beta": round(beta, 3),
        "max_approximation_ratio": round(max_ratio, 4),
        "exact_distances": {int(v): int(d) for v, d in exact.items()},
        "approx_distances": {int(v): int(d) for v, d in approx.items()},
    }


def main() -> None:
    out = {
        "gnn_preprocessing": gnn_preprocessing(n=200, density=0.02, seed=42),
        "rag_reranking": rag_reranking(n_docs=80, density=0.04, seed=42),
        "compiler_inlining": compiler_inlining(n_blocks=120, density=0.15, seed=42),
        "social_network": social_network(n=500, density=0.01, seed=42),
        "bioinformatics": bioinformatics(n_proteins=200, density=0.02, seed=42),
        "hopset_demo": hopset_demo(),
    }
    json_path = OUT_DIR / "examples.json"
    json_path.write_text(json.dumps(out, indent=2))
    print(f"wrote {json_path}")
    for k, v in out.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()