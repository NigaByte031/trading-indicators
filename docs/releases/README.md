# Release notes

One file per release tag: `docs/releases/<tag>.md` (for example
`docs/releases/v0.2.0.md`).

Pushing a `v*` tag runs
[`.github/workflows/release.yml`](../../.github/workflows/release.yml), which
tests the tagged commit and publishes the matching file here as the GitHub
release body — so **these files are the canonical release notes**, not a
duplicate of `CHANGELOG.md`. The changelog stays terse and complete; the release
notes here explain what changed and why it matters.

## Releases

| Tag | Date | Highlight |
|-----|------|-----------|
| [v0.2.0](v0.2.0.md) | 2026-10-06 | RSI, Bollinger Bands and MACD; CI, lint and release automation |
| [v0.1.0](v0.1.0.md) | 2026-10-04 | The spec-first scaffold, plus SMA, EMA, ADX and Ichimoku |

## Writing a release

1. Finish the release in `CHANGELOG.md`: move the entries from `[Unreleased]`
   into a new `## [x.y.z] - YYYY-MM-DD` section, and reset `[Unreleased]`.
2. Bump `python/src/indicators/_version.py` — the only place the version lives.
3. Add `docs/releases/vX.Y.Z.md` (copy the structure of an older release).
4. Commit, then `git tag -a vX.Y.Z -m "vX.Y.Z"` and `git push origin main --tags`.
