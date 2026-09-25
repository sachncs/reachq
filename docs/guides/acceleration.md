# Acceleration Backends (experimental, not shipped)

`reachq/accel/` contains optional, **experimental** scaffolding for native
kernels (Cython, Rust, Numba) plus Dask/Ray/GraphBLAS hooks. The current
development snapshot is installed from source and the package artifacts built
by CI contain only the pure-Python fallback path.

## What ships vs what does not

| Component | In the current package artifacts? |
|---|---|
| `reachq.core.*` pure-Python algorithms | yes |
| `reachq.accel` wrapper modules + pure-Python fallbacks (`bfs.py`, `dijkstra.py`, `setup.py`) | yes |
| Cython `.pyx` kernels (`reachq/accel/cython`) | **no** (git repo only) |
| Compiled `_cy_*.so` / Rust `.so` extensions | **no** |
| Rust source (`reachq/accel/rust`, `Cargo.toml`, `src/lib.rs`) | **no** (git repo only) |

The shipped wheel and sdist contain only the pure-Python fallback
wrappers. The `.pyx` and Rust sources live only in the git repository,
so the kernels cannot be compiled from an installed package. There is
**no build hook**: `pip install "reachq[accel-cython]"` only installs
build dependencies (`cython`), it does not compile anything.

## Status and support

- **Experimental.** These backends are scaffolding, not a supported feature.
  They are not exercised by CI beyond the pure-Python fallback path, and
  no runtime improvement is promised until a backend has a build path,
  correctness coverage, and reproducible measurements.
- The only behavior guaranteed and tested is the fallback: every wrapper
  falls back to the pure-Python implementations in `reachq.bfs` and
  `reachq.shortest_paths` when the compiled extension is absent
  (covered by `tests/test_accel_fallbacks.py`).
- Do not rely on the native kernels for correctness or performance until
  a build + test path is added and CI-verified.

## If you build them anyway

This requires a **git checkout** of the repo — the kernel sources are not in
the current package artifacts. Building the Cython kernels requires a C
compiler and numpy headers:

```bash
cd reachq/accel/cython
python setup.py build_ext --inplace
```

This produces `_cy_bfs*.so` and `_cy_dijkstra*.so` next to the `.pyx`
files; the wrappers `reachq.accel.cython.bfs` and
`reachq.accel.cython.dijkstra` pick them up on the next import. The Rust
backend builds with `maturin develop --release` in `reachq/accel/rust`.

## Backend overview

| Backend | Build tool | Current status |
|---|---|---|
| **Cython** | `python setup.py build_ext` | Experimental source-only path |
| **Numba** | JIT at first call | Experimental source-only path |
| **Rust** | `maturin develop --release` | Experimental source-only path |

All expose the same Python API:

- `cy_bfs_forward(indptr, indices, source, n, max_depth=...) -> ndarray[bool]`
- `cy_bfs_backward(indptr_rev, indices_rev, source, n, max_depth=...) -> ndarray[bool]`
- `cy_dijkstra(indptr, indices, weights, source, n) -> ndarray[float64]`

Plus helpers `is_cython_available()`, `is_numba_available()`,
`is_rust_available()` that report whether a compiled kernel is loadable
(always `False` for a default install).

## Adding a new backend

To add a new backend (e.g., a GPU kernel):

1. Implement the three kernel functions in your language of choice.
2. Build a Python extension module exposing those functions.
3. Add a wrapper module in `reachq/accel/<name>/__init__.py` that
   tries `import <your_extension>` and falls back to the
   pure-Python implementations.
4. Add an `is_<name>_available()` helper.
5. Add tests in `tests/test_accel_fallbacks.py` covering the
   fallback path.
