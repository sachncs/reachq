<p align="center">
  <a href="https://sachncs.github.io/reachq/"><img src="https://sachncs.github.io/reachq/assets/logo.svg" alt="reachq logo" width="120" /></a>
</p>

<h1 align="center">reachq</h1>

<p align="center"><strong>Graph reachability, queryable.</strong></p>

<p align="center">Parallel shortcut sets and hopsets for reachability and shortest paths in dense digraphs.</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue" alt="Python"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
  <a href="https://github.com/sachncs/reachq/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/sachncs/reachq/ci.yml?branch=master" alt="CI"></a>
  <a href="https://github.com/sachncs/reachq/actions/workflows/pages.yml"><img src="https://img.shields.io/github/actions/workflow/status/sachncs/reachq/pages.yml?branch=master&label=docs" alt="Docs"></a>
  <a href="https://codecov.io/gh/sachncs/reachq"><img src="https://codecov.io/gh/sachncs/reachq/graph/badge.svg" alt="Codecov"></a>
  <a href="https://github.com/sachncs/reachq/security/advisories/new"><img src="https://img.shields.io/badge/security-report%20privately-blueviolet" alt="Security"></a>
</p>

---

## What is reachq?

`reachq` is a pure-Python library that builds **shortcut sets** and **hopsets** for directed graphs. The two constructions let you answer reachability and shortest-path queries on dense digraphs faster than naïve BFS or Dijkstra.

You should use `reachq` when:

- You work with **dense directed graphs** and want parallel-reachability or approximate-shortest-path speedups.
- You need a **reproducible** implementation whose outputs are byte-stable across processes and machines.
- You want to **tinker**: every algorithm ships with a Python entry point, a typed config, and doctests you can run in 5 seconds.

You should look elsewhere when:

- You need a **full general-purpose graph library** (BFS, Dijkstra, SCC, etc.). Use `networkx` or `igraph` for the day-to-day work and call `reachq` only for the JLS shortcut-set or CFR hopset.
- You need true parallel speedup today. `reachq` ships sequential and process-pool paths; the JLS construction parallelises per-pivot BFS, but the CFR hopset path is sequential because per-pivot SSSP is GIL-bound in Python.

## What reachq is not

- **Not a PyPI package yet.** Install from source for now (instructions below). A first PyPI release is on the Roadmap.
- **Not a JIT compiler.** The wheel is pure Python. Cython/Rust/Numba kernels live under `reachq/accel/` as opt-in build targets.
- **Not a `(1+ε)`-approximation oracle.** `greedy_shortcut_set` is a vanilla greedy; the formal guarantee is research-stage.

## Where to start

```python
from reachq import RefinementConfig, Digraph
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.invariants import assert_reachability_preserved
from reachq.generators import random_dag

# Build a 1000-vertex random DAG.
g = random_dag(n=1000, edge_probability=0.1, random_seed=42)

# Build a shortcut set and disable a refinement if you want.
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
)

# Assert that adding the shortcuts preserves reachability for every source.
assert_reachability_preserved(g, shortcuts)

# Now queries are fast.
assert parallel_bfs(g, g.vertices()[0], shortcuts) == bfs_reachability(g, g.vertices()[0])
```

## When to use reachq

Use reachq when you want a Python library that:

- Computes shortcut sets for parallel reachability (Theorem 2 of the paper).
- Computes hopsets for approximate shortest paths (Theorem 4 of the paper).
- Ships with reproducible benchmarks and tests.

## Comparison

| Feature                                  | reachq | networkx | igraph |
| ---------------------------------------- | :----: | :------: | :----: |
| JLS shortcut set                         |   ✅   |    ❌    |   ❌   |
| CFR hopset                               |   ✅   |    ❌    |   ❌   |
| β-hopbound-preserving sparsification     |   ✅   |    ❌    |   ❌   |
| Streaming shortcut set                   |   🧪   |    ❌    |   ❌   |
| (1+ε) approximation                      |   🧪   |    ❌    |   ❌   |
| Full graph library                       |   ❌   |    ✅    |   ✅   |
| Reproducible benchmarks across machines  |   ✅   |   partial|   ❌   |

