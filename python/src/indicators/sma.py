"""Simple Moving Average (SMA / MA).

A Python port of ``specs/sma.md``. This is the classic unweighted moving
average; the algorithm and warm-up behaviour must match the specification
exactly, because the same vectors are used to check every other language port.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

__all__ = ["sma"]


def sma(close: Sequence[float], period: int) -> List[Optional[float]]:
    """Return the SMA of ``close`` over ``period`` bars.

    The returned list has the same length as ``close``. The first
    ``period - 1`` values are ``None`` (the warm-up region). If ``period`` is
    longer than ``close``, every value is ``None``.
    """
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period < 1:
        raise ValueError("period must be >= 1")

    count = len(close)
    out: List[Optional[float]] = [None] * count

    if period > count:
        return out

    # Rolling sum of the current window, to avoid re-summing every bar.
    running = float(sum(close[:period]))
    out[period - 1] = running / period
    for i in range(period, count):
        running += close[i] - close[i - period]
        out[i] = running / period

    return out
