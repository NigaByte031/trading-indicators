# Exponential Moving Average (EMA)

A moving average that weights recent prices more heavily than older ones, using
an exponentially decaying weighting.

## Parameters

| Name   | Type | Default | Range | Description                                   |
|--------|------|---------|-------|-----------------------------------------------|
| period | int  | 14      | >= 1  | The smoothing period (number of lookback bars) |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

- `ema` — a series the **same length** as `close`.
- The first `period - 1` values are **undefined** (they are emitted as `null` /
  NaN). This is the warm-up region.
- The value at index `period - 1` is the seed (see below).
- Every later value is computed by the recurrence.

## Algorithm

Let `alpha = 2 / (period + 1)`.

1. If `period < 1`, raise an error.
2. If `period > length(close)`, the whole output is undefined.
3. Otherwise:
   - The output at index `i` is undefined for `i < period - 1`.
   - **Seed:** `ema[period - 1] = mean(close[0 .. period - 1])` (the simple
     average of the first `period` values).
   - For `i` from `period` to `length(close) - 1`:
     `ema[i] = alpha * close[i] + (1 - alpha) * ema[i - 1]`.

Pseudocode:

```
alpha = 2 / (period + 1)
out   = array of length(close) filled with undefined
if period <= length(close):
    out[period - 1] = mean(close[0 : period])
    for i in period .. length(close) - 1:
        out[i] = alpha * close[i] + (1 - alpha) * out[i - 1]
```

## Edge cases

- `period < 1` → error.
- `period == 1` → `alpha == 1`, the seed is `close[0]`, and every value equals
  the corresponding input price (identity).
- `period > length(close)` → no defined values; the whole output is undefined.
- An empty input → an empty output.
- No value is ever defined before index `period - 1`; do **not** back-fill the
  warm-up region.

## References

- Standard technical-analysis definition of the EMA.
- Note on seeding: this spec uses the **SMA seed** (the SMA of the first
  `period` prices), which is the convention used by most charting platforms.
  Some libraries instead seed with the first price; the shared test vectors in
  `specs/vectors/ema.json` pin down the required behaviour.
