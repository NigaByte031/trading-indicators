# Simple Moving Average (SMA / MA)

The unweighted mean of the last `period` prices. This is the classic "moving
average" (MA) and is the baseline every other moving average is compared to.

## Parameters

| Name   | Type | Default | Range | Description                                   |
|--------|------|---------|-------|-----------------------------------------------|
| period | int  | 14      | >= 1  | The smoothing period (number of lookback bars) |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

- `sma` — a series the **same length** as `close`.
- The first `period - 1` values are **undefined** (they are emitted as `null` /
  NaN). This is the warm-up region.
- The value at index `i >= period - 1` is the arithmetic mean of the `period`
  prices ending at `i` (inclusive).

## Algorithm

1. If `period < 1`, raise an error.
2. If `period > length(close)`, the whole output is undefined.
3. Otherwise, for `i` from `period - 1` to `length(close) - 1`:
   `sma[i] = mean(close[i - period + 1 .. i])`.

Pseudocode:

```
out = array of length(close) filled with undefined
if period <= length(close):
    for i in period - 1 .. length(close) - 1:
        out[i] = mean(close[i - period + 1 : i + 1])
```

A rolling sum may be kept instead of re-summing each window, provided the result
is identical up to floating-point tolerance.

## Edge cases

- `period < 1` → error.
- `period == 1` → every value equals the corresponding input price (identity).
- `period > length(close)` → no defined values; the whole output is undefined.
- An empty input → an empty output.
- No value is ever defined before index `period - 1`; do **not** back-fill the
  warm-up region.

## References

- Standard technical-analysis definition of the simple moving average.

## Notes on naming

The indicator is known as **SMA** ("simple moving average") or simply **MA**
("moving average") depending on the platform. The slug used everywhere in this
repository is `sma`.
