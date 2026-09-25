"""Execute the two canonical examples published on the documentation site."""

from reachq import WeightedDigraph
from reachq.generators import random_dag
from reachq.hopset import build_hopset_for_sssp
from reachq.invariants import (
    assert_distance_approximation,
    assert_reachability_preserved,
)
from reachq.shortcut import build_shortcut_set_for_reachability


def test_documented_reachability_example() -> None:
    graph = random_dag(n=100, edge_probability=0.1, random_seed=42)
    shortcuts, _, realised_bound = build_shortcut_set_for_reachability(
        graph, omega=3.0, random_seed=42
    )

    assert realised_bound >= 0
    assert_reachability_preserved(graph, shortcuts)


def test_documented_shortest_path_example() -> None:
    graph = WeightedDigraph()
    graph.add_edge("a", "b", 1)
    graph.add_edge("b", "c", 2)
    graph.add_edge("a", "c", 10)
    hopset, _ = build_hopset_for_sssp(graph, epsilon=0.1, random_seed=42, omega=3.0)

    ratios = assert_distance_approximation(
        graph, hopset, source="a", epsilon=0.1, max_hops=20
    )
    assert ratios["c"] <= 1.1
