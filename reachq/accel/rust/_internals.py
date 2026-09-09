"""Internal state for the Rust accelerator.

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed.

Only :mod:`reachq.accel.rust` imports from this module.
"""

from __future__ import annotations

from typing import Any

AVAILABLE: bool = False
FORWARD: Any = None
DIJKSTRA: Any = None


def probe() -> bool:
    """Try to import the compiled Rust extension.

    Returns:
        True if the extension is loaded; False otherwise.
    """
    global AVAILABLE, FORWARD, DIJKSTRA
    try:
        from reachq.accel.rust._reachq_rust import (  # type: ignore[import-not-found]
            rust_bfs_forward as forward,
        )
        from reachq.accel.rust._reachq_rust import (
            rust_dijkstra as dijkstra,
        )
    except ImportError:
        # Maturin may install the .so at a different path. Try the
        # top-level module installed via maturin develop.
        try:
            from _reachq_rust._reachq_rust import (  # type: ignore[import-not-found]
                rust_bfs_forward as forward,
            )
            from _reachq_rust._reachq_rust import (
                rust_dijkstra as dijkstra,
            )
        except ImportError:
            return False
    FORWARD = forward
    DIJKSTRA = dijkstra
    AVAILABLE = True
    return True


def is_available() -> bool:
    """Return True if the compiled Rust extension is loaded."""
    return AVAILABLE


probe()


__all__ = ["AVAILABLE", "DIJKSTRA", "FORWARD", "is_available", "probe"]