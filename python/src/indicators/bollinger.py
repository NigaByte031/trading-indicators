"""Bollinger Bands (BB).

A Python port of ``specs/bollinger.md``. A simple moving average with an upper
and lower band drawn a number of population standard deviations away from it.
The algorithm and warm-up behaviour must match the specification exactly,
because the same vectors are used to check every other language port.
"""

from __future__ import annotations

import math
from typing import List, NamedTuple, Optional, Sequence

__all__ = ["bollinger", "BollingerBands"]


class BollingerBands(NamedTuple):
    """The three Bollinger Band lines, each the same length as the input."""

    middle: List[Optional[float]]
    upper: List[Optional[float]]
    lower: List[Optional[float]]


def bollinger(
    close: Sequence[float],
    period: int = 20,
    num_std: float = 2,
) -> BollingerBands:
    """Return the Bollinger Bands of ``close`` over ``period`` bars.

    The returned series have the same length as ``close``. The first
    ``period - 1`` values of each line are ``None`` (the warm-up region). If
    ``period`` is longer than ``close``, every value is ``None``.
    """
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period < 1:
        raise ValueError("period must be >= 1")
    if isinstance(num_std, bool) or not isinstance(num_std, (int, float)):
        raise TypeError("num_std must be a number")
    if num_std < 0:
        raise ValueError("num_std must be >= 0")

    count = len(close)
    middle: List[Optional[float]] = [None] * count
    upper: List[Optional[float]] = [None] * count
    lower: List[Optional[float]] = [None] * count

    if period > count:
        return BollingerBands(middle, upper, lower)

    for i in range(period - 1, count):
        window = close[i - period + 1 : i + 1]
        mean = sum(window) / period
        variance = sum((value - mean) ** 2 for value in window) / period
        stddev = math.sqrt(variance)
        middle[i] = mean
        upper[i] = mean + num_std * stddev
        lower[i] = mean - num_std * stddev

    return BollingerBands(middle, upper, lower)
