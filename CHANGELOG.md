# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Nothing yet._

## [0.2.0] - 2026-10-06

The "common indicator set" release: the repository now covers the indicators
most charting platforms ship with, and the surrounding engineering scaffolding
is in place. See [`docs/releases/v0.2.0.md`](docs/releases/v0.2.0.md) for the
full release notes.

### Added

- **RSI** — Relative Strength Index, using Wilder's smoothing and the
  simple-average seed, with the flat-market (100) and all-down (0) edges
  defined in the spec.
- **Bollinger Bands** — a moving average with upper/lower bands `num_std`
  *population* standard deviations away.
- **MACD** — Moving Average Convergence Divergence: the fast/slow EMA spread,
  its signal EMA and the histogram, with the warm-up boundary
  (`slow + signal - 2`) fixed by the spec.
- Continuous integration: the Python test suite runs on Python 3.9–3.13, plus a
  Ruff lint job.
- A release workflow that publishes the notes in `docs/releases/<tag>.md` when a
  `v*` tag is pushed.
- `CODE_OF_CONDUCT.md`, `CITATION.cff`, pull-request and issue templates.
- Shared test helpers (`python/tests/_vectors.py`) so every test loads the
  language-agnostic vectors from `specs/vectors/` in one place.

### Changed

- The Python version is now defined once, in
  `python/src/indicators/_version.py`; the build reads it through
  `[tool.setuptools.dynamic]` instead of repeating the number in
  `pyproject.toml`.
- Root `README.md` gained badges, a development section and links to the
  changelog, release notes and code of conduct.

## [0.1.0] - 2026-10-04

The initial scaffold plus the first four indicators. See
[`docs/releases/v0.1.0.md`](docs/releases/v0.1.0.md).

### Added

- Repository scaffold: language-agnostic specs in `specs/` with shared JSON test
  vectors in `specs/vectors/`, and a self-contained Python port under `python/`.
- EMA — Exponential Moving Average, seeded with the SMA of the first `period`
  values.
- SMA / MA — Simple Moving Average.
- ADX — Average Directional Index built on Wilder's smoothing.
- Ichimoku Kinko Hyo — Tenkan, Kijun, Senkou Span A/B and Chikou, with the
  displacement baked into the returned series.

[Unreleased]: https://github.com/NigaByte031/trading-indicators/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/NigaByte031/trading-indicators/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/NigaByte031/trading-indicators/releases/tag/v0.1.0
