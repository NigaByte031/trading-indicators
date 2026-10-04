"""Shared helpers for loading the language-agnostic test vectors.

Every test module reads its expected values from ``specs/vectors/<slug>.json``
instead of hard-coding them, so all language ports are checked against a single
contract. Keeping that loading logic here means each test file stays focused on
the behaviour it verifies.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

VECTORS_DIR = Path(__file__).resolve().parents[2] / "specs" / "vectors"


def load_cases(slug: str) -> List[Dict[str, Any]]:
    """Return the ``cases`` array of ``specs/vectors/<slug>.json``."""
    path = VECTORS_DIR / f"{slug}.json"
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def is_undefined(value: Optional[float]) -> bool:
    """True when a produced value counts as undefined (``None`` or NaN)."""
    return value is None or (isinstance(value, float) and math.isnan(value))
