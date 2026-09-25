# reachq

> **Graph reachability, queryable.**

reachq is a pure-Python library for adding reusable structure to directed graphs. It builds **shortcut sets** for exact reachability workflows and **hopsets** for weighted shortest-path workflows, so repeated queries do not have to rediscover the same paths from scratch.

## Project status

reachq is pre-1.0 and installs from source. The core library is actively developed, deterministic by default, and intended for dense directed-graph research and algorithmic prototyping.

It is not a hosted graph database or a general-purpose replacement for NetworkX or igraph. The research namespace and optional acceleration backends are experimental and outside the stability contract.

## Install

~~~bash
git clone https://github.com/sachncs/reachq.git
cd reachq
python -m pip install -e ".[dev]"
~~~

Requires Python 3.10–3.13, NumPy ≥ 1.21, and SciPy ≥ 1.10.

## Minimal working example

Build a reachability shortcut set, verify its invariant, and query the augmented graph:

~~~python
from reachq.generators import random_dag
from reachq.invariants import assert_reachability_preserved
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.shortcut import build_shortcut_set_for_reachability

graph = random_dag(n=1000, edge_probability=0.1, random_seed=42)
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    graph, omega=3.0, random_seed=42,
)

assert_reachability_preserved(graph, shortcuts)

source = graph.vertices()[0]
assert parallel_bfs(graph, source, shortcuts) == bfs_reachability(graph, source)
~~~

For weighted shortest paths, start with [the shortest-path tutorial](tutorials/quickstart-shortest-paths.md).

## Core capabilities

### Reachability shortcut sets

A shortcut set augments the original directed graph with carefully chosen edges. The supported invariant is exact reachability preservation: adding shortcuts should not change which vertices are reachable.

See [the reachability tutorial](tutorials/quickstart-reachability.md), [the algorithms guide](algorithms.md), and the [API reference](reference.md).

### Weighted shortest-path hopsets

A hopset adds weighted links that reduce the number of hops in a path. The epsilon parameter is explicit; compare the hop-bounded result with an exact Dijkstra baseline for the graph and workload you care about.

See [the shortest-path tutorial](tutorials/quickstart-shortest-paths.md), [the algorithms guide](algorithms.md), and the [API reference](reference.md).

## Guarantees and non-guarantees

Supported invariants and engineering properties:

- shortcut-set workflows expose reachability-preservation checks;
- random seeds and typed configuration make runs reproducible;
- the reachability construction can optionally dispatch per-pivot BFS work through a process pool;
- benchmark and test inputs can record graph size, parameters, construction time, query time, and output sizes.

Do not infer:

- a universal practical speedup from beta or hopbound alone;
- true parallel speedup for every construction;
- a formal approximation guarantee for experimental greedy routines;
- production readiness for research modules or optional acceleration backends.

## Limitations

- The package is not published to PyPI yet.
- The hopset path is currently sequential because its per-pivot SSSP workload is GIL-bound in Python.
- The wheel is pure Python; Cython, Numba, and Rust code under \`reachq/accel/\` is opt-in and not shipped by default.
- \`reachq.research\` contains experimental algorithms that may change without a major-version bump.
- Exact transitive closure is output-quadratic and guarded by an explicit pair budget.

See the full [limitations page](limitations.md) before adopting reachq for production decisions.

## Performance and benchmarks

There is no single representative speedup number. A useful benchmark record includes:

- reachq version and commit;
- Python version, operating system, and CPU;
- graph source/type, vertex count n, edge count m, density, and random seed;
- algorithm parameters such as omega, epsilon, beta, and hopbound;
- construction time, query time, memory, shortcut/hopset size, and approximation error.

The [benchmark guide](benchmarks.md) separates theoretical bounds, microbenchmarks, and end-to-end measurements.

## Documentation map

- [Installation and first construction](getting-started.md)
- [Reachability tutorial](tutorials/quickstart-reachability.md)
- [Shortest-path tutorial](tutorials/quickstart-shortest-paths.md)
- [Algorithms and refinements](algorithms.md)
- [API reference](reference.md)
- [Examples](examples.md)
- [Architecture](architecture.md)
- [Benchmarks](benchmarks.md)
- [Testing](testing.md)
- [Limitations](limitations.md)
- [Glossary](GLOSSARY.md)

Research provenance and historical material live under [Research](INSPIRED_BY.md) and the repository archive; they do not redefine the supported API.

## Research and contribution

The constructions are informed by *Parallel Reachability and Shortest Paths on Non-sparse Digraphs* by Ashvinkumar, Bernstein, Probst Gutenberg, and Saranurak. See [the provenance notes](INSPIRED_BY.md) for the relationship between the paper, this implementation, and experimental extensions.

To contribute, read [CONTRIBUTING.md](https://github.com/sachncs/reachq/blob/master/CONTRIBUTING.md). Report security issues through [SECURITY.md](https://github.com/sachncs/reachq/blob/master/SECURITY.md).

## License

MIT. See the [LICENSE](https://github.com/sachncs/reachq/blob/master/LICENSE) file.
