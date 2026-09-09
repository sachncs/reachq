# API reference

This page is generated from the docstrings in `reachq/`. It is the
authoritative reference: every signature, parameter, return type,
and exception is read directly from the source. To regenerate:

```bash
pip install -e ".[dev]" mkdocs mkdocs-material mkdocstrings
mkdocs build --strict
```

If a public function is missing from this page, it is either not
in `reachq.__all__` (and therefore not part of the stability
contract) or the mkdocstrings directive needs updating. Open an
issue if you find either.

## Graph primitives

::: reachq.graph.Digraph
    options:
      show_root_heading: true
      show_symbol_class_heading: true
      show_symbol_class_toc: true
      members:
        - add_vertex
        - add_edge
        - add_edges
        - remove_edge
        - has_vertex
        - vertices
        - iter_vertices
        - num_vertices
        - num_edges
        - index_of
        - vertex_at
        - out_degree
        - in_degree
        - degree_out
        - degree_in
        - reverse
        - reversed
        - induced_subgraph
        - edges
        - iter_edges
        - out_edges
        - in_edges
        - is_dag
        - is_acyclic
        - has_cycle
        - copy
        - restore_indices

::: reachq.graph.WeightedDigraph
    options:
      show_root_heading: true
      show_symbol_class_heading: true
      show_symbol_class_toc: true

## Shortcut-set construction

::: reachq.shortcut.build_shortcut_set_for_reachability
    options:
      show_root_heading: true
      separate_signature: true

::: reachq.shortcut.jls_with_tc_pruning
    options:
      show_root_heading: true
      separate_signature: true

## Hopset construction

::: reachq.hopset.build_hopset_for_sssp
    options:
      show_root_heading: true
      separate_signature: true

::: reachq.hopset.cfr_with_truncsssp_pruning
    options:
      show_root_heading: true
      separate_signature: true

## Reachability and graph algorithms

::: reachq.reachability.bfs_reachability
    options:
      show_root_heading: true

::: reachq.reachability.reverse_bfs_reachability
    options:
      show_root_heading: true

::: reachq.reachability.parallel_bfs
    options:
      show_root_heading: true

::: reachq.reachability.strongly_connected_components
    options:
      show_root_heading: true

::: reachq.reachability.topological_sort
    options:
      show_root_heading: true

::: reachq.reachability.compute_ancestors
    options:
      show_root_heading: true

::: reachq.reachability.compute_descendants
    options:
      show_root_heading: true

::: reachq.reachability.compute_bridges
    options:
      show_root_heading: true

## Shortest paths

::: reachq.shortest_paths.dijkstra
    options:
      show_root_heading: true

::: reachq.shortest_paths.truncated_dijkstra
    options:
      show_root_heading: true

::: reachq.shortest_paths.shortest_path
    options:
      show_root_heading: true

::: reachq.shortest_paths.shortest_path_tree
    options:
      show_root_heading: true

::: reachq.shortest_paths.shortest_path_hopbound
    options:
      show_root_heading: true

::: reachq.shortest_paths.astar
    options:
      show_root_heading: true

::: reachq.shortest_paths.compute_d_ancestors
    options:
      show_root_heading: true

::: reachq.shortest_paths.compute_d_descendants
    options:
      show_root_heading: true

## CSR BFS kernels

::: reachq.bfs.csr_reachable_forward
    options:
      show_root_heading: true

::: reachq.bfs.csr_reachable_backward
    options:
      show_root_heading: true

::: reachq.bfs.csr_bfs_layered
    options:
      show_root_heading: true

## Transitive closure

::: reachq.closure.transitive_closure
    options:
      show_root_heading: true

::: reachq.closure.transitive_closure_brute_force
    options:
      show_root_heading: true

::: reachq.closure.transitive_closure_on_subset
    options:
      show_root_heading: true

::: reachq.closure.TransitiveClosureBudgetError
    options:
      show_root_heading: true

## TC-pruning internals

