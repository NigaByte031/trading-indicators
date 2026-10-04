"""Multi-language technical indicators — Python implementation.

Each indicator is a faithful port of its language-agnostic specification in
``specs/`` and is verified against the shared vectors in ``specs/vectors/``.
"""

from indicators.ema import ema

__all__ = ["ema"]
__version__ = "0.1.0"
