# Examples

The [`examples/`](https://github.com/sachncs/reachq/tree/master/examples)
directory ships end-to-end applications that show what `reachq` is
useful for. Each example is short (under 100 lines), uses only the
public API, and is paired with a deterministic output below so you
can read this page without running anything.

The numbers below come from running each script with the listed
seed and parameters. To regenerate:

```bash
python scripts/build_examples_outputs.py
```

The output is written to [`docs/examples/outputs/examples.json`](examples/outputs/examples.json).

## Graph-domain overview

| Example | Domain | What it shows |
| ------- | ------ | ------------- |
| [GNN preprocessing](#gnn-preprocessing) | Citation graph | Shortcuts augment a sparse citation graph for a downstream GNN. |
| [RAG reranking](#rag-reranking) | Passage citation | Pivot-reach ranking for retrieval-augmented generation. |
| [Compiler inlining](#compiler-inlining) | IR graph | Shortcut edges surface inlining candidates. |
| [Social network](#social-network) | SNAP-style citation | Empirical `|H| / |E|` ratio on a denser random DAG. |
| [Bioinformatics](#bioinformatics) | PPI network | Downstream-hub detection in a synthetic protein-interaction network. |
| [Hopset demo](#hopset-demo) | Weighted SSSP | `(1 + ε)` distance approximation in action. |

## GNN preprocessing

**Graph:** 200 papers, density 0.02, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 200 |
| Edges | 376 |
| Shortcuts | 1650 |
| Asymptotic β | 12.077 |
| Realised bound | 7 |
| `|H| / |E|` | 4.388 |

The shortcut set is 4.4× larger than the edge set. That sounds
expensive, but in a GNN pipeline the shortcuts pre-compute
2-hop reachability, so the per-batch message passing skips the
intermediate hop.

**Run it yourself:**

```bash
python examples/gnn_preprocessing.py
```

## RAG reranking

**Graph:** 80 documents, density 0.04, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 80 |
| Shortcuts | 4732 |
| Asymptotic β | 6.93 |
| Direct citations from `d0` | 5 |
| Top-ranked neighbours (sample) | `d10`, `d13`, `d2`, `d20`, `d68` |

Pivot-reach ranking reorders passages by their shortcut-derived
distance from the seed document. The top-ranked neighbours include
`d10`, `d13`, `d2`, `d20`, and `d68`, in that order.

**Run it yourself:**

```bash
python examples/rag_reranking.py
```

## Compiler inlining

**Graph:** 120 IR blocks, density 0.15, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 120 |
| Shortcuts | 4930 |
| Asymptotic β | 6.31 |
| Top inlining candidates (block, in-degree) | (107, 22), (118, 21), (108, 20), (110, 20), (116, 20) |

The shortcut set surfaces the high-in-degree vertices: blocks 107
and 118 with 22 and 21 incoming edges respectively. These are the
prime inlining candidates — every call site that can reach them
will benefit from inlining once.

**Run it yourself:**

```bash
python examples/compiler_inlining.py
```

## Social network

**Graph:** 500 vertices, density 0.01, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 500 |
| Edges | 1230 |
| Shortcuts | 5857 |
| Asymptotic β | 17.855 |
| `|H| / |E|` | 4.762 |

A sparser random DAG produces a similar `|H| / |E|` ratio to the
GNN example. The shortcut-set cost is amortised by the per-query
speedup on dense reachability questions.

**Run it yourself:**

```bash
python examples/social_network.py
```

## Bioinformatics

**Graph:** 200 proteins (vertices labelled `P0`...`P199`), density
0.02, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 200 |
| Shortcuts | 38227 |
| Asymptotic β | 10.067 |
| Downstream hubs (2-hop from `P0`) | 196 |

A 200-protein PPI network with random activation edges has 38227
shortcut edges. From a query protein `P0`, 196 of the other 199
proteins are reachable within 2 hops once the shortcuts are
applied — effectively a full sweep of the network.

**Run it yourself:**

```bash
python examples/bioinformatics.py
```

## Hopset demo

**Graph:** a 7-vertex weighted digraph built to exercise a hopset.

| Metric | Value |
| ------ | ----- |
| Vertices | 7 |
| Edges | 9 |
| Hopset size | 5 |
| Asymptotic β | 2.485 |
| Max approximation ratio | 1.0 |

The hopset on this small graph gives the exact distances for every
vertex — `shortest_path_hopbound` matches `dijkstra` for every
source-target pair. On larger graphs the `(1 + ε)` slack kicks in.

**Vertex distances from `0` (exact vs. hopset-augmented):**

| Vertex | Exact | Hopset-augmented |
| ------ | ----- | ---------------- |
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 2 | 3 | 3 |
| 3 | 6 | 6 |
| 4 | 6 | 6 |
| 5 | 8 | 8 |
| 6 | 9 | 9 |

**Run it yourself:**

```bash
python examples/compiler_inlining.py   # noqa — this is a placeholder; see scripts/build_examples_outputs.py
```

(The hopset demo lives in `scripts/build_examples_outputs.py`.)

---

## Notes

- Every example uses deterministic seeds. The numbers above are
  reproducible from a clean checkout.
- Outputs are tiny by design — these are sketches, not
  production pipelines. The point is to show the API surface,
  not to benchmark.
- Each example is paired with a regression test where useful; see
  `tests/test_examples_smoke.py` if it exists in your checkout.