# Python

The Python implementation of the indicators in this repository.

## Layout

```
python/
├── pyproject.toml
├── src/indicators/     # the package
│   ├── adx.py
│   ├── ema.py
│   └── sma.py
└── tests/              # reads the shared vectors from ../../specs/vectors
```

## Requirements

- Python 3.9+
- No runtime dependencies
- `pytest` for the tests

## Running the tests

```bash
cd python
python -m pytest
```

The tests load the shared, language-agnostic vectors from
`specs/vectors/*.json`, so passing them means this port agrees with every other
language in the repository.

## Trying it out

```python
from indicators import adx, ema, sma

ema([10, 12, 11, 13, 12, 14, 15, 13], 4)
# [None, None, None, 11.5, 11.7, 12.62, 13.572, 13.3432]

sma([10, 12, 11, 13, 12, 14, 15, 13], 4)
# [None, None, None, 11.5, 12.0, 12.5, 13.5, 13.5]

adx(high, low, close, 14)
# Wilder-smoothed ADX; the first 2 * period - 2 values are None
```
