"""Bollinger Bands are checked against the shared, language-agnostic vectors.

The expected values are never hard-coded here: they are read from
``specs/vectors/bollinger.json`` so that this port and every future port (MQL5,
Pine Script, ...) are validated against the exact same contract.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from indicators import bollinger

from _vectors import is_undefined, load_cases

LINES = ("middle", "upper", "lower")


@pytest.mark.parametrize(
    "case", load_cases("bollinger"), ids=lambda case: case["name"]
)
def test_bollinger_matches_shared_vectors(case: Dict[str, Any]) -> None:
    params = case["parameters"]
    result = bollinger(
        case["input"]["close"], params["period"], params["num_std"]
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


def test_warmup_region_is_never_backfilled() -> None:
    result = bollinger([1, 2, 3, 4, 5], 3, 2)
    for name in LINES:
        line = getattr(result, name)
        assert line[0] is None
        assert line[1] is None


def test_bands_are_symmetric_around_the_middle() -> None:
    result = bollinger([10, 12, 11, 13, 12], 3, 2)
    for i in range(len(result.middle)):
        if result.middle[i] is not None:
            width = result.upper[i] - result.middle[i]
            assert width == pytest.approx(result.middle[i] - result.lower[i])


def test_num_std_zero_collapses_the_bands() -> None:
    result = bollinger([2, 4, 4, 4, 5], 3, 0)
    assert result.upper == result.middle
    assert result.lower == result.middle


def test_period_one_equals_the_input() -> None:
    close = [3, 1, 4, 1, 5]
    result = bollinger(close, 1, 2)
    assert result.middle == pytest.approx(close)
    assert result.upper == pytest.approx(close)
    assert result.lower == pytest.approx(close)


def test_every_line_has_the_same_length_as_the_input() -> None:
    close = [3, 1, 4, 1, 5, 9, 2, 6]
    result = bollinger(close, 4, 2)
    for name in LINES:
        assert len(getattr(result, name)) == len(close), name


def test_empty_input_yields_empty_series() -> None:
    result = bollinger([], 5, 2)
    for name in LINES:
        assert getattr(result, name) == []


@pytest.mark.parametrize("bad_period", [0, -1, -5])
def test_period_below_one_raises(bad_period: int) -> None:
    with pytest.raises(ValueError):
        bollinger([1, 2, 3], bad_period, 2)


def test_negative_num_std_raises() -> None:
    with pytest.raises(ValueError):
        bollinger([1, 2, 3], 2, -1)


def test_non_numeric_num_std_raises() -> None:
    with pytest.raises(TypeError):
        bollinger([1, 2, 3], 2, "wide")  # type: ignore[arg-type]


def test_non_integer_period_raises() -> None:
    with pytest.raises(TypeError):
        bollinger([1, 2, 3], 2.5, 2)  # type: ignore[arg-type]
