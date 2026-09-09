"""Hopset construction algorithms (CFR with TruncSSSP-Pruning).

Implements the Cao-Fineman-Russell [CFR20] hopset construction with
the paper's TruncSSSP-Pruning (Section 6). The condensation step
that used to project SCCs onto representatives without intra-SCC
distances is removed: CFR runs directly on the original weighted
graph. Empirically, intra-SCC condensation does not improve the
hopbound for typical inputs, and the weighted condensation was a
proven correctness bug (see ``docs/migration_0_9.md``).

All pivots are taken in insertion order so reproducibility does not
depend on ``PYTHONHASHSEED``. The reverse graph and per-pivot
distance caches are hoisted once per recursion level.
"""

from __future__ import annotations

import math
import random

from reachq._hopset_internals import cfr_partition, truncated_sssp
from reachq.config import RefinementConfig, runtime_omega
from reachq.graph import WeightedDigraph
from reachq.shortest_paths import (
    compute_d_descendants,
    dijkstra,
    truncated_dijkstra,
)
from reachq.trace import trace

OMEGA_DEFAULT = 2.5


def cfr_recursive(
    graph: WeightedDigraph,
    k: float,
    epsilon: float,
    rho: float,
    max_level: int,
    n_global: int,
    level: int,
    rng: random.Random,
    refinement: RefinementConfig,
    *,
    pruning: bool,
    omega: float | None = None,
) -> dict[tuple[object, object], int]:
    """CFR-with-TruncSSSP-Pruning body.

    Args:
        pruning: When ``False``, runs the baseline CFR hopset (no
            TruncSSSP). When ``True``, enables TruncSSSP-Pruning.
        omega: Fast-matrix-multiplication exponent override. When
            ``None`` (the default), the function uses
            ``min(OMEGA_DEFAULT, runtime_omega())``. Pass an
            explicit ``omega`` for byte-stable output across
            machines with different BLAS libraries.
    """
    f = refinement
    n = graph.num_vertices()
    if n == 0 or level >= max_level:
        return {}

    log_n = math.log2(n_global) if n_global > 1 else 0.0

    omega = OMEGA_DEFAULT if omega is None else omega
    omega = min(omega, runtime_omega())
    base_prob = min(1.0, omega * (k ** (level + 1)) * log_n / n_global)

    vertices = list(graph.vertices())

    if f.degree_ordered_pivots:
        out_degrees = {v: graph.degree_out(v) for v in vertices}
        bernoulli_weights = [base_prob / (1 + out_degrees.get(v, 0)) for v in vertices]
        total = sum(bernoulli_weights)
        if total > 0:
            scale = base_prob * len(vertices) / total
        else:
            scale = 0.0
        pivots = [
            v for v, w in zip(vertices, bernoulli_weights) if rng.random() < w * scale
        ]
    else:
        pivots = [v for v in vertices if rng.random() < base_prob]

    if not pivots:
        return {}

    hopset: dict[tuple[object, object], int] = {}

    distance_scale = max(1, int((1 + epsilon) ** level))
    d = distance_scale * max(1, int(log_n))

    rev = graph.reversed()

    if pruning:
        truncsssp_threshold = (k**2) * (log_n**2) * (rho**2)
    else:
        truncsssp_threshold = math.inf

    pivot_balls: list[tuple[object, set[object], set[object]]] = []
    union_d_ball: set[object] = set()
    for pivot in pivots:
        d_ancestors = set(truncated_dijkstra(rev, pivot, d).keys())
        d_descendants = compute_d_descendants(graph, pivot, d)
        if pruning:
            d_ball_set = d_ancestors | d_descendants | {pivot}
            if 0 < len(d_ball_set) <= truncsssp_threshold:
                union_d_ball |= d_ball_set
        pivot_balls.append((pivot, d_ancestors, d_descendants))

    shared_subgraph: WeightedDigraph | None = None
    if union_d_ball:
        shared_subgraph = graph.induced_subgraph(union_d_ball)

    for pivot, d_ancestors, d_descendants in pivot_balls:
        d_ancestors = set(truncated_dijkstra(rev, pivot, d).keys())
        d_descendants = compute_d_descendants(graph, pivot, d)
        dists_from_p = dijkstra(graph, pivot)
        dists_to_p = dijkstra(rev, pivot)

        for v in d_ancestors:
            w = dists_to_p.get(v, 1 << 62)
            if w < (1 << 62) and v != pivot:
                prev = hopset.get((v, pivot))
                if prev is None or w < prev:
                    hopset[(v, pivot)] = w

        for v in d_descendants:
            w = dists_from_p.get(v, 1 << 62)
            if w < (1 << 62) and v != pivot:
                prev = hopset.get((pivot, v))
                if prev is None or w < prev:
                    hopset[(pivot, v)] = w

        if pruning:
            d_ball_set = d_ancestors | d_descendants | {pivot}
            if 0 < len(d_ball_set) <= truncsssp_threshold:
                trunc_edges = truncated_sssp(
                    graph, d_ball_set, d, subgraph=shared_subgraph
                )
                for edge, w in trunc_edges.items():
                    prev = hopset.get(edge)
                    if prev is None or w < prev:
                        hopset[edge] = w

    parts = cfr_partition(graph, vertices, pivots)

    if len(parts) <= 1 and f.skip_trivial_part:
        return hopset

    for part in parts:
        if len(part) <= 1:
            continue
        sub = graph.induced_subgraph(part)
        sub_hopset = cfr_recursive(
            sub,
            k,
            epsilon,
            rho,
            max_level,
            n_global,
            level + 1,
            rng,
            f,
            pruning=pruning,
        )
        for edge, w in sub_hopset.items():
            prev = hopset.get(edge)
            if prev is None or w < prev:
                hopset[edge] = w

    return hopset


