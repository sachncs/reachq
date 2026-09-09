"""Internal state for the Numba accelerator.

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed.

Only :mod:`reachq.accel.numba` imports from this module.
"""

from __future__ import annotations

from typing import Any

AVAILABLE: bool = False
NUMBA: Any = None
BFS_FORWARD: Any = None
DIJKSTRA: Any = None


def probe() -> bool:
    """Try to import numba and JIT-compile the two kernels.

    Returns:
        True if numba is available and the kernels compiled; False
        otherwise.
    """
    global AVAILABLE, NUMBA, BFS_FORWARD, DIJKSTRA
    try:
        import numba  # type: ignore[import-not-found]
    except ImportError:
        return False

    NUMBA = numba
    import numpy as np

    @numba.njit(cache=True, fastmath=True, boundscheck=False)
    def jit_bfs_forward_kernel(
        indptr: np.ndarray,
        indices: np.ndarray,
        source: int,
        n: int,
        max_depth: int,
    ) -> np.ndarray:
        """JIT-compiled forward BFS. Releases the GIL."""
        reached = np.zeros(n, dtype=numba.boolean)
        if source < 0 or source >= n:
            return reached
        reached[source] = True
        frontier = np.empty(n, dtype=np.int64)
        next_frontier = np.empty(n, dtype=np.int64)
        frontier[0] = source
        frontier_size = 1
        for _depth in range(max_depth):
            if frontier_size == 0:
                break
            next_size = 0
            for i in range(frontier_size):
                u = frontier[i]
                start = indptr[u]
                end = indptr[u + 1]
                for j in range(start, end):
                    v = indices[j]
                    if not reached[v]:
                        reached[v] = True
                        next_frontier[next_size] = v
                        next_size += 1
            for i in range(next_size):
                frontier[i] = next_frontier[i]
            frontier_size = next_size
        return reached

    @numba.njit(cache=True, fastmath=True, boundscheck=False)
    def jit_dijkstra_kernel(
        indptr: np.ndarray,
        indices: np.ndarray,
        weights: np.ndarray,
        source: int,
        n: int,
    ) -> np.ndarray:
        """JIT-compiled Dijkstra with inline binary heap. Releases the GIL."""
        dist = np.full(n, np.inf, dtype=np.float64)
        if source < 0 or source >= n:
            return dist
        # Inline binary min-heap.
        heap_dist = np.empty(n + 16, dtype=np.float64)
        heap_vertex = np.empty(n + 16, dtype=np.int64)
        heap_pos = np.full(n, -1, dtype=np.int64)
        heap_size = 0
        dist[source] = 0.0
        heap_dist[0] = 0.0
        heap_vertex[0] = source
        heap_pos[source] = 0
        heap_size = 1
        while heap_size > 0:
            u = heap_vertex[0]
            du = heap_dist[0]
            heap_size -= 1
            if heap_size > 0:
                heap_dist[0] = heap_dist[heap_size]
                heap_vertex[0] = heap_vertex[heap_size]
                heap_pos[heap_vertex[0]] = 0
                k = 0
                while True:
                    child = 2 * k + 1
                    if child >= heap_size:
                        break
                    if (
                        child + 1 < heap_size
                        and heap_dist[child + 1] < heap_dist[child]
                    ):
                        child += 1
                    if heap_dist[k] <= heap_dist[child]:
                        break
                    heap_dist[k], heap_dist[child] = heap_dist[child], heap_dist[k]
                    heap_vertex[k], heap_vertex[child] = (
                        heap_vertex[child],
                        heap_vertex[k],
                    )
                    heap_pos[heap_vertex[k]] = k
                    heap_pos[heap_vertex[child]] = child
                    k = child
            heap_pos[u] = -2
            j = indptr[u]
            while j < indptr[u + 1]:
                v = indices[j]
                alt = du + weights[j]
                if alt < dist[v]:
                    dist[v] = alt
                    pos_v = heap_pos[v]
                    if pos_v == -2:
                        heap_dist[heap_size] = alt
                        heap_vertex[heap_size] = v
                        heap_pos[v] = heap_size
                        heap_size += 1
                        k = heap_size - 1
                        while k > 0:
                            parent = (k - 1) // 2
                            if heap_dist[parent] <= heap_dist[k]:
                                break
                            heap_dist[parent], heap_dist[k] = (
                                heap_dist[k],
                                heap_dist[parent],
                            )
                            heap_vertex[parent], heap_vertex[k] = (
                                heap_vertex[k],
                                heap_vertex[parent],
                            )
                            heap_pos[heap_vertex[parent]] = parent
                            heap_pos[heap_vertex[k]] = k
                            k = parent
                    elif pos_v >= 0:
                        k = pos_v
                        heap_dist[k] = alt
                        while k > 0:
                            parent = (k - 1) // 2
                            if heap_dist[parent] <= heap_dist[k]:
                                break
                            heap_dist[parent], heap_dist[k] = (
                                heap_dist[k],
                                heap_dist[parent],
                            )
                            heap_vertex[parent], heap_vertex[k] = (
                                heap_vertex[k],
                                heap_vertex[parent],
                            )
                            heap_pos[heap_vertex[parent]] = parent
                            heap_pos[heap_vertex[k]] = k
                            k = parent
                    else:
                        heap_dist[heap_size] = alt
                        heap_vertex[heap_size] = v
                        heap_pos[v] = heap_size
                        heap_size += 1
                        k = heap_size - 1
                        while k > 0:
                            parent = (k - 1) // 2
                            if heap_dist[parent] <= heap_dist[k]:
                                break
                            heap_dist[parent], heap_dist[k] = (
                                heap_dist[k],
                                heap_dist[parent],
                            )
                            heap_vertex[parent], heap_vertex[k] = (
                                heap_vertex[k],
                                heap_vertex[parent],
                            )
                            heap_pos[heap_vertex[parent]] = parent
                            heap_pos[heap_vertex[k]] = k
                            k = parent
                j += 1
        return dist

    BFS_FORWARD = jit_bfs_forward_kernel
    DIJKSTRA = jit_dijkstra_kernel
    AVAILABLE = True
    return True


def is_available() -> bool:
    """Return True if numba is installed and kernels compiled."""
    return AVAILABLE


probe()


__all__ = ["AVAILABLE", "BFS_FORWARD", "DIJKSTRA", "NUMBA", "is_available", "probe"]