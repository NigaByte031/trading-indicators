"""SMA is checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/sma.json`` so that this port and every future port (MQL5, Pine
Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from indicators import sma

from _vectors import is_undefined, load_cases


@pytest.mark.parametrize("case", load_cases("sma"), ids=lambda case: case["name"])
def test_sma_matches_shared_vectors(case: Dict[str, Any]) -> None:
    result = sma(case["input"]["close"], case["parameters"]["period"])
    expected = case["expected"]["sma"]

    assert len(result) == len(expected)
    for got, want in zip(result, expected):
        if want is None:
            assert is_undefined(got), f"expected undefined, got {got!r}"
        else:
            assert got == pytest.approx(want, abs=1e-9)


def test_warmup_region_is_never_backfilled() -> None:
    result = sma([1, 2, 3, 4, 5], 3)
    assert result[0] is None
    assert result[1] is None
    assert result[2:] == pytest.approx([2.0, 3.0, 4.0])


def test_window_mean_is_correct() -> None:
    assert sma([1, 2, 3, 4], 2) == pytest.approx([None, 1.5, 2.5, 3.5])


def test_output_length_matches_input() -> None:
    close = [3, 1, 4, 1, 5, 9, 2, 6]
    assert len(sma(close, 4)) == len(close)


def test_empty_input_yields_empty_output() -> None:
    assert sma([], 3) == []


@pytest.mark.parametrize("bad_period", [0, -1, -5])
def test_period_below_one_raises(bad_period: int) -> None:
    with pytest.raises(ValueError):
        sma([1, 2, 3], bad_period)


def test_non_integer_period_raises() -> None:
    with pytest.raises(TypeError):
        sma([1, 2, 3], 2.5)  # type: ignore[arg-type]