✅ = shipped, 🧪 = prototype in `reachq.research`, ❌ = not implemented.

---

## Installation

```bash
git clone https://github.com/sachncs/reachq
cd reachq
pip install -e ".[dev]"
```

**Requirements:** Python ≥ 3.10, `numpy` ≥ 1.21, `scipy` ≥ 1.10. The wheel is pure Python — no JIT, no native extensions.

---

## Quick start

Build a shortcut set, assert reachability is preserved for every source, and confirm a query runs against `G ∪ H`.

```python
from reachq import RefinementConfig, Digraph
from reachq.generators import random_dag
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.invariants import assert_reachability_preserved

g = random_dag(n=1000, edge_probability=0.1, random_seed=42)
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
)

# Invariant: shortcut set preserves reachability for every source.
assert_reachability_preserved(g, shortcuts)

# Equivalence: parallel_bfs over G ∪ H equals bfs_reachability over G
# for two distinct sources (insertion-order vertex 0 and a middle vertex).
sources = (g.vertices()[0], g.vertices()[len(g.vertices()) // 2])
for src in sources:
    assert parallel_bfs(g, src, shortcuts) == bfs_reachability(g, src)
```

Disable any refinement:

```python
from reachq import RefinementConfig

shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
    refinement=RefinementConfig(enable_tc_pruning=False, tight_tc_trigger=True),
)
```

Five end-to-end applications live in [`examples/`](examples/):

- `gnn_preprocessing.py` — citation graph → PyG `Data` object.
- `rag_reranking.py` — passage-citation graph → pivot-reach ranking.
- `compiler_inlining.py` — IR graph → inlining-candidate ranking.
- `social_network.py` — SNAP `cit-HepPh` → `|H|/|E|` ratio.
- `bioinformatics.py` — synthetic PPI → downstream-hub detection.

See [`docs/examples.md`](docs/examples.md) for rendered outputs and discussion of each.

---

## Algorithmic refinements

The nine toggles on `RefinementConfig` (a frozen dataclass). All default to on except `parallel`.

