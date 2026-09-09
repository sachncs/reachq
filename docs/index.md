# reachq

> Graph reachability, queryable.

`reachq` is a Python library for building **shortcut sets** and **hopsets**
on directed graphs. The constructions come from the paper *Parallel
Reachability and Shortest Paths on Non-sparse Digraphs* by Ashvinkumar,
Bernstein, Probst Gutenberg, and Saranurak (2026). The implementation is
pure Python, deterministic, and supports parallel dispatch when you opt in.

## What's here

| Section | Purpose |
| ------- | ------- |
| [Quick start](#quick-start) | First construction in 30 lines |
| [API reference](reference.md) | Every public function |
| [Examples](examples.md) | Five end-to-end applications with rendered outputs |
| [Algorithms](algorithms.md) | How the constructions work |
| [Architecture](architecture.md) | Per-module responsibility table |
| [Benchmarks](benchmarks.md) | asv micro-benchmarks |
| [Limitations](limitations.md) | What is not implemented |
| [Glossary](GLOSSARY.md) | Terminology |

## Quick start

Install from source for now (a PyPI release is on the Roadmap):

```bash
git clone https://github.com/sachncs/reachq
cd reachq
pip install -e ".[dev]"
```

### Build a shortcut set

```python
from reachq import Digraph, RefinementConfig
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.invariants import assert_reachability_preserved
from reachq.generators import random_dag

# A 1000-vertex random DAG.
g = random_dag(n=1000, edge_probability=0.1, random_seed=42)

# Build a shortcut set; returns (shortcuts, beta, realised_bound).
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
)

# Invariant: shortcut set preserves reachability for every source.
assert_reachability_preserved(g, shortcuts)

# Queries: parallel_bfs over G ∪ H equals bfs_reachability over G.
sources = (g.vertices()[0], g.vertices()[len(g.vertices()) // 2])
for src in sources:
    assert parallel_bfs(g, src, shortcuts) == bfs_reachability(g, src)
```

### Build a hopset

```python
from reachq import WeightedDigraph
from reachq.hopset import build_hopset_for_sssp
from reachq.shortest_paths import dijkstra, shortest_path_hopbound

g = WeightedDigraph()
for i, j, w in [(0, 1, 1), (1, 2, 2), (0, 2, 10)]:
    g.add_edge(i, j, w)

hopset, beta = build_hopset_for_sssp(g, epsilon=0.1, random_seed=42)

# Verify (1 + eps) approximation for a source.
original = dijkstra(g, 0)
approx = shortest_path_hopbound(g, hopset, 0, max_hops=100)
for v, exact in original.items():
    assert approx[v] <= (1 + 0.1) * exact + 1e-9
```

### Save and load

```python
from reachq.io import dump, load

text = dump(g)
h = load(text)
assert g.num_vertices() == h.num_vertices()
```

### Disable refinements

```python
from reachq import RefinementConfig

shortcuts, beta, _ = build_shortcut_set_for_reachability(
    g,
    omega=3.0,
    random_seed=42,
    refinement=RefinementConfig(enable_tc_pruning=False, tight_tc_trigger=True),
)
```

## Configuration

The `refinement` parameter is a :class:`~reachq.RefinementConfig` dataclass
of boolean toggles. All default to on except `parallel`. See
[Algorithms → Refinement flags](algorithms.md#refinement-flags) for the
full list and what each does.

```python
from reachq import RefinementConfig

cfg = RefinementConfig(
    adaptive_sampling=True,
    enable_tc_pruning=True,
    parallel=False,  # set True to dispatch per-pivot BFS across processes
)
```

## CLI

```bash
python -m reachq.cli --help
```

## Where to look next

- [Quick start](getting-started.md) — install + first construction in detail.
- [Algorithms](algorithms.md) — how the constructions work.
- [API reference](reference.md) — every public function, signature, and parameter.
- [Examples](examples.md) — five end-to-end applications with rendered outputs.
- [Limitations](limitations.md) — what is not implemented.

## Running tests

```bash
pytest                  # the full suite
pytest -m "not slow"    # skip the slow stress tests
pytest --cov=reachq     # with a coverage report
```

## License

MIT. See the [LICENSE](https://github.com/sachncs/reachq/blob/master/LICENSE) file.