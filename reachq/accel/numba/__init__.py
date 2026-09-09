"""Numba-JIT accelerated kernels.

This module provides Numba-JIT-compiled kernels for the
CSR-based BFS and Dijkstra inner loops. The Numba kernels use
``@njit`` and ``fastmath=True`` for vectorised arithmetic where
applicable; the GIL is released during the JIT'd loops.

If Numba is not installed, the wrapper functions fall back to the
pure-Python implementations in :mod:`reachq.bfs` and
:mod:`reachq.shortest_paths`. Numba can be installed with
``pip install numba``; it adds a JIT compile cost on first call
(typically a few seconds per kernel) but the compiled kernels
execute 10-50x faster than pure Python on typical inputs.

Public API (mirrors the Cython wrappers):

- :func:`njit_bfs_forward` — forward BFS over a CSR adjacency.
- :func:`njit_dijkstra` — Dijkstra from a single source.
- :func:`is_numba_available` — True if Numba is installed.
"""

from __future__ import annotations

import numpy as np

from reachq.accel.numba import _internals as internals
from reachq.bfs import csr_reachable_forward
from reachq.shortest_paths import dijkstra


def njit_bfs_forward(
    indptr: np.ndarray,
    indices: np.ndarray,
    source: int,
    n: int,
    *,
    max_depth: int = 1 << 30,
) -> np.ndarray:
    """Forward BFS over a CSR adjacency (Numba-JIT).

    Identical API to :func:`reachq.accel.cython.bfs.cy_bfs_forward`.
    Falls back to :func:`reachq.bfs.csr_reachable_forward`
    when Numba is not installed.
    """
    if internals.is_available():
        result_ext = internals.BFS_FORWARD(
            indptr, indices, source, n, max_depth
        )
        if isinstance(result_ext, np.ndarray):
            return result_ext
    # Fallback: pure-Python returns the indices of reached vertices;
    # convert to a boolean mask of length n.
    reached_indices = csr_reachable_forward(
        indptr, indices, source, n, max_depth=max_depth
    )
    out = np.zeros(n, dtype=bool)
    out[reached_indices] = True
    return out


def njit_dijkstra(
    indptr: np.ndarray,
    indices: np.ndarray,
    weights: np.ndarray,
    source: int,
    n: int,
) -> np.ndarray:
    """Dijkstra from ``source`` over a weighted CSR adjacency (Numba-JIT).

    Falls back to :func:`reachq.shortest_paths.dijkstra` when
    Numba is not installed.
    """
    if internals.is_available():
        result = internals.DIJKSTRA(indptr, indices, weights, source, n)
        if isinstance(result, np.ndarray):
            return result
    from reachq.graph import WeightedDigraph

    g = WeightedDigraph()
    for u in range(n):
        start = int(indptr[u])
        end = int(indptr[u + 1])
        g.add_vertex(u)
        for j in range(start, end):
            v = int(indices[j])
            w = float(weights[j])
            g.add_vertex(v)
            g.add_edge(u, v, int(w))
    result = dijkstra(g, source)
    out = np.full(n, np.inf, dtype=np.float64)
    if source in g:
        out[source] = 0.0
    for v_obj, d in result.items():
        if isinstance(v_obj, int) and 0 <= v_obj < n:
            out[v_obj] = d
    return out


def is_numba_available() -> bool:
    """Return True if Numba is installed."""
    return internals.is_available()


def prewarm(
    *,
    bfs_size: int = 256,
    bfs_avg_degree: int = 4,
    bfs_depth: int = 16,
    dijkstra_size: int = 256,
    dijkstra_avg_degree: int = 4,
) -> None:
    """Pre-compile Numba kernels with representative input shapes.

    Numba JIT-compiles each kernel on its first invocation, paying
    a one-time cost (1-5 seconds per kernel on cold start) before
    subsequent calls run at native speed. For latency-sensitive
    applications where that first-call latency is unacceptable,
    call ``prewarm()`` at application startup.

    The prewarm arguments control the size and shape of the dummy
    CSR arrays used to trigger compilation. They do NOT affect the
    size of subsequent real calls — once compiled, the kernels
    specialise on the *types* (int64, float64) of the inputs, not
    their sizes.

    With the default arguments (256 vertices, 4 avg degree), prewarm
    completes in under 1 second on a typical machine. Larger inputs
    give a slightly faster compiled kernel but cost more at warmup.

    Args:
        bfs_size: Number of vertices in the dummy CSR for BFS warmup.
        bfs_avg_degree: Average out-degree in the dummy CSR.
        bfs_depth: Maximum BFS depth for the warmup call.
        dijkstra_size: Number of vertices in the dummy CSR for
            Dijkstra warmup.
        dijkstra_avg_degree: Average out-degree for Dijkstra warmup.

    Raises:
        RuntimeError: If Numba is not installed.
    """
    if not internals.is_available():
        raise RuntimeError(
            "Numba is not installed. Install with `pip install numba` "
            "or `pip install reachq[accel-numba]`."
        )
    import numpy as np

    rng = np.random.default_rng(0)
    n = bfs_size
    avg_d = max(1, bfs_avg_degree)
    indptr = np.zeros(n + 1, dtype=np.int64)
    counts = rng.poisson(avg_d, n).clip(min=0)
    np.cumsum(counts, out=indptr[1:])
    m = int(indptr[-1])
    indices = rng.integers(0, n, m, dtype=np.int64)
    # Trigger BFS compilation.
    internals.BFS_FORWARD(indptr, indices, 0, n, bfs_depth)

    n = dijkstra_size
    avg_d = max(1, dijkstra_avg_degree)
    indptr = np.zeros(n + 1, dtype=np.int64)
    counts = rng.poisson(avg_d, n).clip(min=0)
    np.cumsum(counts, out=indptr[1:])
    m = int(indptr[-1])
    indices = rng.integers(0, n, m, dtype=np.int64)
    weights = rng.uniform(1.0, 5.0, m).astype(np.float64)
    # Trigger Dijkstra compilation.
    internals.DIJKSTRA(indptr, indices, weights, 0, n)


__all__ = ["is_numba_available", "njit_bfs_forward", "njit_dijkstra", "prewarm"]