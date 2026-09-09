# Frequently asked questions

## General

### What is `reachq`?

`reachq` is a Python library that builds shortcut sets and hopsets
for directed graphs. The constructions come from the paper
*Parallel Reachability and Shortest Paths on Non-sparse Digraphs:
Near-linear Work and Sub-square-root Depth* by Ashvinkumar,
Bernstein, Probst Gutenberg, and Saranurak (2026).

### What does `reachq` implement?

- Two graph classes: `Digraph` and `WeightedDigraph` with insertion-order vertex indexing.
- Shortcut-set construction (Theorem 2) with TC-pruning.
- Hopset construction (Theorem 4) with TruncSSSP-pruning.
- Graph primitives: BFS, reverse BFS, Dijkstra, A*, SCC, topological sort.
- Boolean-semiring transitive closure with an explicit `max_pairs` budget.
- Deterministic graph generators and a SNAP loader.
- JSON, Arrow, and NetworkX serialisation.
- Work-depth accounting for the simulated PRAM model.
- Invariant checkers that exercise the theorems empirically.

### What is NOT implemented?

See [Limitations](limitations.md) for the consolidated list. The
short version:

- True PRAM parallelism. Python does not support the PRAM model.
- A JIT compiler or native C/Rust kernels in the default wheel.
- A formal `(1+ε)`-approximation oracle (`greedy_shortcut_set` is a vanilla greedy).
- An amortised `O(log² n)` streaming bound (`StreamingShortcutSet` is a prototype).
- Real-world scale (web-Google, n ≈ 875k) on a single Python process.

### What Python versions does `reachq` support?

Python 3.10 through 3.13. The package pins `requires-python = ">=3.10"`
in `pyproject.toml`.

## Installation

### Do I need numpy or scipy?

Yes. Both are required dependencies. numpy drives the transitive
closure; scipy drives sparse matrix operations.

### Do I need pyarrow or networkx?

Only for the Arrow and NetworkX adapters. Both are optional and
are not auto-installed. Install them directly with
`pip install pyarrow` or `pip install networkx`.

### Why is `pip install reachq` not working?

A PyPI release is on the Roadmap. Until it ships, install from
source: `pip install -e ".[dev]"` from a fresh clone.

## Usage

### How do I build a shortcut set?

```python
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.generators import random_dag

g = random_dag(n=1000, edge_probability=0.1, random_seed=42)
shortcuts, beta, realised_bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
)
```

### How do I verify the shortcut set is correct?

```python
from reachq.invariants import assert_reachability_preserved
assert_reachability_preserved(g, shortcuts)
```

This iterates every source and asserts `R+(G, s) == R+(G ∪ H, s)`.
A failure means the shortcut set is unsound.

### How do I get byte-stable output across machines?

Pass an explicit `omega` to `build_hopset_for_sssp`:

```python
hopset, beta = build_hopset_for_sssp(
    g, epsilon=0.1, random_seed=42, omega=3.0,
)
```

The default `omega=None` reads the running BLAS vendor and uses
`omega=2.5` for OpenBLAS/MKL/Accelerate/BLIS, `omega=3.0`
otherwise. The hopset differs between the two. Pass `omega=3.0`
to disable the BLAS-aware shortcut.

## Performance

### Can I speed up the construction with parallelism?

Yes, for the shortcut-set path. Pass `parallel_workers > 1` and
`refinement.parallel=True`:

```python
from reachq import RefinementConfig

shortcuts, beta, _ = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42,
    refinement=RefinementConfig(parallel=True),
    parallel_workers=4,
)
```

The hopset path stays sequential because per-pivot SSSP is
GIL-bound in Python.

### My construction runs out of memory on large graphs. What now?

`reachq` is honest about its scaling limits. The
[Limitations](limitations.md) page documents where the wall-clock
and memory ceilings sit. Strategies that help:

- Reduce graph size before construction.
- Use sparse graph generators (`random_dag`, `path_graph`).
- Monitor memory with `psutil` or `tracemalloc`.
- Move the construction to a machine with more RAM.

### Floating-point precision issues?

Shortest-path algorithms use floats for distances. For critical
applications:

- Use integer weights where possible.
- Set tolerances explicitly in distance comparisons.
- Verify results with the brute-force oracle (`dijkstra`).

## Contributing

See [CONTRIBUTING.md](https://github.com/sachncs/reachq/blob/master/CONTRIBUTING.md) for:

- Setting up the development environment.
- Branch naming and commit conventions.
- The pull-request process.
- Coding standards.
- Running tests.

## Getting help

- [Open an issue](https://github.com/sachncs/reachq/issues).
- Read the [API reference](reference.md).
- Read the [Algorithms](algorithms.md) page for theoretical background.
- Read [Examples](examples.md) for end-to-end applications.