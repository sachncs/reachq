"""Regression tests for the documented top-level package surface."""

from importlib.metadata import version

import reachq


def test_top_level_api_and_version_are_consistent() -> None:
    expected = {
        "Digraph",
        "WeightedDigraph",
        "build_shortcut_set_for_reachability",
        "build_hopset_for_sssp",
    }

    assert expected <= set(reachq.__all__)
    assert reachq.__version__ == version("reachq")
    for name in expected:
        assert getattr(reachq, name) is not None
