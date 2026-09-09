"""JLS shortcut-set construction.

Public entry points:

* :func:`build_shortcut_set_for_reachability` -- Theorem 2 wrapper.
* :func:`jls_with_tc_pruning` -- direct JLS-with-TC entry point.
* :class:`ShortcutState` -- immutable worker payload.

Domain helpers:

* :func:`condense_to_dag` -- SCC condensation for cyclic inputs.
* :func:`intra_scc_shortcuts` -- exact intra-SCC reachability edges.
* :func:`density_aware_constant` -- sampling-constant heuristic.
* :func:`adaptive_scale` -- adaptive sampling multiplier.
* :func:`build_state` -- construct a worker-state from a Digraph.

The algorithm flows::

    graph -> condense_to_dag -> intra_scc_shortcuts +
            cfr_dag      -> jls_recursive -> shortcuts

State binds the CSR pair, vertex tuple, and ``max_hops`` once per
call and threads it through every recursion step. There are no
module-level globals: omega, the sampling constant, and the
parallel-mode choice all flow as explicit parameters.

Parallel dispatch:

When ``refinement.parallel`` is True and ``parallel_workers > 1``,
the per-pivot BFS runs across a process pool with ``spawn`` start
method so numpy/scipy re-import cleanly per worker. Sequential mode
is otherwise equivalent and avoids the spawn re-import cost, which
dominates the per-pivot BFS for graphs with fewer than ~1000
vertices.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any

import numpy as np

from reachq.config import get_logger
from reachq.csr import build_csr_pair
from reachq.graph import Digraph, partition_by_labels
from reachq.reachability import bfs_reachability, reverse_bfs_reachability
from reachq.trace import trace
from reachq._shortcut_internals import (
    PARALLEL_SPAWN_WARN_BELOW,
    bfs_reachable,
    build_labels,
    deque_hop_limited_bfs,
    expand_one_pivot,
    sample_pivots,
    validate_algorithm_params,
)

MIN_CSR_VERTICES = 500


@dataclass(frozen=True)
class ShortcutState:
    """Immutable worker payload passed to per-pivot expanders.

    When constructed via :func:`build_state`, the CSR arrays carry
    the vertex indices in insertion order. ``csr_indptr`` /
    ``csr_indices`` are the forward CSR pair; ``csr_rev_indptr``
    and ``csr_rev_indices`` are the reverse pair. When the graph is
    too small to warrant CSR conversion both pairs are ``None``.
    Workers handle the no-CSR path directly using the deque-based
    fallback in :mod:`reachq._shortcut_internals`.
    """

    csr_indptr: np.ndarray | None
    csr_indices: np.ndarray | None
    csr_rev_indptr: np.ndarray | None
    csr_rev_indices: np.ndarray | None
    idx_to_vertex: tuple[object, ...]
    n: int
    max_hops: int | None = None


def build_state(graph: Digraph, *, max_hops: int | None = None) -> ShortcutState:
    """Construct a worker-state payload from a Digraph.

    Uses a CSR pair when the graph has at least
    :data:`MIN_CSR_VERTICES` vertices; below that threshold the
    deque-based Python BFS is faster than CSR conversion.
    """
    if graph.num_vertices() >= MIN_CSR_VERTICES:
        indptr, indices, indptr_rev, indices_rev, n, idx_to_vertex = build_csr_pair(
            graph
        )
    else:
        indptr = indices = indptr_rev = indices_rev = None  # type: ignore[assignment]
        n = graph.num_vertices()
        idx_to_vertex = graph.vertices()
    return ShortcutState(
        csr_indptr=indptr,
        csr_indices=indices,
        csr_rev_indptr=indptr_rev,
        csr_rev_indices=indices_rev,
        idx_to_vertex=idx_to_vertex,
        n=n,
        max_hops=max_hops,
    )


def density_aware_constant(rho: float, k: float) -> float:
    """Sampling constant chosen by graph density.

    The default constant is ``10.0``; sparse graphs (rho < k)
    shrink it, floored at ``1.0``. Dense graphs keep ``10.0``.
    """
    if rho <= 0 or k <= 1:
        return 10.0
    scale = min(1.0, max(0.1, rho / max(1.0, k)))
    return 10.0 * scale


def adaptive_scale(
    parts: list[set[object]],
    n_global: int,
    level: int,
    k: float,
) -> float:
    """Multiplier on the sampling constant for the next recursion level.

    Clips to ``[0.1, 10]``; if all parts are empty returns ``1.0``.
    """
    if not parts:
        return 1.0
    largest = max(len(p) for p in parts)
    if n_global <= 1 or k <= 1:
        return 1.0
    target = max(1, int(n_global / (k ** (level + 2))))
    if largest <= 0 or target <= 0:
        return 1.0
    return min(10.0, max(0.1, target / largest))


def condense_to_dag(
    graph: Digraph,
) -> tuple[list[list[object]], dict[object, int], list[object]]:
    """Compute the SCC condensation of ``graph`` as a DAG.

    Returns:
        ``(sccs, scc_map, representatives)``. Each SCC appears as
        a list of vertices in insertion order. The representative
        of SCC ``i`` is the first vertex of ``sccs[i]``.

    Inter-SCC edges are not produced here; the call to
    :func:`build_shortcut_set_for_reachability` constructs the
    condensation DAG explicitly.
    """
    from reachq.reachability import strongly_connected_components

    components = strongly_connected_components(graph)
    sccs = [sorted(c, key=lambda v: graph.index_of(v)) for c in components]
    scc_map: dict[object, int] = {}
    representatives: list[object] = []
    for idx, scc in enumerate(sccs):
        for v in scc:
            scc_map[v] = idx
        representatives.append(scc[0])
    return sccs, scc_map, representatives


def intra_scc_shortcuts(
    graph: Digraph,
    sccs: list[list[object]],
) -> set[tuple[object, object]]:
    """Exact intra-SCC reachability edges (reachability, unweighted).

    For each non-trivial SCC, every vertex reaches every other via
    the SCC's own edges. Emits the missing pairs as shortcuts so
    that condensation does not lose reachability information.
    """
    shortcuts: set[tuple[object, object]] = set()
    for scc in sccs:
        if len(scc) <= 1:
            continue
        sub = graph.induced_subgraph(set(scc))
        for u in scc:
            r_minus = {
                v for v in sub.iter_vertices() if u != v and v in bfs_reachable(sub, u)
            }
            for v in r_minus:
                shortcuts.add((u, v))
    return shortcuts


def pivot_probability(
    k: float, level: int, n_global: int, sampling_constant: float
) -> float:
    """Per-level pivot probability ``min(1, c * k^(l+1) * log(n) / n)``."""
    if n_global <= 1:
        return 0.0
    log_n = math.log2(n_global)
    return min(1.0, sampling_constant * (k ** (level + 1)) * log_n / n_global)


# ---------------------------------------------------------------------------
# Per-pivot expanders and dispatch.
#
# `expand_pivot` is the module-level callable used by both sequential
# dispatch and the process-pool worker. It delegates to
# `expand_one_pivot` from `_shortcut_internals`. `run_pivots` chooses
# sequential or process-pool based on flags + parallel_workers; the
# spawn cost is logged at most once per call.
# ---------------------------------------------------------------------------


def expand_pivot(
    args: tuple[Digraph, ShortcutState, object],
) -> dict[str, Any]:
    """Worker function: ``expand_pivot((graph, state, pivot))``."""
    graph, state, pivot = args
    return expand_one_pivot(graph, state, pivot)


def run_pivots(
    graph: Digraph,
    state: ShortcutState,
    pivots: Iterable[object],
    *,
    parallel: bool,
    n_workers: int,
    build_ctx: BuildContext,
) -> list[dict[str, Any]]:
    """Dispatch ``pivots`` through :func:`expand_pivot`.

    Sequential when ``parallel`` is False or ``n_workers <= 1``;
    otherwise a ``ProcessPoolExecutor`` with ``spawn`` start method.

    The per-call ``build_ctx`` carries the spawn-warning latch, so
    concurrent ``build_shortcut_set_for_reachability`` calls cannot
    clobber each other's bookkeeping through a shared module global.

    Public because :mod:`tests.test_shortcut_parallel` exercises
    the dispatcher directly.
    """
    tasks = [(graph, state, item) for item in pivots]
    if not parallel or n_workers <= 1:
        return [expand_pivot(t) for t in tasks]
    if not build_ctx.spawn_warn_emitted and graph.num_vertices() < PARALLEL_SPAWN_WARN_BELOW:
        build_ctx.spawn_warn_emitted = True
        get_logger("reachq.shortcut").info(
            "process-pool spawn cost may exceed the per-pivot BFS for "
            "graph with %d vertices (< %d); consider sequential mode "
            "for small graphs.",
            graph.num_vertices(),
            PARALLEL_SPAWN_WARN_BELOW,
        )
    import multiprocessing

    ctx = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx) as pool:
        return list(pool.map(expand_pivot, tasks))


@dataclass
class BuildContext:
    """Per-invocation bookkeeping for a JLS build.

    Holds mutable state that must not be shared across concurrent
    builds. Construct one ``BuildContext`` per call to
    :func:`build_shortcut_set_for_reachability` (or
    :func:`jls_with_tc_pruning`) to keep concurrent builds
    independent.
    """

    spawn_warn_emitted: bool = False

    def reset(self) -> None:
        """Clear the spawn-warning latch. Test helper."""
        self.spawn_warn_emitted = False


def reset_spawn_warn_emitted(build_ctx: BuildContext) -> None:
    """Test hook: clear the spawn-warning latch on ``build_ctx``.

    Public because :mod:`tests.test_shortcut_parallel` invokes it
    between calls to inspect log capture.
    """
    build_ctx.reset()


def jls_recursive(
    graph: Digraph,
    state: ShortcutState,
    k: float,
    rho: float,
    max_level: int,
    n_global: int,
    level: int,
    rng,
    flags,
    sampling_constant: float,
    *,
    parallel: bool,
    n_workers: int,
    tc_threshold: float | None = None,
    build_ctx: BuildContext,
) -> set[tuple[object, object]]:
    """JLS recursion body.

    Sample pivots, expand ``R-/R+`` per pivot, build labels,
    partition by label equality, recurse on each non-trivial part.
    Returns the union of shortcut edges from this level and below.

    Public because :mod:`reachq.research` helpers and the
    property-based tests invoke the recursion directly.
    """
    n = graph.num_vertices()
    if n == 0 or level >= max_level:
        return set()

    base_prob = pivot_probability(k, level, n_global, sampling_constant)

    vertices = list(graph.iter_vertices())
    out_degrees: dict[object, int] = (
        {v: graph.degree_out(v) for v in vertices}
        if flags.degree_ordered_pivots
        else {}
    )
    pivots = sample_pivots(
        vertices,
        base_prob,
        out_degrees,
        degree_aware=flags.degree_ordered_pivots,
        rng=rng,
    )
    pivots.sort(key=lambda v: graph.index_of(v))

    if not pivots:
        return set()

    shortcuts: set[tuple[object, object]] = set()
    r_minus_per_pivot: dict[object, set[object]] = {}
    r_plus_per_pivot: dict[object, set[object]] = {}

    pivot_results = run_pivots(
        graph,
        state,
        pivots,
        parallel=parallel,
        n_workers=n_workers,
        build_ctx=build_ctx,
    )

    from reachq.prune import apply_tc_pruning

    for pivot, result in zip(pivots, pivot_results):
        r_minus = result.get("r_minus", set())
        r_plus = result.get("r_plus", set())
        r_minus_per_pivot[pivot] = r_minus
        r_plus_per_pivot[pivot] = r_plus
        for v in r_minus:
            shortcuts.add((v, pivot))
        for v in r_plus:
            shortcuts.add((pivot, v))

        if flags.enable_tc_pruning and tc_threshold is not None:
            r_ball = r_minus | r_plus | {pivot}
            shortcuts |= apply_tc_pruning(graph, r_ball, tc_threshold)

    labels = build_labels(vertices, pivots, r_plus_per_pivot, r_minus_per_pivot)
    parts = partition_by_labels(vertices, labels)

    if len(parts) <= 1 and flags.skip_trivial_part:
        return shortcuts

    next_sampling = sampling_constant
    if flags.adaptive_sampling:
        scale = adaptive_scale(parts, n_global, level, k)
        next_sampling = sampling_constant * scale

    for part in parts:
        if len(part) <= 1:
            continue
        sub = graph.induced_subgraph(part)
        sub_state = build_state(sub, max_hops=state.max_hops)
        sub_rng = rng
        sub_shortcuts = jls_recursive(
            sub,
            sub_state,
            k,
            rho,
            max_level,
            n_global,
            level + 1,
            sub_rng,
            flags,
            next_sampling,
            parallel=parallel,
            n_workers=n_workers,
            tc_threshold=tc_threshold,
            build_ctx=build_ctx,
        )
        shortcuts |= sub_shortcuts

    return shortcuts


def params_from_omega(
    n: int, m: int, omega: float
) -> tuple[float, float, int, float, float]:
    """Standard parameter selection for JLS.

    Returns ``(k, rho, max_level, beta, realised_bound)``.

    ``beta`` is the paper's asymptotic target hop bound
    ``(n^omega/m)^(1/(2*omega-2))``. ``realised_bound`` is the
    *algorithm's actual guarantee* based on the chosen ``rho`` and
    ``max_level``: a single per-level hop path of length
    ``max(2, ceil(rho))`` is composed across ``max_level`` levels
    plus a final hop, giving ``max_level * max(2, ceil(rho)) + 1``.
    The test suite asserts this realised bound, not the
    asymptotic target.

    Public because :mod:`reachq.research.sparsify_hop` imports it
    to mirror the JLS bound when computing the realised β for a
    hop-bounded sparsifier.
    """
    k = max(2.0, math.log2(n))
    beta = (n**omega / m) ** (1.0 / (2.0 * omega - 2.0)) if m > 0 else float("inf")
    rho = max(1.0, math.sqrt(n) / beta) if beta > 0 else 1.0
    rho = min(rho, math.sqrt(n))
    max_level = max(1, int(math.log(n) / math.log(k)) + 1) if k > 1 else 1
    realised_bound = float(max_level * max(2, math.ceil(rho))) + 1.0
    return k, rho, max_level, beta, realised_bound


def build_shortcut_set_for_reachability(
    graph: Digraph,
    omega: float = 3.0,
    random_seed: int | None = None,
    refinement: Any = None,
    parallel_workers: int = 1,
) -> tuple[set[tuple[object, object]], float, float]:
    """Construct a ``beta``-shortcut set matching Theorem 2.

    Returns ``(shortcuts, beta, realised_bound)``.

    ``beta`` is the paper's asymptotic target hop bound
    ``(n^omega/m)^(1/(2*omega-2))``. ``realised_bound`` is the
    algorithm's actual upper bound on hops, derived from the
    chosen ``rho`` and recursion depth. Test oracles should
    assert against ``realised_bound``; the asymptotic ``beta``
    is for documentation and reference.

    Args:
        graph: Input digraph (cycles handled by SCC condensation).
        omega: Fast matrix multiplication exponent.
        random_seed: Optional seed for reproducibility.
        refinement: A :class:`reachq.config.RefinementConfig`.
        parallel_workers: When ``>1`` and ``refinement.parallel`` is
            True, the per-pivot BFS dispatches across a process pool.

    Returns:
        ``(shortcuts, beta, realised_bound)``. ``beta`` is the
        asymptotic target hop bound (Theorem 2);
        ``realised_bound`` is the algorithm's actual guarantee
        based on the chosen ``rho`` and recursion depth.
    """
    from reachq.config import RefinementConfig
    from reachq.prune import compute_tc_pruning_threshold

    with trace("build_shortcut_set", n=graph.num_vertices(), m=graph.num_edges()):
        flags = (
            refinement
            if isinstance(refinement, RefinementConfig)
            else RefinementConfig.from_dict(refinement)
        )
        n = graph.num_vertices()
        m = graph.num_edges()
        if n == 0:
            return set(), 0.0, 0.0

        sccs, scc_map, representatives = condense_to_dag(graph)
        trivial = (
            flags.skip_condense and all(len(scc) == 1 for scc in sccs)
        ) or n == len(sccs)
        if trivial:
            dag = graph
        else:
            dag = Digraph()
            for idx in range(len(sccs)):
                dag.add_vertex(idx)
            for u, v in graph.edges():
                if scc_map[u] != scc_map[v]:
                    dag.add_edge(scc_map[u], scc_map[v])

        k, rho, max_level, beta, realised_bound = params_from_omega(n, m, omega)

        sampling_constant = (
            density_aware_constant(rho, k) if flags.adaptive_sampling else 10.0
        )

        state = build_state(dag)
        log_n = math.log2(n) if n > 1 else 0.0
        tc_threshold = (
            compute_tc_pruning_threshold(k, log_n, rho, n, omega)
            if flags.enable_tc_pruning
            else None
        )

        parallel = bool(getattr(flags, "parallel", False))
        build_ctx = BuildContext()

        import random as _random

        rng = _random.Random(random_seed)

        dag_shortcuts = jls_recursive(
            dag,
            state,
            k,
            rho,
            max_level,
            n,
            level=0,
            rng=rng,
            flags=flags,
            sampling_constant=sampling_constant,
            parallel=parallel,
            n_workers=parallel_workers,
            tc_threshold=tc_threshold,
            build_ctx=build_ctx,
        )

        shortcuts: set[tuple[object, object]] = set()
        if not trivial:
            shortcuts |= intra_scc_shortcuts(graph, sccs)

        for u_idx, v_idx in dag_shortcuts:
            if trivial:
                shortcuts.add((u_idx, v_idx))
            else:
                u_rep = representatives[int(u_idx)]
                v_rep = representatives[int(v_idx)]
                shortcuts.add((u_rep, v_rep))

        return shortcuts, beta, realised_bound


def jls_with_tc_pruning(
    graph: Digraph,
    *,
    k: float,
    rho: float,
    max_level: int,
    n_global: int,
    level: int = 0,
    random_seed: int | None = None,
    refinement: Any = None,
    parallel_workers: int = 1,
    sampling_constant: float | None = None,
) -> set[tuple[object, object]]:
    """Direct JLS-with-TC entry point.

    Args:
        graph: Input digraph (caller is responsible for any condensation).
        k: Recursion widening factor (>1).
        rho: Hop-parameter (>0).
        max_level: Maximum recursion depth (>=0).
        n_global: Global vertex count used by the pivot probability.
        level: Recursion level (default 0).
        random_seed: Optional seed.
        refinement: A :class:`RefinementConfig`.
        parallel_workers: When >1 and ``refinement.parallel``, dispatch
            per-pivot BFS through a process pool.
        sampling_constant: Optional sampling-constant override.

    Returns:
        Set of shortcut edges.
    """
    from reachq.config import RefinementConfig
    from reachq.prune import compute_tc_pruning_threshold

    validate_algorithm_params(k, rho, max_level)

    flags = (
        refinement
        if isinstance(refinement, RefinementConfig)
        else RefinementConfig.from_dict(refinement)
    )
    state = build_state(graph)
    log_n = math.log2(n_global) if n_global > 1 else 0.0
    tc_threshold = (
        compute_tc_pruning_threshold(k, log_n, rho, graph.num_vertices(), omega=2.5)
        if flags.enable_tc_pruning
        else None
    )
    parallel = bool(getattr(flags, "parallel", False))
    build_ctx = BuildContext()

    if sampling_constant is None:
        sampling_constant = 10.0

    import random as _random

    rng = _random.Random(random_seed)
    return jls_recursive(
        graph,
        state,
        k,
        rho,
        max_level,
        n_global,
        level,
        rng,
        flags,
        sampling_constant,
        parallel=parallel,
        n_workers=parallel_workers,
        tc_threshold=tc_threshold,
        build_ctx=build_ctx,
    )


__all__ = [
    "MIN_CSR_VERTICES",
    "BuildContext",
    "ShortcutState",
    "adaptive_scale",
    "build_shortcut_set_for_reachability",
    "build_state",
    "condense_to_dag",
    "density_aware_constant",
    "expand_pivot",
    "intra_scc_shortcuts",
    "jls_recursive",
    "jls_with_tc_pruning",
    "params_from_omega",
    "pivot_probability",
    "reset_spawn_warn_emitted",
    "run_pivots",
]
