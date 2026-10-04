# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- RSI — Relative Strength Index, with Wilder's smoothing and the simple-average
  seed.

- Continuous integration: the Python test suite runs on Python 3.9–3.13, plus a
  Ruff lint job.
- `CODE_OF_CONDUCT.md`, `CITATION.cff`, pull-request and issue templates.
- Shared test helpers (`python/tests/_vectors.py`) so every test loads the
  language-agnostic vectors from `specs/vectors/` in one place.

## [0.1.0] - 2026-10-04

### Added

- Repository scaffold: language-agnostic specs in `specs/` with shared JSON test
  vectors in `specs/vectors/`, and a self-contained Python port under `python/`.
- EMA — Exponential Moving Average, seeded with the SMA of the first `period`
  values.
- SMA / MA — Simple Moving Average.
- ADX — Average Directional Index built on Wilder's smoothing.
- Ichimoku Kinko Hyo — Tenkan, Kijun, Senkou Span A/B and Chikou, with the
  displacement baked into the returned series.

[Unreleased]: https://github.com/NigaByte031/trading-indicators/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/NigaByte031/trading-indicators/releases/tag/v0.1.0
