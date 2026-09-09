"""Cython extension build configuration for reachq acceleration kernels.

Build::

    cd reachq/accel/cython
    python setup.py build_ext --inplace

After a successful build, ``_cy_bfs*.so`` and ``_cy_dijkstra*.so``
appear next to the ``.pyx`` files. The wrapper modules
``reachq.accel.cython.bfs`` and ``reachq.accel.cython.dijkstra``
will pick them up automatically.

Alternatively, install the wheels built by cibuildwheel from
``reachq[accel]`` distribution on PyPI.
"""

from __future__ import annotations

from setuptools import Extension, setup

from reachq.accel.cython import _setup_helpers as helpers


setup(
    name="reachq_cython_kernels",
    ext_modules=[
        Extension(
            name=helpers.module_name_from_path(path),
            sources=[path],
            include_dirs=helpers.numpy_include(),
            extra_compile_args=["-O3", "-march=native"],
            extra_link_args=["-O3"],
            language="c",
        )
        for path in helpers.pyx_files()
    ],
)