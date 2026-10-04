# Bollinger Bands (BB)

A volatility envelope around a simple moving average: a moving average with an
upper and a lower band drawn `num_std` standard deviations away from it. The
bands widen when the market is volatile and narrow when it is calm.

## Parameters

| Name    | Type  | Default | Range | Description                                      |
|---------|-------|---------|-------|--------------------------------------------------|
| period  | int   | 20      | >= 1  | The moving-average and deviation window          |
| num_std | float | 2       | >= 0  | The number of standard deviations for the bands  |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

Three series, each the **same length** as `close`:

- `middle` — the simple moving average (SMA) of `close` over `period`.
- `upper` — `middle + num_std * stddev`.
- `lower` — `middle - num_std * stddev`.

The first `period - 1` values of all three are **undefined** (the warm-up
region); `upper` and `lower` are undefined exactly where `middle` is.

## Algorithm

Let `stddev` be the **population** standard deviation of the trailing `period`
prices (divide the sum of squared deviations by `period`, not `period - 1`).

For `i` from `period - 1` to `length(close) - 1`, with the window
`w = close[i - period + 1 .. i]`:

```
mean    = sum(w) / period
variance = sum((x - mean)^2 for x in w) / period
stddev  = sqrt(variance)
middle[i] = mean
upper[i]  = mean + num_std * stddev
lower[i]  = mean - num_std * stddev
```

Pseudocode:

```
out = three arrays of length(close) filled with undefined
if period <= length(close):
    for i in period - 1 .. length(close) - 1:
        mean, variance = moments(close[i - period + 1 : i + 1])
        sd = sqrt(variance)
        middle[i] = mean
        upper[i]  = mean + num_std * sd
        lower[i]  = mean - num_std * sd
```

## Edge cases

- `period < 1` → error.
- `num_std < 0` → error.
- `num_std == 0` → the bands collapse onto `middle` (`upper == middle == lower`).
- `period == 1` → the standard deviation is 0, so all three lines equal
  `close`.
- `period > length(close)` → no defined values; all three series are undefined.
- An empty input → three empty series.
- No value is ever defined before index `period - 1`; do **not** back-fill the
  warm-up region.

## References

- John Bollinger, *Bollinger on Bollinger Bands* (2001).
- Standard technical-analysis definition. This spec uses the **population**
  standard deviation (the convention used by most charting platforms).
