<p align="center">
  <a href="https://sachncs.github.io/reachq/"><img src="site/public/logo.svg" alt="reachq" width="360" /></a>
</p>

<p align="center"><strong>Graph reachability, queryable.</strong></p>

<p align="center">A pure-Python toolkit for building reachability shortcut sets and weighted hopsets on directed graphs.</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%E2%80%933.13-3776AB" alt="Python 3.10–3.13"></a>
  <a href="https://github.com/sachncs/reachq/actions/workflows/ci.yml"><img src="https://github.com/sachncs/reachq/actions/workflows/ci.yml/badge.svg?branch=master" alt="CI"></a>
  <a href="https://sachncs.github.io/reachq/"><img src="https://img.shields.io/badge/docs-online-4F46E5" alt="Documentation"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-14B8A6" alt="MIT License"></a>
</p>

## What reachq does

reachq adds algorithmic structure to directed graphs so repeated queries do not have to rediscover the same paths from scratch.

- **Shortcut sets for reachability:** add directed shortcuts and verify that reachability is preserved.
- **Hopsets for weighted shortest paths:** add weighted links that reduce path hops, with an explicit epsilon parameter.
- **Reproducible experiments:** deterministic graph generators, seeds, typed configuration, invariants, and benchmark tooling.

It is designed for dense directed-graph research and algorithmic prototyping. It is not a hosted graph database and it is not a replacement for NetworkX or igraph's general graph APIs.

## Project status

reachq is pre-1.0 and installs from source. The core library is pure Python with optional experimental acceleration code under reachq/accel/.

Parallelism is specific to the construction:

- the reachability shortcut-set path can dispatch per-pivot BFS work through a process pool;
- the hopset path is currently sequential because its per-pivot SSSP workload is GIL-bound in Python;
- research modules under reachq.research are experimental and outside the stability contract.

Read the [limitations](https://sachncs.github.io/reachq/limitations.html) before using it for production decisions.

## Installation

~~~bash
git clone https://github.com/sachncs/reachq.git
cd reachq
python -m pip install -e ".[dev]"
~~~

Requirements: Python 3.10–3.13, NumPy ≥ 1.21, and SciPy ≥ 1.10.

## Minimal example

Build a shortcut set, check its invariant, and run a query over the augmented graph:

~~~python
from reachq.generators import random_dag
from reachq.invariants import assert_reachability_preserved
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.shortcut import build_shortcut_set_for_reachability

graph = random_dag(
    n=1000,
    edge_probability=0.1,
    random_seed=42,
)

shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    graph,
    omega=3.0,
    random_seed=42,
)

assert_reachability_preserved(graph, shortcuts)

source = graph.vertices()[0]
assert parallel_bfs(graph, source, shortcuts) == bfs_reachability(graph, source)
~~~

For weighted shortest paths:

~~~python
from reachq.hopset import build_hopset_for_sssp
from reachq.shortest_paths import dijkstra, shortest_path_hopbound

hopset, beta = build_hopset_for_sssp(
    weighted_graph,
    epsilon=0.1,
    random_seed=42,
)

exact = dijkstra(weighted_graph, source=0)
approx = shortest_path_hopbound(weighted_graph, hopset, source=0, max_hops=100)
~~~

The hopset path exposes the approximation parameter; compare it with an exact baseline for the graph and workload you care about.

## Documentation

Use the [product page](https://sachncs.github.io/reachq/) for the project story, status, and entry points.

- [Install and first construction](https://sachncs.github.io/reachq/getting-started.html)
- [Reachability tutorial](https://sachncs.github.io/reachq/tutorials/quickstart-reachability/)
- [Shortest-path tutorial](https://sachncs.github.io/reachq/tutorials/quickstart-shortest-paths/)
- [Algorithms and refinements](https://sachncs.github.io/reachq/algorithms.html)
- [API reference](https://sachncs.github.io/reachq/reference.html)
- [Examples](https://sachncs.github.io/reachq/examples.html)
- [Benchmarks](https://sachncs.github.io/reachq/benchmarks.html)
- [Limitations](https://sachncs.github.io/reachq/limitations.html)

The documentation separates supported usage from research notes and historical material. Start with the [documentation home](https://sachncs.github.io/reachq/).

## Development

~~~bash
python -m pytest
python -m pytest -m "not slow"
python -m ruff check .
python -m mypy reachq
~~~

The public website is built from [site/](site/) with Astro. Documentation
source files live in [docs/](docs/) and remain readable in the repository.

## Research and citation

The constructions are informed by *Parallel Reachability and Shortest Paths on Non-sparse Digraphs* by Ashvinkumar, Bernstein, Probst Gutenberg, and Saranurak. See the [research and provenance notes](https://sachncs.github.io/reachq/INSPIRED_BY.html) for the relationship between the paper, the implementation, and experimental extensions.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. For security issues, use [SECURITY.md](SECURITY.md) rather than a public issue.

## License

[MIT](LICENSE) © 2026 Sachin
