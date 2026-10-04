"""Exponential Moving Average (EMA).

A Python port of ``specs/ema.md``. The algorithm, the seeding rule and the
warm-up behaviour must match the specification exactly, because the same
vectors are used to check every other language port.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

__all__ = ["ema"]


def ema(close: Sequence[float], period: int) -> List[Optional[float]]:
    """Return the EMA of ``close`` over ``period`` bars.

    The returned list has the same length as ``close``. The first
    ``period - 1`` values are ``None`` (the warm-up region) and the value at
    index ``period - 1`` is seeded with the simple average of the first
    ``period`` values. If ``period`` is longer than ``close``, every value is
    ``None``.
    """
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period < 1:
        raise ValueError("period must be >= 1")

    count = len(close)
    out: List[Optional[float]] = [None] * count

    if period > count:
        return out

    # Seed with the SMA of the first `period` values.
    seed_index = period - 1
    previous = sum(close[:period]) / period
    out[seed_index] = previous

    alpha = 2.0 / (period + 1.0)
    for i in range(period, count):
        previous = alpha * close[i] + (1.0 - alpha) * previous
        out[i] = previous

    return out
