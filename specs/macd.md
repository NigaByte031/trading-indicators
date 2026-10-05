# MACD (Moving Average Convergence Divergence)

A trend-following momentum indicator built from two exponential moving averages
of the price. It produces three lines: the MACD line (the fast/slow spread), a
signal line (an EMA *of the MACD line*) and a histogram (their difference).

## Parameters

| Name          | Type | Default | Range | Description                                       |
|---------------|------|---------|-------|---------------------------------------------------|
| fast_period   | int  | 12      | >= 1  | The window of the faster EMA                      |
| slow_period   | int  | 26      | >= 1  | The window of the slower EMA                      |
| signal_period | int  | 9       | >= 1  | The window of the signal EMA                      |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

Three series, each the **same length** as `close`:

- `macd` — `EMA(close, fast_period) - EMA(close, slow_period)`.
- `signal` — `EMA(macd, signal_period)`, the exponential average **of the MACD
  line**, computed only over the region where the MACD line is defined.
- `histogram` — `macd - signal`.

## Algorithm

Build both EMAs with the same seeding rule as [`ema.md`](ema.md): the value at
index `period - 1` is the simple average of the first `period` prices, and every
later value is `alpha * price + (1 - alpha) * previous` with
`alpha = 2 / (period + 1)`.

```
fast = EMA(close, fast_period)
slow = EMA(close, slow_period)

# The MACD line is defined exactly where both EMAs are defined.
start = max(fast_period - 1, slow_period - 1)
for i in start .. length(close) - 1:
    macd[i] = fast[i] - slow[i]

# The signal line is an EMA of the *defined* MACD values, re-aligned.
defined = macd[start .. length(close) - 1]      # a dense list of floats
signal_values = EMA(defined, signal_period)     # same seeding rule
for j in 0 .. length(defined) - 1:
    if signal_values[j] is defined:
        signal[start + j] = signal_values[j]
        histogram[start + j] = macd[start + j] - signal_values[j]
```

The `histogram` is defined exactly where the `signal` is.

## Warm-up

- The MACD line is `undefined` for the first `max(fast_period, slow_period) - 1`
  values (the slower EMA's warm-up region).
- The signal line additionally needs `signal_period` defined MACD values, so its
  first defined index — and therefore the histogram's — is
  `max(fast_period, slow_period) - 1 + signal_period - 1`
  (i.e. `slow_period + signal_period - 2` under the classic defaults).
- `undefined` values are never back-filled.

## Edge cases

- Any `*_period < 1` → error.
- `fast_period == slow_period` → the MACD line is `0.0` wherever it is defined,
  so the signal and histogram are `0.0` too.
- Very short input, where the slower EMA has no defined value
  (`slow_period > length(close)`) → all three series are entirely `undefined`.
- The number of defined MACD values is smaller than `signal_period` → `macd` has
  defined values but `signal` and `histogram` are entirely `undefined`.
- An empty input → three empty series.

## References

- Gerald Appel, *The Moving Average Convergence-Divergence Trading Method*
  (1979).
- Standard technical-analysis definition (as used by most charting platforms).
