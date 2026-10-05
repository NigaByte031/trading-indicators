"""Moving Average Convergence Divergence (MACD).

A Python port of ``specs/macd.md``. Two exponential moving averages of the
price give the MACD line; an EMA *of that line* gives the signal; their
difference is the histogram. The algorithm, the seeding rule and the warm-up
behaviour must match the specification exactly, because the same vectors are
used to check every other language port.
"""

from __future__ import annotations

from typing import List, NamedTuple, Optional, Sequence

from indicators.ema import ema

__all__ = ["macd", "MACDResult"]


class MACDResult(NamedTuple):
    """The three MACD lines, each the same length as the input."""

    macd: List[Optional[float]]
    signal: List[Optional[float]]
    histogram: List[Optional[float]]


def macd(
    close: Sequence[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> MACDResult:
    """Return the MACD lines of ``close``.

    The returned series have the same length as ``close``. The MACD line is
    undefined through the slower EMA's warm-up; the signal line and histogram
    are additionally undefined until ``signal_period`` MACD values exist.
    """
    for name, period in (
        ("fast_period", fast_period),
        ("slow_period", slow_period),
        ("signal_period", signal_period),
    ):
        if isinstance(period, bool) or not isinstance(period, int):
            raise TypeError(f"{name} must be an int")
        if period < 1:
            raise ValueError(f"{name} must be >= 1")

    count = len(close)
    fast = ema(close, fast_period)
    slow = ema(close, slow_period)

    macd_line: List[Optional[float]] = [None] * count
    start: Optional[int] = None
    for i in range(count):
        if fast[i] is not None and slow[i] is not None:
            macd_line[i] = fast[i] - slow[i]  # type: ignore[operator]
            if start is None:
                start = i

    signal_line: List[Optional[float]] = [None] * count
    histogram: List[Optional[float]] = [None] * count

    if start is not None:
        defined: List[float] = []
        for i in range(start, count):
            value = macd_line[i]
            assert value is not None  # dense from `start` onward
            defined.append(value)

        signal_values = ema(defined, signal_period)
        for j, value in enumerate(signal_values):
            if value is not None:
                index = start + j
                signal_line[index] = value
                histogram[index] = defined[j] - value

    return MACDResult(macd_line, signal_line, histogram)
