# trading-indicators

A multi-language collection of technical indicators.

Every indicator lives in a **language-agnostic specification** under
[`specs/`](specs/) together with shared **test vectors**. Each language then
*ports* that specification, and its test suite is checked against the very same
vectors — so the Python, MQL5, Pine Script, … versions can never silently drift
apart.

## Why a single repository?

The value here is **parity**: the same indicator, in several languages. Fixing a
formula or a bug must update every port in one commit, and the ports must be
verified against a shared source of truth. That is exactly what a monorepo plus
`specs/vectors` gives us.

## Repository layout

```
trading-indicators/
├── specs/            # ⭐ the single source of truth (language-agnostic)
│   ├── <indicator>.md
│   └── vectors/      # shared input → expected output, in JSON
├── docs/             # formulas, screenshots, background
├── python/           # one self-contained folder per language
│   ├── pyproject.toml
│   ├── src/indicators/
│   └── tests/
└── <other languages>/  # added over time
```

Each language folder is **self-contained**: its own tooling, config and tests.
Rules for the shared format live in [`specs/README.md`](specs/README.md).

## Indicators

| Indicator | Spec | Test vectors | Python | MQL5 | Pine Script |
|-----------|------|--------------|:------:|:----:|:-----------:|
| SMA / MA (Simple Moving Average) | [spec](specs/sma.md) | [vectors](specs/vectors/sma.json) | ✅ | – | – |
| EMA (Exponential Moving Average) | [spec](specs/ema.md) | [vectors](specs/vectors/ema.json) | ✅ | – | – |
| ADX (Average Directional Index) | [spec](specs/adx.md) | [vectors](specs/vectors/adx.json) | ✅ | – | – |
| Ichimoku (Ichimoku Kinko Hyo) | [spec](specs/ichimoku.md) | [vectors](specs/vectors/ichimoku.json) | ✅ | – | – |

Languages marked `–` are planned. Adding one means: read `specs/<name>.md`,
implement it, and check the output against `specs/vectors/<name>.json`.

## Python

```bash
cd python
python -m pytest
```

Requires Python 3.9+ and `pytest` (no runtime dependencies).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE) © Mohammad Yazdani
