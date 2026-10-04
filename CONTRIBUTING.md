# Contributing

Thanks for helping! The golden rule of this repository is:

> **The specification is the source of truth. Every language port must agree
> with it, and the agreement is proven by the shared test vectors.**

## Adding a new indicator

1. **Write the spec** — `specs/<slug>.md`, using the template in
   [`specs/README.md`](specs/README.md). It must define the formula, the
   parameters and their defaults, the output alignment (length, leading empty
   values) and any edge cases.
2. **Add test vectors** — `specs/vectors/<slug>.json` with a representative
   input series and the expected output. These numbers are the contract shared
   by every language.
3. **Implement the port** — in each language folder you support, e.g.
   `python/src/indicators/<slug>.py`.
4. **Test the port against the vectors** — do *not* hard-code expected values in
   the test; load the JSON from `specs/vectors/`. See
   `python/tests/test_ema.py` for the pattern.
5. **Update the matrix** in the root `README.md`.

## Adding a new language

Create a top-level folder for it (e.g. `pine/`, `mql5/`) and keep it
self-contained: its own build/tooling files, its own `README.md`, and a test
runner that reads the shared `specs/vectors/*.json`. Then add a column to the
matrix in the root `README.md`.

## Running the Python tests

```bash
cd python
python -m pytest
```

## Guidelines

- Prefer **zero runtime dependencies** for an implementation when practical.
- Keep an implementation a faithful, readable transcription of its spec — the
  same algorithm should look similar in every language.
- One indicator = one spec = one vector file = one file per language.
