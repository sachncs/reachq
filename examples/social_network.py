"""Synthetic social-graph reachability example.

This intentionally uses a small generated graph. Downloading a large SNAP
dataset is not a safe default for an example, and a large-graph result needs a
separate reproducible benchmark record.
"""

from reachq.generators import random_dag
from reachq.shortcut import build_shortcut_set_for_reachability


def main() -> None:
    g = random_dag(n=100, edge_probability=0.05, random_seed=42)
    print(f"synthetic social graph: {g.num_vertices()} nodes, {g.num_edges()} edges")
    H, beta, _ = build_shortcut_set_for_reachability(g, omega=3.0, random_seed=42)
    print(f"shortcut set: {len(H)} shortcuts (beta={beta:.2f})")
    print(f"|H|/|E| ratio: {len(H) / max(1, g.num_edges()):.2f}")


if __name__ == "__main__":
    main()
