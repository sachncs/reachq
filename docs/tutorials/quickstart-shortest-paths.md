# Quick start: shortest paths

This 5-minute tutorial shows you how to build a `(β, ε)` hopset,
verify the `(1 + ε)` approximation, and answer shortest-path
queries in fewer hops than Dijkstra.

## Goal

Build a hopset `H` for a weighted digraph `G` such that
`dist_H(s, v) ≤ (1 + ε) * dist_G(s, v)` for every reachable
target `v`, in at most `β` hops.

## Setup

```bash
pip install -e ".[dev]"
```

## 1. Build a weighted graph

```python
from reachq import WeightedDigraph

g = WeightedDigraph()
for u, v, w in [
    (0, 1, 1),
    (1, 2, 2),
    (0, 2, 10),
    (2, 3, 3),
    (3, 4, 1),
    (0, 4, 12),
]:
    g.add_edge(u, v, w)
print(f"Graph: {g.num_vertices()} vertices, {g.num_edges()} edges")
```

## 2. Build a hopset

```python
from reachq.hopset import build_hopset_for_sssp

hopset, beta = build_hopset_for_sssp(
    g,
    epsilon=0.1,
    random_seed=42,
)
print(f"|H|={len(hopset)}, β={beta:.3f}")
```

`β` is the asymptotic target hop bound from Theorem 4. The
returned `hopset` is a dict of `(u, v) -> weight` triples.

## 3. Verify the (1 + ε) approximation

```python
from reachq.invariants import assert_distance_approximation

ratios = assert_distance_approximation(
    g,
    hopset,
    source=0,
    epsilon=0.1,
    max_hops=100,
)
print(f"max ratio: {max(ratios.values()):.4f}  (must be ≤ 1.1)")
```

The invariant helper computes exact Dijkstra distances and
hop-bounded SSSP distances, then asserts that every reachable
target's ratio is at most `1 + ε` (within numerical tolerance).

## 4. Query with the hopset

```python
from reachq.shortest_paths import dijkstra, shortest_path_hopbound

exact = dijkstra(g, 0)
approx = shortest_path_hopbound(g, hopset, 0, max_hops=100)

for v in g.vertices():
    e, a = exact.get(v, float("inf")), approx.get(v, float("inf"))
    if e != float("inf"):
        print(f"  {v}: exact={e}, approx={a}, ratio={a / e:.3f}")
```

The hopset-augmented distances are exact on small graphs and
within `(1 + ε)` on large ones.

## 5. Cross-machine reproducibility

```python
# Pass an explicit omega for byte-stable output across BLAS vendors.
hopset, beta = build_hopset_for_sssp(
    g,
    epsilon=0.1,
    random_seed=42,
    omega=3.0,  # disable BLAS-aware shortcut
)
```

Without `omega=3.0`, the construction reads the running BLAS
vendor and uses `omega=2.5` for OpenBLAS/MKL/Accelerate/BLIS and
`omega=3.0` otherwise. The hopset differs between the two. Pass
an explicit `omega` if you need byte-stable output across machines.

## What you learned

- `build_hopset_for_sssp` returns `(hopset, β)`.
- `assert_distance_approximation` is the `(1 + ε)` check.
- `shortest_path_hopbound(g, hopset, src, max_hops)` answers queries.
- `omega` controls BLAS-vendor sensitivity for cross-machine reproducibility.

## Next steps

- [Quick start: reachability](quickstart-reachability.md) — the same workflow with reachability shortcuts.
- [Algorithms](../algorithms.md) — what CFR is doing.
- [Examples](../examples.md) — five end-to-end applications.