::: reachq.prune.compute_tc_pruning_threshold
    options:
      show_root_heading: true

::: reachq.prune.apply_tc_pruning
    options:
      show_root_heading: true

## Graph generators

::: reachq.generators.random_dag
    options:
      show_root_heading: true

::: reachq.generators.erdos_renyi_digraph
    options:
      show_root_heading: true

::: reachq.generators.weighted_random_dag
    options:
      show_root_heading: true

::: reachq.generators.weighted_dense_graph
    options:
      show_root_heading: true

::: reachq.generators.weighted_path_graph
    options:
      show_root_heading: true

::: reachq.generators.dense_graph
    options:
      show_root_heading: true

::: reachq.generators.layered_dag
    options:
      show_root_heading: true

::: reachq.generators.graph_with_sccs
    options:
      show_root_heading: true

::: reachq.generators.path_graph
    options:
      show_root_heading: true

::: reachq.generators.cycle_graph
    options:
      show_root_heading: true

::: reachq.generators.grid_graph
    options:
      show_root_heading: true

::: reachq.generators.petersen_graph
    options:
      show_root_heading: true

::: reachq.generators.paley_graph
    options:
      show_root_heading: true

::: reachq.generators.shrikhande_graph
    options:
      show_root_heading: true

::: reachq.generators.hamming_graph
    options:
      show_root_heading: true

## Configuration, errors, logging

::: reachq.config.RefinementConfig
    options:
      show_root_heading: true
      show_symbol_class_toc: true
      members:
        - from_dict

::: reachq.config.configure_logging
    options:
      show_root_heading: true

::: reachq.config.get_logger
    options:
      show_root_heading: true

::: reachq.config.runtime_omega
    options:
      show_root_heading: true

::: reachq.errors.ReachqError
    options:
      show_root_heading: true

::: reachq.errors.ReachqValueError
    options:
      show_root_heading: true

::: reachq.errors.ReachqTypeError
    options:
      show_root_heading: true

::: reachq.errors.ReachqGraphError
    options:
      show_root_heading: true

## Work-depth accounting

::: reachq.work_depth.WorkDepthAccountant
    options:
      show_root_heading: true
      show_symbol_class_toc: true

## Serialisation

::: reachq.io.dump
    options:
      show_root_heading: true

::: reachq.io.load
    options:
      show_root_heading: true

::: reachq.io.weighted_dump
    options:
      show_root_heading: true

::: reachq.io.weighted_load
    options:
      show_root_heading: true

::: reachq.io.digraph_to_dict
    options:
      show_root_heading: true

::: reachq.io.digraph_from_dict
    options:
      show_root_heading: true

::: reachq.io_arrow.dump_arrow
    options:
      show_root_heading: true

::: reachq.io_arrow.load_arrow
    options:
      show_root_heading: true

::: reachq.io_networkx.to_networkx
    options:
      show_root_heading: true

::: reachq.io_networkx.from_networkx
    options:
      show_root_heading: true

## Invariants

::: reachq.invariants.assert_reachability_preserved
    options:
      show_root_heading: true

::: reachq.invariants.assert_hopbound
    options:
      show_root_heading: true

::: reachq.invariants.assert_scc_shortcuts_form_cliques
    options:
      show_root_heading: true

::: reachq.invariants.assert_partition_correctness
    options:
      show_root_heading: true

::: reachq.invariants.assert_distance_approximation
    options:
      show_root_heading: true

::: reachq.invariants.assert_shortcut_set_size_bound
    options:
      show_root_heading: true

::: reachq.invariants.assert_hopset_size_bound
    options:
      show_root_heading: true

::: reachq.invariants.check_equivalence_classes
    options:
      show_root_heading: true

## CLI

The CLI entry point is `python -m reachq.cli`. It is not part of
the stability contract; consult the `--help` output for the current
surface.

---

## Removing dead entries

If you remove a function from the public API, also remove it from
this page. The mkdocs build will fail if a `:::` directive refers
to a missing symbol, which is the intent: dead entries are caught
in CI.