| Flag                    | Effect                                                                |
| ----------------------- | --------------------------------------------------------------------- |
| `adaptive_sampling`     | Adapt per-level sampling probability from observed part sizes.        |
| `label_compress`        | Store labels as `frozenset[int]` instead of `set[str]`.               |
| `skip_condense`         | Skip SCC condensation on DAG inputs.                                  |
| `hop_bounded_bfs`       | Use a hop-bounded BFS kernel in the pivot loop.                       |
| `degree_ordered_pivots` | Process pivots in ascending out-degree order.                         |
| `tight_tc_trigger`      | Tighten the TC-pruning trigger by work comparison.                    |
| `skip_trivial_part`     | Skip recursion when the partition is a single part.                   |
| `enable_tc_pruning`     | Enable TC-pruning (Theorem 2's improvement).                          |
| `parallel`              | When `True`, dispatch per-pivot BFS through a process pool when `parallel_workers > 1`. |

`parallel_workers` on `build_shortcut_set_for_reachability` is the process-pool size. The hopset path runs sequentially because the per-pivot workload is a SSSP (GIL-bound in Python). See [`docs/algorithms.md`](docs/algorithms.md) § "Refinement flags" and [`docs/migration_0_9.md`](docs/migration_0_9.md).

---

## Experimental / research API

The `reachq.research` namespace ships paper-experimental algorithms that are not part of the stability contract. They may change without a major-version bump.

```python
from reachq.research.approximation import greedy_shortcut_set          # vanilla greedy, no formal (1+ε) guarantee
from reachq.research.iterate import iterative_shortcut_set              # iterative refinement
from reachq.research.sparsify import sparsify_shortcut_set               # reach-bound-preserving (small graphs)
from reachq.research.sparsify_hop import sparsify_hop_bounded            # hop-bound-preserving
from reachq.research.streaming import StreamingShortcutSet               # streaming shortcut set (prototype)
```

Each submodule has its own docstring with the algorithm, complexity, and a pinned test. See [`docs/PAPER.md`](docs/PAPER.md) for the relationship to the cited work.

---

## Tests

```bash
pytest                  # run the full suite
pytest -m "not slow"    # skip the slow stress tests
pytest --cov=reachq     # with a coverage report
```

The lemma tests run 50 random seeds per invariant claim; a failure means the lemma does not hold empirically on the tested graph class. See [`docs/testing.md`](docs/testing.md) for the testing strategy.

---

## API summary

```python
from reachq import RefinementConfig, Digraph, WeightedDigraph

from reachq.shortcut import (
    build_shortcut_set_for_reachability,  # Theorem-2 wrapper
    jls_with_tc_pruning,                  # direct recursion
)

from reachq.hopset import (
    build_hopset_for_sssp,                # Theorem-4 wrapper
    cfr_with_truncsssp_pruning,           # direct recursion
)

from reachq.reachability import (
    bfs_reachability,
    parallel_bfs,
    strongly_connected_components,
    topological_sort,
)

from reachq.shortest_paths import (
    dijkstra,
    shortest_path_hopbound,
    truncated_dijkstra,
)

from reachq.closure import (
    TransitiveClosureBudgetError,
    transitive_closure,
    transitive_closure_brute_force,
)

from reachq.generators import (
    random_dag,
    weighted_random_dag,
    layered_dag,
    dense_graph,
    graph_with_sccs,
    path_graph,
    cycle_graph,
    grid_graph,
    petersen_graph,
    paley_graph,
    shrikhande_graph,
    hamming_graph,
)

from reachq.io import (
    dump,           # Digraph -> JSON
    load,           # JSON -> Digraph
    weighted_dump,
    weighted_load,
)
```

The full API reference is auto-generated from the docstrings in [`docs/reference.md`](docs/reference.md).

---

## Project structure

```
reachq/
├── reachq/                              # the Python package
│   ├── __init__.py                      # public API + __version__
│   ├── bfs.py                           # CSR BFS kernels
│   ├── cli.py                           # CLI entry point (python -m reachq.cli)
│   ├── closure.py                       # Boolean-semiring transitive closure
│   ├── config.py                        # RefinementConfig + logging + omega table
│   ├── csr.py                           # CSR pair builder
│   ├── errors.py                        # Reachq* error hierarchy
│   ├── generators.py                    # deterministic graph generators + SNAP loader
│   ├── graph.py                         # Digraph, WeightedDigraph
│   ├── hopset.py                        # CFR + TruncSSSP-Pruning (Theorem 4)
│   ├── invariants.py                    # theorem-oriented validators
│   ├── io.py                            # JSON serialisation
│   ├── io_arrow.py                      # Arrow IPC serialisation (pyarrow)
│   ├── io_networkx.py                   # NetworkX adapter
│   ├── proto.py                         # duck-typed Protocols
│   ├── prune.py                         # TC-pruning (extracted)
│   ├── reachability.py                  # BFS, SCC, topological sort
│   ├── research/                        # opt-in refinements (off-paper)
│   ├── accel/                           # experimental Cython / Numba / Rust kernels
│   ├── shortcut.py                      # JLS + TC-pruning (Theorem 2)
│   ├── shortest_paths.py                # Dijkstra, A*, truncated SSSP
│   ├── trace.py                         # context-manager tracing
│   └── work_depth.py                    # PRAM work/depth accounting
├── tests/                               # test suite
├── scripts/                             # CLI / benchmark / reproduction scripts
├── docs/                                # documentation source (mkdocs)
├── examples/                            # five end-to-end applications
├── benchmarks/                          # asv micro-benchmarks
├── notebooks/                           # exploratory Jupyter notebooks
├── pyproject.toml
├── mkdocs.yml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── README.md
└── LICENSE
```

The full module responsibility table lives in [`docs/architecture.md`](docs/architecture.md).

---

## Documentation

The full documentation site is built with MkDocs Material and deployed to GitHub Pages at [sachncs.github.io/reachq](https://sachncs.github.io/reachq/).

Build it locally:

```bash
pip install -e ".[dev]" mkdocs mkdocs-material
mkdocs serve             # preview at http://127.0.0.1:8000
mkdocs build --strict    # build into ./site/
```

Notable entry points:

- [`docs/START_HERE.md`](docs/START_HERE.md) — three routing paths (use / understand / extend).
- [`docs/getting-started.md`](docs/getting-started.md) — install + first construction.
- [`docs/algorithms.md`](docs/algorithms.md) — algorithm descriptions, parameter selection, `RefinementConfig` flags.
- [`docs/architecture.md`](docs/architecture.md) — module responsibilities + dependencies.
- [`docs/reference.md`](docs/reference.md) — full API reference (auto-generated).
- [`docs/limitations.md`](docs/limitations.md) — what is NOT implemented.
- [`docs/GLOSSARY.md`](docs/GLOSSARY.md) — terminology.
- [`docs/examples.md`](docs/examples.md) — rendered example outputs.

---

## Known limitations

See [`docs/limitations.md`](docs/limitations.md) for the consolidated list. The short version:

- **Process parallelism** is real for the JLS shortcut-set construction when `refinement.parallel=True` and `parallel_workers > 1`. The hopset construction runs sequentially because the per-pivot workload is a SSSP (GIL-bound in Python).
- **No JIT, no native extensions.** Pure-Python wheel; the experimental Cython / Rust / Numba kernels in `reachq/accel/` are not built or shipped by default.
- **No formal `(1+ε)` approximation.** `greedy_shortcut_set` is a vanilla greedy.
- **No amortised streaming bound.** `StreamingShortcutSet` is a prototype; the O(log² n) per-insertion bound is not implemented.
- **`web-Google` (n=875k) is out of reach** for single-process Python.
- **Exact transitive closure** is inherently output-quadratic; the Boolean-semiring core respects an explicit `max_pairs` budget and raises `TransitiveClosureBudgetError` when exceeded.

---

## Roadmap

### Planned

- [ ] Cython port of the per-pivot BFS inner loop (for web-Google-scale inputs) — scaffolding exists under `reachq/accel/` but is not built or shipped (see [`docs/accel.md`](docs/accel.md)).
- [ ] Publish the first reachq release to PyPI.
- [ ] Build a `blis`/`mkl`-agnostic byte-stable hopset output (see #33).

### Done in v0.9.0

- [x] Cross-process byte-stability for the JLS shortcut-set construction (under `PYTHONHASHSEED` sweep).
- [x] Boolean-semiring transitive closure with an explicit `max_pairs` budget.
- [x] Per-pivot BFS dispatch through a process pool when `parallel=True`.
- [x] Insertion-order vertex indexing across `Digraph` / `WeightedDigraph` / CSR.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For research questions, see [`docs/PAPER.md`](docs/PAPER.md) for what has been proved and what is empirical.

## Citation

```bibtex
@article{ashvinkumar2026parallel,
  title={Parallel Reachability and Shortest Paths on Non-sparse Digraphs:
         Near-linear Work and Sub-square-root Depth},
  author={Ashvinkumar, Vikrant and Bernstein, Aaron and
          Probst Gutenberg, Maximilian and Saranurak, Thatchaphol},
  journal={arXiv preprint arXiv:2605.03892},
  year={2026}
}
```

For the refinements in this implementation:

```bibtex
@misc{reachq2026refinements,
  title={Algorithmic refinements for parallel reachability:
         tightened TC-pruning and hop-bounded pivot BFS},
  author={reachq contributors},
  year={2026},
  howpublished={\url{https://github.com/sachncs/reachq}}
}
```

## License

[MIT](LICENSE) © 2026 Sachin