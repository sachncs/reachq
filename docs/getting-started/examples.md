# Examples

The [`examples/`](https://github.com/sachncs/reachq/tree/master/examples)
directory ships small, illustrative integration sketches. They show how a
reachq construction can be composed with a domain-shaped graph; they do not
establish a domain-specific quality or runtime benefit. Each example is short,
uses the public API, and is paired with deterministic output below.

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
| [Social network](#social-network) | Synthetic directed graph | Construction-size ratio on a small deterministic graph. |
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

The shortcut set is 4.4× larger than the edge set. This is a construction-size
observation for the supplied synthetic graph, not evidence of a GNN training
or inference improvement.

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

Pivot-reach ranking reorders passages by a shortcut-derived graph signal. The
listed neighbours are deterministic output for this synthetic input; no
retrieval-quality claim is implied.

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
possible candidates for further compiler analysis. The example does not run a
compiler or establish that inlining them improves generated code.

**Run it yourself:**

```bash
python examples/compiler_inlining.py
```

## Social network

**Graph:** 100 vertices, edge probability 0.05, random seed 42.

| Metric | Value |
| ------ | ----- |
| Vertices | 500 |
| Edges | 224 |
| Shortcuts | 915 |
| Asymptotic β | 8.17 |
| `|H| / |E|` | 4.08 |

A small synthetic directed graph produces a `|H| / |E|` ratio of 4.08 for
this seed. The ratio is a construction-size measurement only; query
amortisation and runtime need a separate workload benchmark.

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

A 200-protein synthetic interaction graph has 38227 shortcut edges. From a
query protein `P0`, 196 of the other 199 vertices are reachable within the
demonstration's two-hop query. This is a graph-algorithm example, not a claim
about biological connectivity.

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
python scripts/build_examples_outputs.py
```

(The hopset demo lives in `scripts/build_examples_outputs.py`.)

---

## Notes

- Every example uses deterministic seeds. The numbers above are
  reproducible from a clean checkout.
- Outputs are tiny by design — these are sketches, not
  production pipelines. The point is to show the API surface,
  not to benchmark.
- The scripts are illustrative and should be run with their documented seed
  before using their output in a benchmark or application decision.
