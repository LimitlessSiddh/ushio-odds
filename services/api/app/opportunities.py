from __future__ import annotations

from decimal import Decimal
from typing import Any

from .domain import CalculationError, calculate_hedge


def detect_two_way_opportunities(games: list[dict[str, Any]], budget: Decimal = Decimal("250")) -> list[dict[str, Any]]:
    """Return only complete two-outcome pairs whose legs come from different books."""
    opportunities: list[dict[str, Any]] = []
    for game in games:
        if len(game.get("outcomes", [])) != 2:
            continue
        quotes = game.get("quotes", [])
        best: tuple[dict[str, Any], list[int]] | None = None
        for first in quotes:
            for second in quotes:
                if first.get("book") == second.get("book"):
                    continue
                if first.get("region_status") == "excluded" or second.get("region_status") == "excluded":
                    continue
                prices = [first.get("prices", [None, None])[0], second.get("prices", [None, None])[1]]
                if not all(isinstance(price, int) for price in prices):
                    continue
                try:
                    result = calculate_hedge(prices, budget)
                except CalculationError:
                    continue
                if not result["is_theoretical_arb"]:
                    continue
                if best is None or Decimal(result["minimum_profit"]) > Decimal(best[0]["minimum_profit"]):
                    best = (result, prices, first.get("quote_version_ids", []), second.get("quote_version_ids", []))
                    best_books = [first["book"], second["book"]]
        if best is not None:
            result, prices, first_versions, second_versions = best
            opportunities.append({"event_id": game["id"], "event": f"{game['away']} / {game['home']}", "market": game["market"], "period": game.get("period"), "line": game.get("line"), "outcomes": game["outcomes"], "books": best_books, "odds": prices, "selected_quote_version_ids": [first_versions[0], second_versions[1]] if len(first_versions) == 2 and len(second_versions) == 2 else [], "calculation_inputs": {"odds": prices, "budget": str(budget)}, "minimum_profit": result["minimum_profit"], "roi_percent": result["roi_percent"], "mode": "indicative"})
    return sorted(opportunities, key=lambda row: Decimal(row["roi_percent"]), reverse=True)
