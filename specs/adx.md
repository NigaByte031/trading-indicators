# Average Directional Index (ADX)

Wilder's trend-strength indicator: a Wilder-smoothed average of the Directional
Movement Index (DX), which itself is derived from the smoothed `+DI` / `-DI`
lines. The ADX measures the **strength** of a trend, not its direction.

## Parameters

| Name   | Type | Default | Range | Description                                |
|--------|------|---------|-------|--------------------------------------------|
| period | int  | 14      | >= 1  | The smoothing period of the Wilder averages |

## Input

- `high` — the high price series (numbers, oldest first).
- `low` — the low price series.
- `close` — the close price series.
- All three inputs must have the **same length**.

## Output

- `adx` — a series the **same length** as the input.
- The first `2 * period - 2` values are **undefined** (the warm-up region).
- The value at index `2 * period - 2` is the seed (see below); every later value
  is computed by the recurrence.

## Algorithm

All smoothing uses **Wilder's smoothing** (RMA), defined below.

**RMA of a series `x` over `period`:**

```
rma[period - 1] = mean(x[0 .. period - 1])          # SMA seed
rma[i]          = rma[i - 1] + (x[i] - rma[i - 1]) / period   # for i >= period
```

which is equivalent to `rma[i] = ((period - 1) * rma[i - 1] + x[i]) / period`.

**Step 1 — True Range (TR) and Directional Movement.**

- `TR[0] = high[0] - low[0]`, and `+DM[0] = -DM[0] = 0`.
- For `i >= 1`, with `up = high[i] - high[i - 1]` and `down = low[i - 1] - low[i]`:
  - `+DM[i] = up`   if `up > down` and `up > 0`, else `0`.
  - `-DM[i] = down` if `down > up` and `down > 0`, else `0`.
  - `TR[i] = max(high[i] - low[i], |high[i] - close[i - 1]|, |low[i] - close[i - 1]|)`.

**Step 2 — Smooth the three series.**

- `atr = rma(TR, period)`, `plus = rma(+DM, period)`, `minus = rma(-DM, period)`.
- All three are first defined at index `period - 1`.

**Step 3 — Directional indicators and DX (for `i >= period - 1`).**

- `+DI[i] = 100 * plus[i] / atr[i]`, `-DI[i] = 100 * minus[i] / atr[i]`.
- If `atr[i] == 0`, then `+DI[i] = -DI[i] = 0` (and `DX[i] = 0`).
- `DX[i] = 100 * |+DI[i] - -DI[i]| / (+DI[i] + -DI[i])`, and `DX[i] = 0` when
  `+DI[i] + -DI[i] == 0`.

**Step 4 — Average the DX.**

- `adx = rma(DX, period)`, applied to the defined region of `DX` (which starts
  at index `period - 1`).
- Hence `adx[2 * period - 2] = mean(DX[period - 1 .. 2 * period - 2])`, and for
  `i >= 2 * period - 1`: `adx[i] = ((period - 1) * adx[i - 1] + DX[i]) / period`.

Pseudocode:

```
out = array of length(high) filled with undefined
if 2 * period - 2 <= length(high) - 1:
    tr, plus_dm, minus_dm = step_1(high, low, close)
    atr   = rma(tr, period)
    plus  = rma(plus_dm, period)
    minus = rma(minus_dm, period)
    dx = step_3(plus, minus, atr, period)   # defined from period - 1
    smoothed = rma(dx[period - 1 :], period)
    for k in 0 .. length(smoothed) - 1:
        out[period - 1 + k] = smoothed[k]
```

## Edge cases

- `period < 1` → error.
- Inputs of different lengths → error.
- Not enough data for a seed (`length < 2 * period - 1`) → the whole output is
  undefined.
- A flat market where `+DI + -DI == 0` → `DX = 0` (and therefore ADX is driven
  to 0), rather than a division error or NaN.
- An empty input → an empty output.
- No value is ever defined before index `2 * period - 2`; do **not** back-fill
  the warm-up region.

## References

- J. Welles Wilder Jr., *New Concepts in Technical Trading Systems* (1978).
- Standard technical-analysis definition of the ADX / DMI. This spec uses the
  **SMA-seeded Wilder smoothing (RMA)** convention for every smoothed series.
