"""Relative Strength Index (RSI).

A Python port of ``specs/rsi.md``. Wilder's momentum oscillator: it compares the
recent average gain with the recent average loss, both smoothed with Wilder's
smoothing. The algorithm, the seeding rule and the warm-up behaviour must match
the specification exactly, because the same vectors are used to check every
other language port.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

__all__ = ["rsi"]


def _rsi_from(avg_gain: float, avg_loss: float) -> float:
    """Return the RSI of one smoothed gain/loss pair."""
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - 100.0 / (1.0 + rs)


def rsi(close: Sequence[float], period: int = 14) -> List[Optional[float]]:
    """Return the RSI of ``close`` over ``period`` bars.

    The returned list has the same length as ``close``. The first ``period``
    values are ``None`` (the warm-up region) and the value at index ``period`` is
    seeded with the simple average of the first ``period`` gains and losses. If
    there are fewer than ``period + 1`` prices, every value is ``None``.
    """
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period < 1:
        raise ValueError("period must be >= 1")

    count = len(close)
    out: List[Optional[float]] = [None] * count

    if count < period + 1:
        return out

    # Seed with the simple average of the first `period` gains and losses.
    gain_sum = 0.0
    loss_sum = 0.0
    for i in range(1, period + 1):
        change = close[i] - close[i - 1]
        if change > 0:
            gain_sum += change
        elif change < 0:
            loss_sum -= change

    avg_gain = gain_sum / period
    avg_loss = loss_sum / period
    out[period] = _rsi_from(avg_gain, avg_loss)

    # Wilder's smoothing for the rest of the series.
    for i in range(period + 1, count):
        change = close[i] - close[i - 1]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0
        avg_gain = ((period - 1) * avg_gain + gain) / period
        avg_loss = ((period - 1) * avg_loss + loss) / period
        out[i] = _rsi_from(avg_gain, avg_loss)

    return out
