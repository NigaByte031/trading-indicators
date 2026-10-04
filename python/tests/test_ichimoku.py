"""Ichimoku is checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/ichimoku.json`` so that this port and every future port (MQL5,
Pine Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from indicators import ichimoku

VECTORS_PATH = (
    Path(__file__).resolve().parents[2] / "specs" / "vectors" / "ichimoku.json"
)

LINES = ("tenkan", "kijun", "senkou_a", "senkou_b", "chikou")


def _load_cases() -> List[Dict[str, Any]]:
    return json.loads(VECTORS_PATH.read_text(encoding="utf-8"))["cases"]


def _is_undefined(value: Optional[float]) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def _line(result: Any, name: str) -> List[Optional[float]]:
    return getattr(result, name)


@pytest.mark.parametrize("case", _load_cases(), ids=lambda case: case["name"])
def test_ichimoku_matches_shared_vectors(case: Dict[str, Any]) -> None:
    params = case["parameters"]
    result = ichimoku(
        case["input"]["high"],
        case["input"]["low"],
        case["input"]["close"],
        params["conversion"],
        params["base"],
        params["span_b"],
        params["displacement"],
    )

    for name in LINES:
        got_series = _line(result, name)
        expected = case["expected"][name]
        assert len(got_series) == len(expected), name
        for got, want in zip(got_series, expected):
            if want is None:
                assert _is_undefined(got), f"{name}: expected undefined, got {got!r}"
            else:
                assert got == pytest.approx(want, abs=1e-9), name


def test_chikou_is_the_close_shifted_back_by_the_displacement() -> None:
    close = [1, 2, 3, 4, 5, 6]
    result = ichimoku(close, close, close, conversion=1, base=1, span_b=1, displacement=2)
    assert result.chikou == pytest.approx([3, 4, 5, 6, None, None])


def test_displacement_zero_keeps_chikou_equal_to_close() -> None:
    close = [1, 2, 3, 4]
    result = ichimoku(close, close, close, conversion=1, base=1, span_b=1, displacement=0)
    assert result.chikou == pytest.approx([1, 2, 3, 4])


def test_default_parameters_are_the_classic_9_26_52_26() -> None:
    import inspect

    signature = inspect.signature(ichimoku)
    assert signature.parameters["conversion"].default == 9
    assert signature.parameters["base"].default == 26
    assert signature.parameters["span_b"].default == 52
    assert signature.parameters["displacement"].default == 26


def test_every_line_has_the_same_length_as_the_input() -> None:
    high = [1, 2, 3, 4, 5, 6, 7, 8]
    low = [0, 1, 2, 3, 4, 5, 6, 7]
    close = [1, 2, 3, 4, 5, 6, 7, 8]
    result = ichimoku(high, low, close, conversion=3, base=4, span_b=5, displacement=2)
    for name in LINES:
        assert len(_line(result, name)) == len(high), name


def test_empty_input_yields_empty_series() -> None:
    result = ichimoku([], [], [])
    for name in LINES:
        assert _line(result, name) == []


def test_mismatched_lengths_raise() -> None:
    with pytest.raises(ValueError):
        ichimoku([1, 2, 3], [1, 2], [1, 2, 3])


@pytest.mark.parametrize("name", ["conversion", "base", "span_b"])
@pytest.mark.parametrize("bad", [0, -1, -5])
def test_period_below_one_raises(name: str, bad: int) -> None:
    kwargs = {"conversion": 1, "base": 1, "span_b": 1, name: bad}
    with pytest.raises(ValueError):
        ichimoku([1, 2, 3], [1, 2, 3], [1, 2, 3], **kwargs)


def test_negative_displacement_raises() -> None:
    with pytest.raises(ValueError):
        ichimoku([1, 2, 3], [1, 2, 3], [1, 2, 3], displacement=-1)


def test_non_integer_parameters_raise() -> None:
    with pytest.raises(TypeError):
        ichimoku([1, 2, 3], [1, 2, 3], [1, 2, 3], conversion=2.5)  # type: ignore[arg-type]
