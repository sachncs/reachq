"""Internal state for the Cython Dijkstra accelerator.

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed.

Only :mod:`reachq.accel.cython.dijkstra` imports from this module.
"""

from __future__ import annotations

from typing import Any

AVAILABLE: bool = False
EXTENSION: Any = None


def probe() -> bool:
    """Try to import the compiled Cython extension; populate EXTENSION.

    Returns:
        True if the extension is loaded, False otherwise.
    """
    global AVAILABLE, EXTENSION
    try:
        from reachq.accel.cython._cy_dijkstra import (  # type: ignore[import-not-found]
            cy_dijkstra as extension,
        )
    except ImportError:
        return False
    EXTENSION = extension
    AVAILABLE = True
    return True


def is_available() -> bool:
    """Return True if the compiled Cython extension is loaded."""
    return AVAILABLE


probe()


__all__ = ["AVAILABLE", "EXTENSION", "is_available", "probe"]