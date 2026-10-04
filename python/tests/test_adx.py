"""ADX is checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/adx.json`` so that this port and every future port (MQL5, Pine
Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from indicators import adx

from _vectors import is_undefined, load_cases


@pytest.mark.parametrize("case", load_cases("adx"), ids=lambda case: case["name"])
def test_adx_matches_shared_vectors(case: Dict[str, Any]) -> None:
    params = case["parameters"]
    result = adx(
        case["input"]["high"],
        case["input"]["low"],
        case["input"]["close"],
        params["period"],
    )
    expected = case["expected"]["adx"]

    assert len(result) == len(expected)
    for got, want in zip(result, expected):
        if want is None:
            assert is_undefined(got), f"expected undefined, got {got!r}"
        else:
            assert got == pytest.approx(want, abs=1e-6)


def test_output_length_matches_input() -> None:
    high = [1, 2, 3, 4, 5, 6]
    low = [0, 1, 2, 3, 4, 5]
    close = [1, 2, 3, 4, 5, 6]
    assert len(adx(high, low, close, 2)) == len(high)


def test_strong_uptrend_converges_to_100() -> None:
    # Every bar makes a higher high and a higher low with no downward move, so
    # -DI is 0 and DX == 100 on every defined bar.
    n = 10
    high = [10.0 + i for i in range(n)]
    low = [9.0 + i for i in range(n)]
    close = [9.5 + i for i in range(n)]
    result = adx(high, low, close, 3)
    assert is_undefined(result[4]) is False
    assert result[4] == pytest.approx(100.0)
    assert result[-1] == pytest.approx(100.0)


def test_empty_input_yields_empty_output() -> None:
    assert adx([], [], [], 3) == []


def test_mismatched_lengths_raise() -> None:
    with pytest.raises(ValueError):
        adx([1, 2, 3], [1, 2], [1, 2, 3], 2)


@pytest.mark.parametrize("bad_period", [0, -1, -5])
def test_period_below_one_raises(bad_period: int) -> None:
    with pytest.raises(ValueError):
        adx([1, 2, 3], [1, 2, 3], [1, 2, 3], bad_period)


def test_non_integer_period_raises() -> None:
    with pytest.raises(TypeError):
        adx([1, 2, 3], [1, 2, 3], [1, 2, 3], 2.5)  # type: ignore[arg-type]
