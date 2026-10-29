from __future__ import annotations

from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, InvalidOperation
from typing import Literal

Money = Decimal


class CalculationError(ValueError):
    pass


def decimal_odds(american: int) -> Decimal:
    if american == 0 or abs(american) < 100:
        raise CalculationError("American odds must have an absolute magnitude of at least 100.")
    return Decimal("1") + (Decimal(american) / 100 if american > 0 else Decimal(100) / abs(Decimal(american)))


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_hedge(
    odds: list[int], amount: Decimal, mode: Literal["budget", "fixed_first"] = "budget"
) -> dict:
    if len(odds) < 2:
        raise CalculationError("At least two mutually exclusive outcomes are required.")
    if amount <= 0:
        raise CalculationError("Amount must be greater than zero.")
    try:
        decimal_prices = [decimal_odds(price) for price in odds]
    except (InvalidOperation, ValueError) as error:
        raise CalculationError(str(error)) from error
    probability_sum = sum((Decimal("1") / price for price in decimal_prices), Decimal("0"))
    if mode == "budget":
        raw_stakes = [amount * (Decimal("1") / price) / probability_sum for price in decimal_prices]
        stakes = [money(stake) for stake in raw_stakes[:-1]]
        stakes.append(money(amount - sum(stakes, Decimal("0"))))
    else:
        first = amount
        payout_target = first * decimal_prices[0]
        stakes = [money(first)] + [money(payout_target / price) for price in decimal_prices[1:]]
    total_stake = sum(stakes, Decimal("0"))
    payouts = [money(stake * price) for stake, price in zip(stakes, decimal_prices)]
    profits = [money(payout - total_stake) for payout in payouts]
    minimum_profit = min(profits)
    return {
        "odds": odds,
        "decimal_odds": [str(price) for price in decimal_prices],
        "stakes": [str(stake) for stake in stakes],
        "total_stake": str(money(total_stake)),
        "payouts": [str(payout) for payout in payouts],
        "profits": [str(profit) for profit in profits],
        "minimum_profit": str(minimum_profit),
        "roi_percent": str(money((minimum_profit / total_stake * 100) if total_stake else Decimal("0"))),
        "is_theoretical_arb": probability_sum < Decimal("1"),
        "probability_sum": str(probability_sum),
    }
