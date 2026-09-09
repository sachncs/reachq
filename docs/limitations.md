# Limitations

This page lists what `reachq` 0.9.0 does not do. Pair it with
[`docs/algorithms.md`](algorithms.md) for what each entry means.

## What is NOT supported

| Capability | Status | Where to look |
| --- | --- | --- |
| Parallel hopset construction | Not implemented. CFR per-pivot SSSP is GIL-bound in Python; the hopset path runs sequentially. JLS dispatches per-pivot BFS through a process pool. | [`docs/migration_0_9.md`](migration_0_9.md), [`docs/algorithms.md`](algorithms.md) |
| JIT / native C extensions | Not implemented. The wheel and sdist ship only pure-Python fallbacks. | [`docs/accel.md`](accel.md) |
| Distributed execution (Ray, Dask, GraphBLAS) | Stub only. | [`reachq/accel/`](https://github.com/sachncs/reachq/tree/master/reachq/accel) |
| GPU acceleration | Not implemented. | This page. |
| `(1+ε)`-approximation for the minimum shortcut set | Not implemented. `greedy_shortcut_set` is a vanilla greedy. | [`docs/approximation_analysis.md`](approximation_analysis.md) |
| Amortised O(log² n) streaming shortcut set | Not implemented. | [`docs/streaming_proof.md`](streaming_proof.md) |
| Backward-compatibility shims | None. v0.9.0 is a hard cut from v0.8.0. | [`docs/migration_0_9.md`](migration_0_9.md) |
| Real-world graph scale (web-Google, n ≈ 875k) | Memory is unblocked, but wall-clock is dominated by Python's per-edge overhead. | [`README.md`](https://github.com/sachncs/reachq/blob/master/README.md) |
| Pretrained / cached predictions | Not implemented. `omega` and `epsilon` are explicit caller-provided parameters with common defaults documented in the docstrings. | n/a |
| Reporting / visualisation beyond printed logs | Not implemented. The CLI prints results; there is no plotting, no dashboard, no HTML report. | [`reachq/cli.py`](https://github.com/sachncs/reachq/blob/master/reachq/cli.py) |

## What IS supported

The "supported" column below was cross-checked against
`reachq.__all__` on this commit. Every entry maps to a real,
importable symbol in the public API.

- Pure-Python JLS shortcut-set construction
  (`build_shortcut_set_for_reachability`).
- CFR + TruncSSSP-Pruning hopset construction
  (`build_hopset_for_sssp`).
- Boolean-semiring transitive closure (`transitive_closure`)
  with an explicit `max_pairs` budget and
  `TransitiveClosureBudgetError`.
- Insertion-order vertex indexing for cross-process
  reproducibility.
- Heap-tie-break correctness for arbitrarily hashable vertex
  types (`object()`, `frozenset`, custom).
- Per-invocation `BuildContext` so concurrent JLS builds cannot
  share mutable worker state.
- Adaptive sampling that actually scales the next-level
  probability.
- Property-based testing (`pytest` + `hypothesis`) including
  differential NetworkX oracles.
- JSON serialisation (`reachq.io.dump` / `load`).
- Arrow IPC serialisation (`reachq.io_arrow.dump_arrow` /
  `load_arrow`).
- NetworkX adapter (`reachq.io_networkx.to_networkx` /
  `from_networkx`).
- Documentation site (`mkdocs build --strict`).