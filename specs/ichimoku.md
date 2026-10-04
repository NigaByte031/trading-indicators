# Ichimoku Kinko Hyo (Ichimoku)

A trend, momentum and support/resistance system built from five lines, three of
which are plotted with a **displacement**: the two leading spans form the "cloud"
(`kumo`) shifted forward, and the lagging span is shifted backward.

The five lines are:

| Line | Name | Formula |
|------|------|---------|
| Tenkan-sen  | Conversion Line | midpoint(`conversion`) |
| Kijun-sen   | Base Line       | midpoint(`base`) |
| Senkou A    | Leading Span A  | `(tenkan + kijun) / 2`, plotted `displacement` bars ahead |
| Senkou B    | Leading Span B  | midpoint(`span_b`), plotted `displacement` bars ahead |
| Chikou      | Lagging Span    | `close`, plotted `displacement` bars behind |

where `midpoint(p, i) = (max(high[i - p + 1 .. i]) + min(low[i - p + 1 .. i])) / 2`.

## Parameters

| Name         | Type | Default | Range | Description                                  |
|--------------|------|---------|-------|----------------------------------------------|
| conversion   | int  | 9       | >= 1  | Tenkan-sen period                            |
| base         | int  | 26      | >= 1  | Kijun-sen period                             |
| span_b       | int  | 52      | >= 1  | Senkou Span B period                         |
| displacement | int  | 26      | >= 0  | Bars the leading spans lead / the Chikou lags |

## Input

- `high` — the high price series (numbers, oldest first).
- `low` — the low price series.
- `close` — the close price series.
- All three inputs must have the **same length**.

## Output

Five series, each the **same length** as the input:

- `tenkan`, `kijun` — defined from index `conversion - 1` and `base - 1`
  respectively; **undefined** before that (the warm-up region).
- `senkou_a` — `(tenkan + kijun) / 2` computed `displacement` bars earlier, so
  `senkou_a[i] = (tenkan[i - displacement] + kijun[i - displacement]) / 2`.
  Undefined where the earlier value is undefined (equivalently while
  `i - displacement < max(conversion, base) - 1`).
- `senkou_b` — `midpoint(span_b)` computed `displacement` bars earlier, so
  `senkou_b[i] = midpoint(span_b, i - displacement)`. Undefined while
  `i - displacement < span_b - 1`.
- `chikou` — the close shifted `displacement` bars **back**, so
  `chikou[i] = close[i + displacement]`. Undefined for the last `displacement`
  bars (`i + displacement > length - 1`).

The displacement is therefore baked into the returned arrays: the values sit at
the bar where a chart would **plot** them, and the future-most `displacement`
cloud bars are truncated at the end of the array (the arrays never extend past
the input length). Setting `displacement = 0` disables all shifting and returns
the raw lines.

## Algorithm

Let `n = length(high)`, `d = displacement`.

1. If any period `< 1`, raise an error; if `d < 0`, raise an error.
2. `tenkan[i] = midpoint(conversion, i)` for `i >= conversion - 1`.
3. `kijun[i]  = midpoint(base, i)`       for `i >= base - 1`.
4. `senkou_a_raw[i] = (tenkan[i] + kijun[i]) / 2` where both are defined.
5. `senkou_b_raw[i] = midpoint(span_b, i)` for `i >= span_b - 1`.
6. Shift: for each `i`, if `i - d >= 0` then
   `senkou_a[i] = senkou_a_raw[i - d]` and `senkou_b[i] = senkou_b_raw[i - d]`;
   otherwise both are undefined.
7. Lag: for each `i`, if `i + d <= n - 1` then `chikou[i] = close[i + d]`;
   otherwise undefined.

Pseudocode:

```
tenkan    = midpoint_series(high, low, conversion)
kijun     = midpoint_series(high, low, base)
senkou_a_raw = [(tenkan[i] + kijun[i]) / 2 where both defined]
senkou_b_raw = midpoint_series(high, low, span_b)

senkou_a = shift_forward(senkou_a_raw, d)   # out[i] = raw[i - d]
senkou_b = shift_forward(senkou_b_raw, d)
chikou   = shift_backward(close, d)         # out[i] = close[i + d]
```

## Edge cases

- Any period `< 1` → error; `displacement < 0` → error.
- Inputs of different lengths → error.
- A period longer than the input → that line is entirely undefined (and any
  leading span depending on it is too).
- `displacement == 0` → no shifting: `senkou_a`/`senkou_b` are the raw lines and
  `chikou` equals `close`.
- `displacement` larger than the input → `senkou_a`/`senkou_b` are entirely
  undefined and `chikou` is entirely undefined.
- An empty input → five empty series.
- No value is ever defined before the indices above; do **not** back-fill the
  warm-up region.

## References

- Goichi Hosoda, *Ichimoku Kinko Hyo*.
- Standard technical-analysis definition. This spec **bakes the displacement
  into the returned arrays** (chart-aligned), the convention used by most
  charting platforms and their indicator functions.
