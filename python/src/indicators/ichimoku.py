"""Ichimoku Kinko Hyo (Ichimoku).

A Python port of ``specs/ichimoku.md``. The five lines are returned at the bar
where a chart would **plot** them: the leading spans are shifted forward by
``displacement`` bars and the lagging span is shifted back, so the arrays never
extend past the input length. The algorithm, the shift and the warm-up
behaviour must match the specification exactly, because the same vectors are
used to check every other language port.
"""

from __future__ import annotations

from typing import List, NamedTuple, Optional, Sequence

__all__ = ["ichimoku", "IchimokuResult"]


class IchimokuResult(NamedTuple):
    """The five Ichimoku lines, each the same length as the input."""

    tenkan: List[Optional[float]]
    kijun: List[Optional[float]]
    senkou_a: List[Optional[float]]
    senkou_b: List[Optional[float]]
    chikou: List[Optional[float]]


def _midpoint(
    high: Sequence[float],
    low: Sequence[float],
    period: int,
    count: int,
) -> List[Optional[float]]:
    """Return ``(max(high) + min(low)) / 2`` over the trailing ``period`` bars."""
    out: List[Optional[float]] = [None] * count
    if period > count:
        return out

    for i in range(period - 1, count):
        start = i - period + 1
        window_high = high[start : i + 1]
        window_low = low[start : i + 1]
        out[i] = (max(window_high) + min(window_low)) / 2.0
    return out


def ichimoku(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    conversion: int = 9,
    base: int = 26,
    span_b: int = 52,
    displacement: int = 26,
) -> IchimokuResult:
    """Return the five Ichimoku lines of the ``high`` / ``low`` / ``close`` series.

    ``displacement`` bakes the standard shift into the returned arrays: the
    leading spans are moved ``displacement`` bars forward and Chikou is moved
    ``displacement`` bars back. Use ``displacement=0`` for the unshifted lines.
    """
    for name, value in (
        ("conversion", conversion),
        ("base", base),
        ("span_b", span_b),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value < 1:
            raise ValueError(f"{name} must be >= 1")
    if isinstance(displacement, bool) or not isinstance(displacement, int):
        raise TypeError("displacement must be an int")
    if displacement < 0:
        raise ValueError("displacement must be >= 0")

    count = len(high)
    if len(low) != count or len(close) != count:
        raise ValueError("high, low and close must have the same length")

    tenkan = _midpoint(high, low, conversion, count)
    kijun = _midpoint(high, low, base, count)

    senkou_a_raw: List[Optional[float]] = [None] * count
    for i in range(count):
        if tenkan[i] is not None and kijun[i] is not None:
            senkou_a_raw[i] = (tenkan[i] + kijun[i]) / 2.0  # type: ignore[operator]

    senkou_b_raw = _midpoint(high, low, span_b, count)

    # Bake the displacement in: plot each line at its shifted bar.
    senkou_a: List[Optional[float]] = [None] * count
    senkou_b: List[Optional[float]] = [None] * count
    for i in range(count):
        source = i - displacement
        if source >= 0:
            senkou_a[i] = senkou_a_raw[source]
            senkou_b[i] = senkou_b_raw[source]

    chikou: List[Optional[float]] = [None] * count
    for i in range(count):
        source = i + displacement
        if source < count:
            chikou[i] = close[source]

    return IchimokuResult(tenkan, kijun, senkou_a, senkou_b, chikou)
