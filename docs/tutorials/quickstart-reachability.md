# Quick start: reachability

This 5-minute tutorial shows you how to compute a shortcut set,
verify it preserves reachability, and answer reachability queries
faster than naive BFS.

## Goal

Build a shortcut set `H` for a dense digraph `G` such that
`R+(G ∪ H, v) == R+(G, v)` for every source vertex `v`.

## Setup

```bash
pip install -e ".[dev]"
```

## 1. Build a graph

```python
from reachq import Digraph
from reachq.generators import random_dag

g = random_dag(n=1000, edge_probability=0.1, random_seed=42)
print(f"Graph: {g.num_vertices()} vertices, {g.num_edges()} edges")
```

A random DAG with 1000 vertices and edge probability 0.1 has about
1000 × 999 / 2 × 0.1 = ~50000 edges, so the construction runs in
a few seconds.

## 2. Build a shortcut set

```python
from reachq.shortcut import build_shortcut_set_for_reachability

shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g,
    omega=3.0,
    random_seed=42,
)
print(f"|H|={len(shortcuts)}, β={beta:.2f}, realised={realised_bound}")
```

`beta` is the asymptotic target hop bound from Theorem 2.
`realised_bound` is the algorithm's actual guarantee — use this
in tests.

## 3. Verify soundness

```python
from reachq.invariants import assert_reachability_preserved
assert_reachability_preserved(g, shortcuts)
print("OK: reachability preserved for every source")
```

The invariant helper iterates every source vertex and compares
`R+(G, s)` against `R+(G ∪ H, s)`. A failure means the shortcut
set is unsound; in that case, raise an issue.

## 4. Query with shortcuts

```python
from reachq.reachability import bfs_reachability, parallel_bfs

src = g.vertices()[0]
direct = bfs_reachability(g, src)
augmented = parallel_bfs(g, src, shortcuts)
assert direct == augmented
print(f"Vertex {src} reaches {len(direct)} vertices in {len(shortcuts)} augmented edges")
```

`parallel_bfs` walks `G ∪ H` from `src`. On dense graphs the
shortcut edges collapse long paths into one hop, so per-query
latency drops from `O(n + m)` to `O(n + |H|)` — comparable
work, but each augmented edge is amortised across many queries.

## 5. Speed it up with parallel mode

```python
from reachq import RefinementConfig

refinement = RefinementConfig(parallel=True)
shortcuts, beta, _ = build_shortcut_set_for_reachability(
    g,
    omega=3.0,
    random_seed=42,
    refinement=refinement,
    parallel_workers=4,
)
```

When `refinement.parallel=True` and `parallel_workers > 1`, the
per-pivot BFS runs across a process pool with `spawn` start
method. The hopset path stays sequential because per-pivot SSSP
is GIL-bound in Python.

## What you learned

- `build_shortcut_set_for_reachability` returns `(shortcuts, β, realised_bound)`.
- `assert_reachability_preserved(g, H)` is the soundness check.
- `parallel_bfs(g, src, H)` answers reachability queries on `G ∪ H`.
- `parallel=True` + `parallel_workers > 1` dispatches per-pivot BFS.

## Next steps

- [Quick start: shortest paths](quickstart-shortest-paths.md) — the same workflow with hopsets and approximate Dijkstra.
- [Algorithms](../algorithms.md) — what the construction is doing.
- [Examples](../examples.md) — five end-to-end applications.