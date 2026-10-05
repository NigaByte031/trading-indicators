"""MACD is checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/macd.json`` so that this port and every future port (MQL5,
Pine Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from indicators import macd

from _vectors import is_undefined, load_cases

LINES = ("macd", "signal", "histogram")


@pytest.mark.parametrize("case", load_cases("macd"), ids=lambda case: case["name"])
def test_macd_matches_shared_vectors(case: Dict[str, Any]) -> None:
    params = case["parameters"]
    result = macd(
        case["input"]["close"],
        params["fast_period"],
        params["slow_period"],
        params["signal_period"],
    )

    for name in LINES:
        got_series = getattr(result, name)
        expected = case["expected"][name]
        assert len(got_series) == len(expected), name
        for got, want in zip(got_series, expected):
            if want is None:
                assert is_undefined(got), f"{name}: expected undefined"
            else:
                assert got == pytest.approx(want, abs=1e-6), name


def test_signal_is_undefined_no_later_than_the_histogram() -> None:
    result = macd([10, 12, 11, 13, 12, 14, 15, 13], 2, 3, 2)
    for i, value in enumerate(result.signal):
        assert (result.histogram[i] is None) == (value is None)


def test_histogram_is_macd_minus_signal() -> None:
    result = macd([10, 12, 11, 13, 12, 14, 15, 13], 2, 3, 2)
    for i in range(len(result.macd)):
        if result.signal[i] is not None:
            assert result.histogram[i] == pytest.approx(
                result.macd[i] - result.signal[i]
            )


def test_default_parameters_are_12_26_9() -> None:
    close = list(range(1, 61))
    result = macd(close)
    assert len(result.macd) == len(close)
    # The MACD line starts once the slower EMA (26) is seeded.
    assert result.macd[24] is None
    assert result.macd[25] is not None
    # The signal needs 9 more defined MACD values (index 25 + 8).
    assert result.signal[32] is None
    assert result.signal[33] is not None


def test_equal_fast_and_slow_give_a_flat_zero_line() -> None:
    result = macd([10, 12, 11, 13, 12], 2, 2, 2)
    defined = [value for value in result.macd if value is not None]
    assert defined and all(value == 0 for value in defined)


def test_every_line_has_the_same_length_as_the_input() -> None:
    close = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = macd(close, 2, 4, 2)
    for name in LINES:
        assert len(getattr(result, name)) == len(close), name


def test_empty_input_yields_empty_series() -> None:
    result = macd([], 2, 3, 2)
    for name in LINES:
        assert getattr(result, name) == []


@pytest.mark.parametrize("bad_period", [0, -1, -5])
def test_period_below_one_raises(bad_period: int) -> None:
    with pytest.raises(ValueError):
        macd([1, 2, 3, 4, 5], bad_period, 3, 2)


def test_non_integer_period_raises() -> None:
    with pytest.raises(TypeError):
        macd([1, 2, 3], 2.5, 3, 2)  # type: ignore[arg-type]
