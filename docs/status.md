# Project status

`reachq` is a pre-1.0, source-first Python library for two focused graph
algorithm workflows:

- exact reachability shortcut sets on directed graphs;
- weighted hopsets and bounded-hop shortest-path queries.

## Supported

The maintained core is pure Python and covered by the test suite. It includes
directed and weighted graph containers, deterministic seeded constructions,
reachability and shortest-path queries, invariants, serialization helpers, and
the CLI smoke paths.

## Experimental

`reachq.research` and optional acceleration backends are available for
exploration. They are not part of the pre-1.0 stability contract.

## Release status

The current development snapshot is `0.9.0.dev0`. It is not a PyPI release and
has no release tag. Install from a source checkout until a real release artifact
is published.

The published documentation site is the user-facing source of truth for
onboarding and supported behavior. Research notes and historical reviews are
kept separately under `docs/research/` and `docs/archive/`.
