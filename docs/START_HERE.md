# Start here

Where you go next depends on what you want to do with `reachq`.

## I want to use the library

Read [Getting started](getting-started.md) for installation and a
minimal example. The canonical entry point is
`reachq.build_shortcut_set_for_reachability`.

If you prefer learning by example, read [Examples](examples.md)
for five end-to-end applications.

## I want to understand the algorithms

Read [Algorithms](algorithms.md) for what the construction is
doing. For the algorithmic content (two lemmas from the
parallel-reachability literature plus the contributions layered
on top of them), read [Paper](PAPER.md). For a shorter overview,
read [Why reachq](WHY.md).

## I want to extend the library

Read [CONTRIBUTING.md](https://github.com/sachncs/reachq/blob/master/CONTRIBUTING.md#adding-a-new-algorithm)
for the pattern. The shortest path from idea to pull request is:

1. Implement `reachq/research/<your_algo>.py` with a single public function.
2. Add an explicit `__all__` listing the public symbols.
3. Add 3+ tests in `tests/test_<your_algo>.py` (including one property-based test).
4. Document in `docs/<your_algo>.md` with: algorithm, complexity, references.

## I want to file a bug or ask a question

[Open a GitHub issue](https://github.com/sachncs/reachq/issues).
See [FAQ](faq.md) for common questions.