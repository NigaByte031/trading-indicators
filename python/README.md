# Python

The Python implementation of the indicators in this repository.

## Layout

```
python/
├── pyproject.toml
├── src/indicators/     # the package
│   └── ema.py
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
from indicators import ema

ema([10, 12, 11, 13, 12, 14, 15, 13], 4)
# [None, None, None, 11.5, 11.7, 12.62, 13.572, 13.3432]
```
