"""Internal state for the Cython BFS accelerator.

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed.

Only :mod:`reachq.accel.cython.bfs` imports from this module.
"""

from __future__ import annotations

from typing import Any

AVAILABLE: bool = False
FORWARD: Any = None
BACKWARD: Any = None


def probe() -> bool:
    """Try to import the compiled Cython extension; populate FORWARD/BACKWARD.

    Returns:
        True if the extension is loaded, False otherwise.
    """
    global AVAILABLE, FORWARD, BACKWARD
    try:
        from reachq.accel.cython._cy_bfs import (  # type: ignore[import-not-found]
            cy_bfs_backward as backward,
        )
        from reachq.accel.cython._cy_bfs import (
            cy_bfs_forward as forward,
        )
    except ImportError:
        return False
    FORWARD = forward
    BACKWARD = backward
    AVAILABLE = True
    return True


def is_available() -> bool:
    """Return True if the compiled Cython extension is loaded."""
    return AVAILABLE


probe()


__all__ = ["AVAILABLE", "BACKWARD", "FORWARD", "is_available", "probe"]