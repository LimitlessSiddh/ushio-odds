from decimal import Decimal

import pytest

from app.domain import CalculationError, calculate_hedge, decimal_odds


def test_reference_fixed_leg_vector() -> None:
    result = calculate_hedge([-110, 115], Decimal("1000"), "fixed_first")
    assert result["stakes"] == ["1000.00", "887.95"]
    assert Decimal(result["minimum_profit"]) >= Decimal("21.14")


def test_non_arb_is_not_marked_positive() -> None:
    result = calculate_hedge([-110, -110], Decimal("250"))
    assert result["is_theoretical_arb"] is False
    assert Decimal(result["minimum_profit"]) < 0


@pytest.mark.parametrize("odds", [0, 99, -99])
def test_invalid_american_odds_rejected(odds: int) -> None:
    with pytest.raises(CalculationError):
        decimal_odds(odds)
