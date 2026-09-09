"""Internal helpers for :mod:`reachq.shortcut`.

This module hosts the implementation details of the JLS shortcut-set
construction. The leading-underscore module name signals "private" to
importers; the helpers inside use plain names so they are not
single-underscore-prefixed.

Only :mod:`reachq.shortcut` imports from this module. Anything you
need to call from outside the JLS implementation is exported from
:mod:`reachq.shortcut` directly (for example ``run_pivots``,
``params_from_omega``).
"""

from __future__ import annotations

from collections import deque

from reachq.graph import Digraph


PARALLEL_SPAWN_WARN_BELOW = 1000


def bfs_reachable(graph: Digraph, source: object) -> set[object]:
    """Plain BFS reachability from ``source`` over ``graph``."""
    visited: set[object] = {source}
    queue: deque[object] = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph.out_edges.get(u, ()):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return visited


def sample_pivots(
    vertices,
    base_prob: float,
    out_degrees: dict[object, int] | None,
    *,
    degree_aware: bool,
    rng,
) -> list[object]:
    """Sample pivots with optional degree-aware weighting.

    When ``degree_aware`` is True the per-vertex probability is
    scaled by ``1 / (1 + out_degree)`` and renormalised so the
    expected pivot count matches ``base_prob * |vertices|``.
    """
    if not degree_aware:
        return [v for v in vertices if rng.random() < base_prob]
    if not out_degrees:
        out_degrees = {}
    raw: list[tuple[object, float]] = []
    weights: list[float] = []
    for v in vertices:
        w = base_prob / (1 + out_degrees.get(v, 0))
        raw.append((v, w))
        weights.append(w)
    total = sum(weights)
    if total <= 0:
        return []
    scale = base_prob * len(raw) / total
    return [v for v, w in raw if rng.random() < w * scale]


def build_labels(
    vertices,
    pivots,
    r_plus_per_pivot: dict[object, set[object]],
    r_minus_per_pivot: dict[object, set[object]],
) -> dict[object, tuple[frozenset[object], frozenset[object]]]:
    """Per-vertex label tuple: ``(r_minus_pivots, r_plus_pivots)``."""
    anc: dict[object, list[object]] = {v: [] for v in vertices}
    des: dict[object, list[object]] = {v: [] for v in vertices}
    for pivot in pivots:
        for v in r_minus_per_pivot.get(pivot, set()):
            anc.setdefault(v, []).append(pivot)
        for v in r_plus_per_pivot.get(pivot, set()):
            des.setdefault(v, []).append(pivot)
    return {v: (frozenset(anc.get(v, [])), frozenset(des.get(v, []))) for v in vertices}


def expand_one_pivot(
    graph: Digraph,
    state,
    pivot: object,
) -> dict:
    """Expand one pivot via CSR numpy BFS or deque fallback.

    Returns ``{"r_plus": set, "r_minus": set}`` with the pivot
    itself removed from both sets.
    """
    from reachq.bfs import csr_reachable_backward, csr_reachable_forward
    from reachq.reachability import bfs_reachability, reverse_bfs_reachability

    if state.csr_indptr is None or state.csr_indices is None:
        if state.max_hops is not None:
            r_plus = deque_hop_limited_bfs(
                graph, pivot, state.max_hops, forward=True
            )
            r_minus = deque_hop_limited_bfs(
                graph, pivot, state.max_hops, forward=False
            )
        else:
            r_plus = bfs_reachability(graph, pivot)
            r_minus = reverse_bfs_reachability(graph, pivot)
        r_plus.discard(pivot)
        r_minus.discard(pivot)
        return {"r_plus": r_plus, "r_minus": r_minus}

    p_idx: int | None = None
    for i, v in enumerate(state.idx_to_vertex):
        if v == pivot:
            p_idx = i
            break
    if p_idx is None:
        return {"r_plus": set(), "r_minus": set()}
    r_plus_arr = csr_reachable_forward(
        state.csr_indptr,
        state.csr_indices,
        p_idx,
        state.n,
        max_depth=state.max_hops,
    )
    rev_indptr = state.csr_rev_indptr
    rev_indices = state.csr_rev_indices
    if rev_indptr is None or rev_indices is None:
        return {"r_plus": set(r_plus_arr), "r_minus": set()}
    r_minus_arr = csr_reachable_backward(
        rev_indptr,
        rev_indices,
        p_idx,
        state.n,
        max_depth=state.max_hops,
    )
    r_plus = {state.idx_to_vertex[int(i)] for i in r_plus_arr}
    r_minus = {state.idx_to_vertex[int(i)] for i in r_minus_arr}
    r_plus.discard(pivot)
    r_minus.discard(pivot)
    return {"r_plus": r_plus, "r_minus": r_minus}


def deque_hop_limited_bfs(
    graph: Digraph,
    source: object,
    max_hops: int,
    *,
    forward: bool,
) -> set[object]:
    """Hop-bounded deque BFS used when CSR arrays are unavailable."""
    visited: set[object] = {source}
    queue: deque[tuple[object, int]] = deque([(source, 0)])
    g = graph if forward else graph.reversed()
    while queue:
        u, d = queue.popleft()
        if d >= max_hops:
            continue
        for v in g.out_edges.get(u, ()):
            if v not in visited:
                visited.add(v)
                queue.append((v, d + 1))
    visited.discard(source)
    return visited


def validate_algorithm_params(k: float, rho: float, max_level: int) -> None:
    """Validate (k, rho, max_level) per the paper's constraints."""
    from reachq.errors import ReachqValueError

    if k <= 1:
        raise ReachqValueError(f"k must be > 1 (got {k})")
    if rho <= 0:
        raise ReachqValueError(f"rho must be > 0 (got {rho})")
    if max_level < 0:
        raise ReachqValueError(f"max_level must be non-negative (got {max_level})")


__all__ = [
    "PARALLEL_SPAWN_WARN_BELOW",
    "bfs_reachable",
    "build_labels",
    "deque_hop_limited_bfs",
    "expand_one_pivot",
    "sample_pivots",
    "validate_algorithm_params",
]