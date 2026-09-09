"""Internal helpers for :mod:`reachq.hopset`.

This module hosts the implementation details of the CFR hopset
construction. The leading-underscore module name signals "private"
to importers; the helpers inside use plain names so they are not
single-underscore-prefixed.

Only :mod:`reachq.hopset` imports from this module.
"""

from __future__ import annotations

import math
import random

from reachq.graph import WeightedDigraph
from reachq.shortest_paths import (
    compute_d_descendants,
    dijkstra,
    truncated_dijkstra,
)


def truncated_sssp(
    graph: WeightedDigraph,
    vertex_subset,
    max_distance: int,
    *,
    subgraph: WeightedDigraph | None = None,
) -> dict[tuple[object, object], int]:
    """All-pairs shortest paths within ``vertex_subset`` truncated at ``max_distance``.

    Args:
        graph: The input weighted digraph.
        vertex_subset: Iterable of vertices to seed the search from.
        max_distance: Hard distance cap for emitted edges.
        subgraph: Optional pre-built induced subgraph. When the caller
            already has the union of every ``vertex_subset`` it will
            pass, supply it here to skip a redundant reconstruction
            per call. The caller is responsible for keeping
            ``vertex_subset`` a subset of ``subgraph``'s vertices.
    """
    edges: dict[tuple[object, object], int] = {}
    if subgraph is None:
        subgraph = graph.induced_subgraph(set(vertex_subset))
    for u in vertex_subset:
        if u not in subgraph:
            continue
        dists = dijkstra(subgraph, u)
        for v, d in dists.items():
            if u != v and d <= max_distance:
                edges[(u, v)] = d
    return edges


def cfr_partition(
    graph: WeightedDigraph,
    vertices,
    pivots,
) -> list[set[object]]:
    """Partition ``vertices`` by their pivot-ancestor/descendant labels.

    Two vertices are in the same part iff they have identical sets
    of d-ancestors and d-descendants (modulo the current pivots).
    """
    anc_of: dict[object, set[object]] = {v: set() for v in vertices}
    des_of: dict[object, set[object]] = {v: set() for v in vertices}

    rev = graph.reversed()
    d = 1
    for pivot in pivots:
        d_ancestors = set(truncated_dijkstra(rev, pivot, d).keys())
        d_descendants = compute_d_descendants(graph, pivot, d)
        for v in d_ancestors:
            anc_of.setdefault(v, set()).add(pivot)
        for v in d_descendants:
            des_of.setdefault(v, set()).add(pivot)

    groups: dict[tuple, set[object]] = {}
    for v in vertices:
        key = (frozenset(anc_of.get(v, set())), frozenset(des_of.get(v, set())))
        groups.setdefault(key, set()).add(v)
    return list(groups.values())


__all__ = ["cfr_partition", "truncated_sssp"]