"""Internal helpers for :file:`setup.py` (build-time only).

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed. Only :file:`setup.py` imports from this
module.
"""

from __future__ import annotations

import os

import numpy as np


def numpy_include() -> list[str]:
    """Return numpy include path."""
    return [np.get_include()]


def pyx_files() -> list[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(here, name) for name in os.listdir(here) if name.endswith(".pyx")
    ]


def module_name_from_path(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    # Files named bfs.pyx -> _cy_bfs; dijkstra.pyx -> _cy_dijkstra.
    return f"_cy_{base}"


__all__ = ["module_name_from_path", "numpy_include", "pyx_files"]