from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from typing import Any

import httpx


@dataclass(frozen=True)
class ProviderStatus:
    configured: bool
    mode: str
    region: str
    credit_floor: int
    message: str


class OddsApiAdapter:
    """Bounded adapter for an explicitly supplied, permitted The Odds API key."""

    base_url = "https://api.the-odds-api.com/v4"

    def status(self) -> ProviderStatus:
        key = getenv("USHIO_ODDS_API_KEY", "")
        region = getenv("USHIO_ODDS_API_REGION", "ca")
        floor = int(getenv("USHIO_ODDS_API_CREDIT_FLOOR", "25"))
        return ProviderStatus(bool(key), "candidate-live" if key else "fixture", region, floor, "Refresh is disabled until a permitted key is supplied." if not key else "Explicit selected-market refresh only; source coverage is not Quebec eligibility.")

    def fetch_selected_market(self, sport: str, market: str) -> dict:
        status = self.status()
        if not status.configured:
            raise RuntimeError(status.message)
        response = httpx.get(f"{self.base_url}/sports/{sport}/odds", params={"apiKey": getenv("USHIO_ODDS_API_KEY"), "regions": status.region, "markets": market, "oddsFormat": "american"}, timeout=15)
        response.raise_for_status()
        remaining = int(response.headers.get("x-requests-remaining", "0"))
        if remaining < status.credit_floor:
            raise RuntimeError(f"Refresh paused: {remaining} credits remain, below the configured safety floor of {status.credit_floor}.")
        return normalise_odds_payload(response.json(), region=status.region, remaining=remaining)


def outcome_label(outcome: dict[str, Any]) -> str:
    """Make player/line identity explicit rather than matching generic Over/Under text."""
    description = str(outcome.get("description") or "").strip()
    name = str(outcome.get("name") or "").strip()
    point = outcome.get("point")
    parts = [part for part in (description, name, str(point) if point is not None else "") if part]
    return " ".join(parts)


def normalise_odds_payload(payload: list[dict[str, Any]], *, region: str, remaining: int) -> dict[str, Any]:
    """Convert only two-outcome, exact-market groups into the public comparison contract."""
    games: list[dict[str, Any]] = []
    for event in payload:
        seen_groups: set[tuple[str, tuple[str, ...]]] = set()
        for market in (market for book in event.get("bookmakers", []) for market in book.get("markets", [])):
            market_key = market.get("key")
            outcomes = market.get("outcomes", [])
            if not market_key or len(outcomes) != 2:
                continue
            outcome_names = [outcome_label(outcome) for outcome in outcomes]
            prices = [outcome.get("price") for outcome in outcomes]
            if not all(outcome_names) or not all(isinstance(price, (int, float)) and abs(price) >= 100 for price in prices):
                continue
            group_key = (str(market_key), tuple(outcome_names))
            if group_key in seen_groups:
                continue
            seen_groups.add(group_key)
            selected_books = []
            for book in event.get("bookmakers", []):
                matching = next((candidate for candidate in book.get("markets", []) if candidate.get("key") == market_key and [outcome_label(item) for item in candidate.get("outcomes", [])] == outcome_names), None)
                if matching is None:
                    continue
                book_prices = [item.get("price") for item in matching.get("outcomes", [])]
                if len(book_prices) == 2 and all(isinstance(price, (int, float)) and abs(price) >= 100 for price in book_prices):
                    selected_books.append({"book": book.get("title", book.get("key", "Unknown")), "prices": [int(book_prices[0]), int(book_prices[1])], "source_time": book.get("last_update") or matching.get("last_update")})
            if len(selected_books) >= 2:
                games.append({"id": f"{event.get('id', 'event')}:{market_key}:{':'.join(outcome_names)}", "sport": event.get("sport_key", "unknown"), "league": event.get("sport_title", event.get("sport_key", "Unknown")), "away": event.get("away_team", "Away"), "home": event.get("home_team", "Home"), "commence_time": event.get("commence_time"), "market": market_key, "period": "provider_declared", "outcomes": outcome_names, "quotes": selected_books})
    return {"mode": "live", "provider": "the-odds-api", "region": region, "as_of": None, "credit_state": {"status": "available", "remaining": remaining}, "capabilities": {"sports": [], "markets": [], "props": []}, "games": games}
