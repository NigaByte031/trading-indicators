"""Average Directional Index (ADX).

A Python port of ``specs/adx.md``. Wilder's trend-strength indicator: the
Wilder-smoothed average of the Directional Movement Index (DX), built on the
smoothed ``+DI`` / ``-DI`` lines. The algorithm, the seeding rule and the
warm-up behaviour must match the specification exactly, because the same
vectors are used to check every other language port.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

__all__ = ["adx", "true_range", "wilder_smoothing", "rma"]


def wilder_smoothing(values: Sequence[float], period: int) -> List[Optional[float]]:
    """Wilder's smoothing (RMA) of a fully-defined series.

    The value at index ``period - 1`` is seeded with the simple average of the
    first ``period`` values; every later value uses
    ``rma[i] = ((period - 1) * rma[i - 1] + values[i]) / period``. The first
    ``period - 1`` values are ``None``.
    """
    count = len(values)
    out: List[Optional[float]] = [None] * count

    if period > count:
        return out

    previous = float(sum(values[:period])) / period
    out[period - 1] = previous
    for i in range(period, count):
        previous = ((period - 1) * previous + values[i]) / period
        out[i] = previous

    return out


# Alias: the specification calls Wilder's smoothing "rma" in its pseudocode.
rma = wilder_smoothing


def true_range(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
) -> List[float]:
    """Return the True Range series (defined at every index).

    ``TR[0] = high[0] - low[0]``; for ``i >= 1`` it is the greatest of the high
    minus low, the gap to the previous close, and the gap from the previous
    close to the low.
    """
    count = len(high)
    out: List[float] = [0.0] * count
    if count == 0:
        return out

    out[0] = high[0] - low[0]
    for i in range(1, count):
        out[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1]),
        )
    return out


def adx(
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    period: int = 14,
) -> List[Optional[float]]:
    """Return the ADX of the ``high`` / ``low`` / ``close`` series.

    The returned list has the same length as the inputs. The first
    ``2 * period - 2`` values are ``None`` (the warm-up region). If there is not
    enough data to seed the DX average, every value is ``None``.
    """
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period < 1:
        raise ValueError("period must be >= 1")

    count = len(high)
    if len(low) != count or len(close) != count:
        raise ValueError("high, low and close must have the same length")

    out: List[Optional[float]] = [None] * count
    if count == 0:
        return out

    # Step 1 — True Range and directional movement.
    tr: List[float] = [0.0] * count
    plus_dm: List[float] = [0.0] * count
    minus_dm: List[float] = [0.0] * count
    tr[0] = high[0] - low[0]
    for i in range(1, count):
        up = high[i] - high[i - 1]
        down = low[i - 1] - low[i]
        plus_dm[i] = up if (up > down and up > 0) else 0.0
        minus_dm[i] = down if (down > up and down > 0) else 0.0
        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1]),
        )

    # Step 2 — smooth the three series.
    atr = wilder_smoothing(tr, period)
    plus = wilder_smoothing(plus_dm, period)
    minus = wilder_smoothing(minus_dm, period)

    # Step 3 — Directional indicators and DX (defined from `period - 1`).
    first = period - 1
    dx: List[Optional[float]] = [None] * count
    for i in range(count):
        atr_i = atr[i]
        if atr_i is None:
            continue
        if atr_i == 0:
            dx[i] = 0.0
            continue
        plus_di = 100.0 * plus[i] / atr_i  # type: ignore[operator]
        minus_di = 100.0 * minus[i] / atr_i  # type: ignore[operator]
        total = plus_di + minus_di
        dx[i] = 0.0 if total == 0 else 100.0 * abs(plus_di - minus_di) / total

    # Step 4 — average the DX (defined from `2 * period - 2`).
    if first >= count:
        return out
    defined_dx = [value for value in dx[first:] if value is not None]
    smoothed = wilder_smoothing(defined_dx, period)
    for k, value in enumerate(smoothed):
        out[first + k] = value

    return out
