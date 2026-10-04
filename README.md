# trading-indicators

[![CI](https://github.com/NigaByte031/trading-indicators/actions/workflows/ci.yml/badge.svg)](https://github.com/NigaByte031/trading-indicators/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](python/)

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
├── .github/          # CI and GitHub templates
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
| RSI (Relative Strength Index) | [spec](specs/rsi.md) | [vectors](specs/vectors/rsi.json) | ✅ | – | – |
| ADX (Average Directional Index) | [spec](specs/adx.md) | [vectors](specs/vectors/adx.json) | ✅ | – | – |
| Ichimoku (Ichimoku Kinko Hyo) | [spec](specs/ichimoku.md) | [vectors](specs/vectors/ichimoku.json) | ✅ | – | – |
| Bollinger Bands (BB) | [spec](specs/bollinger.md) | [vectors](specs/vectors/bollinger.json) | ✅ | – | – |

Languages marked `–` are planned. Adding one means: read `specs/<name>.md`,
implement it, and check the output against `specs/vectors/<name>.json`.

## Development

The Python port is self-contained under [`python/`](python/) and has no runtime
dependencies (Python 3.9+).

```bash
cd python
python -m pytest        # run the suite against the shared vectors
ruff check .            # lint (pip install ruff, or pip install -e ".[dev]")
```

CI runs the test suite on Python 3.9–3.13 plus Ruff on every push and pull
request — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and our
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Notable changes are recorded in the
[`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE) © Mohammad Yazdani
