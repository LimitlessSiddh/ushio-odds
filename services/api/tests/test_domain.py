from decimal import Decimal

import pytest
from hypothesis import given, strategies as st

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


valid_american_odds = st.one_of(st.integers(min_value=-1000, max_value=-100), st.integers(min_value=100, max_value=1000))


@given(first=valid_american_odds, second=valid_american_odds, budget=st.decimals(min_value="1.00", max_value="10000.00", places=2))
def test_budget_mode_conserves_cents_and_returns_finite_result(first: int, second: int, budget: Decimal) -> None:
    result = calculate_hedge([first, second], budget, "budget")
    assert sum((Decimal(stake) for stake in result["stakes"]), Decimal("0")) == budget
    assert len(result["profits"]) == 2
    assert all(Decimal(profit).is_finite() for profit in result["profits"])