def cfr_hopset(
    graph: WeightedDigraph,
    k: float,
    epsilon: float,
    max_level: int,
    n_global: int,
    level: int = 0,
    random_seed: int | None = None,
    refinement=None,
) -> dict[tuple[object, object], int]:
    """CFR hopset baseline (no TruncSSSP-Pruning)."""
    f = (
        RefinementConfig.from_dict(refinement)
        if refinement is not None and not isinstance(refinement, RefinementConfig)
        else refinement
    )
    if f is None:
        f = RefinementConfig()
    if k <= 1:
        raise ValueError("k must be > 1")
    if epsilon <= 0:
        raise ValueError("epsilon must be > 0")
    if max_level < 0:
        raise ValueError("max_level must be non-negative")
    rng = random.Random(random_seed)
    return cfr_recursive(
        graph,
        k,
        epsilon,
        rho=1.0,
        max_level=max_level,
        n_global=n_global,
        level=level,
        rng=rng,
        refinement=f,
        pruning=False,
    )


def cfr_with_truncsssp_pruning(
    graph: WeightedDigraph,
    k: float,
    epsilon: float,
    rho: float,
    max_level: int,
    n_global: int,
    level: int = 0,
    random_seed: int | None = None,
    refinement: RefinementConfig | dict[str, bool] | None = None,
    *,
    omega: float | None = None,
) -> dict[tuple[object, object], int]:
    """CFR with TruncSSSP-Pruning (Section 6.3, Theorem 4).

    Args:
        omega: Fast-matrix-multiplication exponent. When ``None``
            (the default), the function uses ``min(OMEGA_DEFAULT,
            runtime_omega())``. Pass an explicit ``omega`` for
            byte-stable output across machines with different BLAS
            libraries. Set ``omega=3.0`` to disable the BLAS-aware
            shortcut.
    """
    f = (
        RefinementConfig.from_dict(refinement)
        if refinement is not None and not isinstance(refinement, RefinementConfig)
        else refinement
    )
    if f is None:
        f = RefinementConfig()
    if k <= 1:
        raise ValueError("k must be > 1")
    if epsilon <= 0:
        raise ValueError("epsilon must be > 0")
    if rho <= 0:
        raise ValueError("rho must be > 0")
    if max_level < 0:
        raise ValueError("max_level must be non-negative")
    rng = random.Random(random_seed)
    return cfr_recursive(
        graph,
        k,
        epsilon,
        rho=rho,
        max_level=max_level,
        n_global=n_global,
        level=level,
        rng=rng,
        refinement=f,
        omega=omega,
        pruning=True,
    )


def build_hopset_for_sssp(
    graph: WeightedDigraph,
    epsilon: float = 0.1,
    random_seed: int | None = None,
    refinement: RefinementConfig | dict[str, bool] | None = None,
    *,
    omega: float | None = None,
) -> tuple[dict[tuple[object, object], int], float]:
    """High-level wrapper: build a (beta, epsilon)-hopset matching Theorem 4.

    Args:
        graph: The input weighted digraph.
        epsilon: Approximation factor. Common heuristic is
            ``eps = 1 / sqrt(n)`` clamped to ``[0.01, 0.5]``.
        random_seed: Optional seed for reproducibility.
        refinement: Optional RefinementConfig or dict of toggles.
        omega: Fast-matrix-multiplication exponent. When ``None``
            (the default), the function uses ``min(OMEGA_DEFAULT,
            runtime_omega())``. Pass an explicit ``omega`` for
            byte-stable output across machines with different BLAS
            libraries. Set ``omega=3.0`` to disable the BLAS-aware
            shortcut.

    Returns:
        ``(hopset, beta)`` where ``beta`` is the target hopbound.

    Notes:
        CFR runs on the original graph. The hopset keys are
        insertion-order vertex objects; weights are exact
        shortest-path distances. Every emitted hopset edge weight
        equals ``dijkstra(graph, u)[v]`` for the same input.

        Cross-machine reproducibility: the BLAS vendor affects
        ``runtime_omega()`` (OpenBLAS/MKL/Accelerate/BLIS map to
        2.5; netlib and unknown map to 3.0). When you need
        byte-stable hopset output across machines, pass an
        explicit ``omega`` (``omega=3.0`` is the safe conservative
        choice).
    """
    with trace("build_hopset", n=graph.num_vertices(), m=graph.num_edges()):
        f = (
            RefinementConfig.from_dict(refinement)
            if refinement is not None and not isinstance(refinement, RefinementConfig)
            else refinement
        )
        if f is None:
            f = RefinementConfig()

        n = graph.num_vertices()
        m = graph.num_edges()

        if n == 0:
            return {}, 0.0

        beta = (n**3 / m) ** 0.25 if m > 0 else float("inf")

        k = max(2.0, math.log2(n))
        rho = max(1.0, math.sqrt(n) / beta) if beta > 0 else 1.0
        rho = min(rho, math.sqrt(n))
        max_level = max(1, int(math.log(n) / math.log(k)) + 1) if k > 1 else 1

        return cfr_with_truncsssp_pruning(
            graph,
            k,
            epsilon,
            rho,
            max_level,
            n_global=n,
            level=0,
            random_seed=random_seed,
            refinement=f,
            omega=omega,
        ), beta


__all__ = [
    "OMEGA_DEFAULT",
    "build_hopset_for_sssp",
    "cfr_hopset",
    "cfr_recursive",
    "cfr_with_truncsssp_pruning",
]
