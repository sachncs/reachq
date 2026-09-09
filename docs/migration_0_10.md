# Migration to v0.10.0 (DRAFT)

> **Status:** DRAFT — proposed, not implemented.
>
> This document describes a planned refactor for a future 0.10.0
> release. It is **not** the migration guide for the current
> release. If you are upgrading from v0.8.x, see
> [`docs/migration_0_9.md`](migration_0_9.md).

v0.10.0 will be a hard-cut refactor for clarity, correctness, and
performance. Every API change will be a breaking change; no compat
shims will be retained. None of the items below have shipped yet.
The test plan for v0.10.0 will land in
`tests/test_regression_invariants.py` at the same time as the
implementation.

## Proposed architecture changes

* `reachq.core.algorithm/` will become a subpackage and may be
  renamed; see issue tracker.
* `reachq.core.tc` may be renamed `reachq.closure`.
* `reachq.core.metrics` is unused by callers and may be deleted.
* `reachq.core.tuner` is unused by callers and may be deleted.
* `reachq.core.predictor` may be renamed `reachq.core.predict`.
* `reachq.core.backends` may be deleted.

## Proposed SSSP and reachability contracts

* Unreachable vertices remain *absent* from `dijkstra`,
  `truncated_dijkstra`, `astar`, `shortest_path_hopbound`, and
  `shortest_path_tree`.
* `shortest_path` will continue to return `UNREACHABLE` for an
  unreachable target.
* All heap tuples will continue to include a per-call monotonic
  counter.

## Proposed transitive-closure changes

* The hopset will be computed directly on the original weighted
  graph (already true in v0.9.0).
* `transitive_closure_matrix` was removed in v0.9.0; the v0.10
  migration recipe will reflect the final name.
* `TransitiveClosureBudgetError` behaviour: pass
  `budget_strict=False` to return a partial result.

## Proposed graph-model changes

* Insertion order remains the canonical vertex index.
* `WeightedDigraph.add_edge` continues to reject non-`int`,
  `bool`, `NaN`, `inf`, and negative weights.

## Proposed removal of compat shims

* The legacy `Flags = RefinementConfig` alias was removed in
  v0.9.0.
* `jls_shortcut_set`, `cfr_hopset` remain non-top-level exports.
* `compute_r_plus`, `compute_r_minus`, `compute_r_ball` are gone;
  use `bfs_reachability` and `reverse_bfs_reachability`.
* `paper_bound_const` may be renamed `upper_bound_paper(n, m)`.

## Proposed build / CLI changes

* `python -m reachq.cli` is the supported entry point
  (already true in v0.9.0).

## Source-breaking example

```python
# 0.8.x → 0.9.0 (current)
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.closure import transitive_closure

# 0.10.0 (proposed; identical to 0.9.0 once it ships)
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.closure import transitive_closure
```

See [`docs/migration_0_9.md`](migration_0_9.md) for the
already-shipped v0.9.0 migration and [the changelog on
GitHub](https://github.com/sachncs/reachq/blob/master/CHANGELOG.md)
for the full release history.