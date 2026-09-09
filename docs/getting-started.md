# Getting started

This page walks you through installing `reachq` and running your
first construction. It takes about 5 minutes.

## Prerequisites

You need Python 3.10 or later and `pip`. No native build tools,
no JIT compiler, no system-level dependencies.

## Install from source

```bash
git clone https://github.com/sachncs/reachq
cd reachq
pip install -e ".[dev]"
```

The `.[dev]` extra pulls in `pytest`, `hypothesis`, `mypy`, and
`ruff`. A PyPI release is on the Roadmap; until then, install
from a clone.

## Verify the install

```bash
pytest
```

You should see 647 tests pass (or so) plus 1 expected failure and
2 deselected slow tests. If you see fewer than 600 tests, the
collection step failed — usually because `scipy` or `numpy` is
missing. Reinstall with `pip install -e ".[dev]"`.

## Build your first shortcut set

Open a Python REPL:

```python
from reachq import Digraph, RefinementConfig
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.invariants import assert_reachability_preserved
from reachq.generators import random_dag

# 1. Build a 1000-vertex random DAG.
g = random_dag(n=1000, edge_probability=0.1, random_seed=42)

# 2. Build a shortcut set; returns (shortcuts, β, realised_bound).
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
)

# 3. Soundness: shortcut set preserves reachability for every source.
assert_reachability_preserved(g, shortcuts)

# 4. Now reachability queries are fast.
sources = (g.vertices()[0], g.vertices()[len(g.vertices()) // 2])
for src in sources:
    assert parallel_bfs(g, src, shortcuts) == bfs_reachability(g, src)
```

If every line runs without raising, your install works.

## Build your first hopset

```python
from reachq import WeightedDigraph
from reachq.hopset import build_hopset_for_sssp
from reachq.shortest_paths import dijkstra, shortest_path_hopbound
from reachq.invariants import assert_distance_approximation

g = WeightedDigraph()
for u, v, w in [
    (0, 1, 1), (1, 2, 2), (0, 2, 10),
    (2, 3, 3), (3, 4, 1), (0, 4, 12),
]:
    g.add_edge(u, v, w)

hopset, beta = build_hopset_for_sssp(g, epsilon=0.1, random_seed=42)

# (1 + ε) approximation: every distance is within 10 % of Dijkstra's.
ratios = assert_distance_approximation(
    g, hopset, source=0, epsilon=0.1, max_hops=100,
)
print(f"max ratio: {max(ratios.values()):.3f}")
```

The hopset path runs sequentially because per-pivot SSSP is
GIL-bound in Python. The shortcut-set path supports process-pool
dispatch when `refinement.parallel=True` and
`parallel_workers > 1`.

## Where to go next

- [Examples](examples.md) — five end-to-end applications with rendered outputs.
- [Quick start: reachability](tutorials/quickstart-reachability.md) — reachability in depth.
- [Quick start: shortest paths](tutorials/quickstart-shortest-paths.md) — hopsets in depth.
- [Algorithms](algorithms.md) — what the construction is doing.
- [API reference](reference.md) — every public function.
- [Limitations](limitations.md) — what is not implemented.

## Troubleshooting

**`ModuleNotFoundError: No module named 'reachq'`**

The package is not installed. Run `pip install -e ".[dev]"` from
the repository root.

**`ImportError: pyarrow is required for Arrow serialisation`**

Install `pyarrow` directly with `pip install pyarrow`. The
`reachq[research]` extra does not include it.

**Tests fail with `RuntimeError: numpy / scipy version mismatch`**

`reachq` requires `numpy>=1.21` and `scipy>=1.10`. Upgrade with
`pip install --upgrade numpy scipy`.

**`NetworkX is required for NetworkX interop`**

Install `networkx` directly with `pip install networkx`. The
`reachq[research]` extra does include `networkx`, but only when
you install with `pip install reachq[research]` from PyPI; for
now, install it directly.

For more, see the [FAQ](faq.md) or open an [issue](https://github.com/sachncs/reachq/issues).