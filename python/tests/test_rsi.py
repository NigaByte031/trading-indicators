"""RSI is checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/rsi.json`` so that this port and every future port (MQL5, Pine
Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from indicators import rsi

from _vectors import is_undefined, load_cases


@pytest.mark.parametrize("case", load_cases("rsi"), ids=lambda case: case["name"])
def test_rsi_matches_shared_vectors(case: Dict[str, Any]) -> None:
    result = rsi(case["input"]["close"], case["parameters"]["period"])
    expected = case["expected"]["rsi"]

    assert len(result) == len(expected)
    for got, want in zip(result, expected):
        if want is None:
            assert is_undefined(got), f"expected undefined, got {got!r}"
        else:
            assert got == pytest.approx(want, abs=1e-6)


def test_warmup_region_is_never_backfilled() -> None:
    result = rsi([44.34, 44.09, 44.15, 43.61], 3)
    assert result[0] is None
    assert result[1] is None
    assert result[2] is None
    assert result[3] == pytest.approx(7.058824, abs=1e-6)


def test_defined_values_stay_within_zero_and_one_hundred() -> None:
    close = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42]
    for value in rsi(close, 3):
        if value is not None:
            assert 0.0 <= value <= 100.0


def test_rising_series_saturates_at_one_hundred() -> None:
    close = [1, 2, 3, 4, 5, 6]
    result = rsi(close, 3)
    assert result[3:] == pytest.approx([100.0, 100.0, 100.0])


def test_output_length_matches_input() -> None:
    close = [3, 1, 4, 1, 5, 9, 2, 6]
    assert len(rsi(close, 4)) == len(close)


def test_empty_input_yields_empty_output() -> None:
    assert rsi([], 3) == []


@pytest.mark.parametrize("bad_period", [0, -1, -5])
def test_period_below_one_raises(bad_period: int) -> None:
    with pytest.raises(ValueError):
        rsi([1, 2, 3], bad_period)


def test_non_integer_period_raises() -> None:
    with pytest.raises(TypeError):
        rsi([1, 2, 3], 2.5)  # type: ignore[arg-type]
