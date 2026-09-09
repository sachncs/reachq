"""Internal helpers for :mod:`reachq.generators`.

The leading-underscore module name signals "private" to importers;
the helpers inside use plain names so they are not single-
underscore-prefixed.

Only :mod:`reachq.generators` imports from this module.
"""

from __future__ import annotations


def is_prime(n: int) -> bool:
    """Return True iff ``n`` is a prime number.

    Used by ``paley_graph`` to validate the prime ``q`` argument.
    Trial division up to sqrt(n); fine for small n used in fixtures.
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def int_to_base_q(v: int, q: int, d: int) -> list[int]:
    """Convert integer to base-q representation with d digits (LSB at index 0)."""
    out = [0] * d
    for i in range(d):
        out[i] = v % q
        v //= q
    return out


def base_q_to_int(coords: list[int], q: int) -> int:
    """Convert base-q digit list (LSB at index 0) back to integer."""
    v = 0
    for i, x in enumerate(coords):
        v += x * (q**i)
    return v


__all__ = ["base_q_to_int", "int_to_base_q", "is_prime"]