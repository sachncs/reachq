# Testing

This page explains the test strategy, what the lemma tests cover,
and how to run subsets of the suite.

## Quick reference

```bash
pytest                  # the full suite
pytest -m "not slow"    # skip slow stress tests
pytest --cov=reachq     # with a coverage report
pytest -k "shortcut"    # run every test whose name contains "shortcut"
```

The default `pytest` invocation (no markers) runs everything.

## Markers

The project uses two markers:

- `slow` — long-running stress tests. Skip with `pytest -m "not slow"`.
- `benchmark` — tests that use `pytest-benchmark`. Run with
  `pytest -m benchmark`.

## Suite layout

The test directory mirrors the package layout:

```
tests/
├── test_shortcut_parallel.py        # parallel dispatch
├── test_shortcut_set_basic.py       # shortcut-set wrapper end-to-end
├── test_shortcut_set_hopbound.py    # hopbound invariants
├── test_shortcut_set_pivots.py      # pivot sampling
├── test_shortcut_set_recursion.py   # JLS recursion termination
├── test_layered_dag_shortcut_set.py # layered-DAG specialisation
├── test_reachability_through_shortcuts.py  # shortcut-augmented BFS
├── test_hopset.py                   # CFR / TruncSSSP
├── test_hopset_soundness.py         # (1+ε) approximation
├── test_invariants.py               # invariant helpers
├── test_invariants_algebraic.py     # algebraic identities
├── test_regression_invariants.py    # v0.9.0 regression
├── test_graph.py                    # Digraph / WeightedDigraph
├── test_generators.py               # graph generators
├── test_blas_omega.py               # BLAS vendor detection
├── test_docstring_no_doctest_collision.py  # guard against O(...)-tokens
├── test_work_depth.py               # work-depth accounting
├── test_*.py                        # ... see the directory for the full list
├── research/                        # tests for reachq.research
├── cli/                             # CLI entry-point tests
├── accel/                           # Cython / Numba / Rust tests
└── integration/                     # cross-module tests
```

## Property-based tests

The suite uses [Hypothesis](https://hypothesis.readthedocs.io/)
to exercise the algorithms on randomly-generated graphs. Look for
`@given(...)` and `@settings(...)` decorators in `tests/`. A
typical test pins an invariant (for example, that the shortcut
set preserves reachability) and lets Hypothesis generate many
random graphs to look for counterexamples.

If Hypothesis finds a counterexample it adds a file to
`.hypothesis/examples/` and prints a `git apply ...` command.
Apply the patch to add the failing input as a regression test.

## Lemma tests

The `tests/test_*_lemma.py` files exercise theorem statements
empirically. For example:

- `tests/test_shortcut_set_lemma.py` pins Theorem 2's
  `|H| ≤ O~(n * ρ²)` bound by running the construction on
  randomised inputs and asserting `|H| / (n * ρ²)` is bounded.
- `tests/test_hopset_weight_accuracy.py` pins Theorem 4's
  exact-weight property by asserting that every emitted
  hopset edge weight equals `dijkstra(graph, u)[v]` for the
  same input.

A failure means the lemma does not hold empirically on the
tested graph class. Open an issue with the failure trace.

## Doctests

`pyproject.toml` enables pytest's `--doctest-modules` flag,
which runs every module docstring through Python's doctest
parser. The parser is greedy: any line that looks like a
Python expression (for example `O(n^2)`, `n*rho`, `O(beta)`)
is attempted, and expressions that fail to evaluate break the
collection of an entire test file.

`tests/test_docstring_no_doctest_collision.py` greps every
docstring in `reachq/` for collision-prone patterns and fails
if any are found. When you document complexity in a docstring,
choose one of:

- Write the symbol in prose: "quadratic", "linear in n", "cubic in the edge count".
- Use a backtick-quoted form: `` `O(n^2)` ``.
- Use a different symbol: ``Theta(n^2)``, ``Big-O(n^2)``, ``n^2``.

## Writing new tests

- Use `pytest.mark.slow` for any test that takes more than ~1
  second on a developer laptop.
- Use `pytest.fixture` for shared graph construction.
- Add `random_seed` to any test that constructs randomised
  graphs; reproducibility is the point.
- Assert against `realised_bound`, not the asymptotic `beta`.
  The asymptotic bound is loose; the realised bound is what
  the algorithm actually guarantees.

## Continuous integration

CI runs `pytest --cov=reachq` on Ubuntu, macOS, and Windows
with Python 3.10, 3.11, 3.12, and 3.13. Coverage is uploaded
to Codecov on `ubuntu-latest × python 3.12`.

The full coverage matrix is in `.github/workflows/ci.yml`.