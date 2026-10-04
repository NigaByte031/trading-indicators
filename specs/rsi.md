# Relative Strength Index (RSI)

Wilder's momentum oscillator that measures the speed and magnitude of recent
price changes on a 0–100 scale. It compares the recent average gain with the
recent average loss, both smoothed with Wilder's smoothing.

## Parameters

| Name   | Type | Default | Range | Description                                   |
|--------|------|---------|-------|-----------------------------------------------|
| period | int  | 14      | >= 1  | The smoothing period (number of lookback bars) |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

- `rsi` — a series the **same length** as `close`.
- The first `period` values are **undefined** (the warm-up region); that is,
  `rsi` needs `period + 1` closes before it has a first value.
- The value at index `period` is the seed (see below); every later value is
  computed by the recurrence.
- Every defined value lies in `[0, 100]`.

## Algorithm

Work with per-bar changes `delta[i] = close[i] - close[i - 1]`, and split each
into `gain[i] = max(delta[i], 0)` and `loss[i] = max(-delta[i], 0)`. Note that
`delta[0]` does not exist (there is no previous close).

**Seed (index `period`)** — the simple average of the first `period` changes:

```
avg_gain = mean(gain[1 .. period])
avg_loss = mean(loss[1 .. period])
rsi[period] = rsi_from(avg_gain, avg_loss)
```

**Recurrence (index `i > period`)** — Wilder's smoothing:

```
avg_gain = ((period - 1) * avg_gain + gain[i]) / period
avg_loss = ((period - 1) * avg_loss + loss[i]) / period
rsi[i]   = rsi_from(avg_gain, avg_loss)
```

**`rsi_from`:**

```
if avg_loss == 0:
    return 100
rs = avg_gain / avg_loss
return 100 - 100 / (1 + rs)
```

Pseudocode:

```
out = array of length(close) filled with undefined
if length(close) >= period + 1:
    avg_gain = mean(close[i] - close[i - 1] for i in 1 .. period, positive part)
    avg_loss = mean(... negative part ...)
    out[period] = rsi_from(avg_gain, avg_loss)
    for i in period + 1 .. length(close) - 1:
        duration = close[i] - close[i - 1]
        avg_gain = ((period - 1) * avg_gain + max(duration, 0)) / period
        avg_loss = ((period - 1) * avg_loss + max(-duration, 0)) / period
        out[i] = rsi_from(avg_gain, avg_loss)
```

## Edge cases

- `period < 1` → error.
- Fewer than `period + 1` input values → the whole output is undefined.
- `avg_loss == 0` (no declines in the window, including a perfectly flat
  market) → `rsi = 100`.
- An all-up market → `avg_loss == 0` → `rsi = 100`.
- An all-down market → `avg_gain == 0` → `rs == 0` → `rsi = 0`.
- An empty input → an empty output.
- No value is ever defined before index `period`; do **not** back-fill the
  warm-up region.

## References

- J. Welles Wilder Jr., *New Concepts in Technical Trading Systems* (1978).
- Standard technical-analysis definition. This spec uses Wilder's smoothing with
  the simple-average seed, consistent with the ADX spec in this repository.
