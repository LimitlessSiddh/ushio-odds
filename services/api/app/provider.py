from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from typing import Any

import httpx

from .books import canonical_selected_book, region_status
from .quote_lifecycle import QuoteLifecycleError, ingest_market_observations


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


def coverage_summary(payload: list[dict[str, Any]]) -> dict[str, Any]:
    """Return request-level, non-secret coverage diagnostics for a bounded payload."""
    titles: set[str] = set()
    keys: set[str] = set()
    selected_titles: dict[str, set[str]] = {}
    source_times: list[str] = []
    rejected = {"unknown_book": 0, "excluded_book": 0, "invalid_two_way_market": 0, "missing_price_or_identity": 0, "one_eligible_book": 0}
    bookmaker_count = market_count = 0
    for event in payload:
        for book in event.get("bookmakers", []):
            bookmaker_count += 1
            title = str(book.get("title") or book.get("key") or "unnamed-book")
            titles.add(title)
            canonical = canonical_selected_book(title)
            if canonical is None:
                rejected["unknown_book"] += 1
            elif region_status(canonical) == "excluded":
                rejected["excluded_book"] += 1
            else:
                selected_titles.setdefault(canonical, set()).add(title)
            if isinstance(book.get("last_update"), str):
                source_times.append(book["last_update"])
            for market in book.get("markets", []):
                market_count += 1
                if market.get("key"):
                    keys.add(str(market["key"]))
                if isinstance(market.get("last_update"), str):
                    source_times.append(market["last_update"])
    return {
        "raw_event_count": len(payload),
        "raw_bookmaker_count": bookmaker_count,
        "raw_bookmaker_titles": sorted(titles),
        "raw_market_count": market_count,
        "raw_market_keys": sorted(keys),
        "selected_book_title_matches": {canonical: sorted(values) for canonical, values in sorted(selected_titles.items())},
        "rejection_counts": rejected,
        "source_timing": {"available": bool(source_times), "timestamp_count": len(source_times), "earliest": min(source_times) if source_times else None, "latest": max(source_times) if source_times else None},
    }


def normalise_odds_payload(payload: list[dict[str, Any]], *, region: str, remaining: int) -> dict[str, Any]:
    """Convert only two-outcome, exact-market groups into the public comparison contract."""
    games: list[dict[str, Any]] = []
    coverage = coverage_summary(payload)
    for event in payload:
        seen_groups: set[tuple[str, tuple[str, ...]]] = set()
        for market in (market for book in event.get("bookmakers", []) for market in book.get("markets", [])):
            market_key = market.get("key")
            outcomes = market.get("outcomes", [])
            if not market_key or len(outcomes) != 2:
                coverage["rejection_counts"]["invalid_two_way_market"] += 1
                continue
            outcome_names = [outcome_label(outcome) for outcome in outcomes]
            prices = [outcome.get("price") for outcome in outcomes]
            if not all(outcome_names) or not all(isinstance(price, (int, float)) and abs(price) >= 100 for price in prices):
                coverage["rejection_counts"]["missing_price_or_identity"] += 1
                continue
            group_key = (str(market_key), tuple(outcome_names))
            if group_key in seen_groups:
                continue
            seen_groups.add(group_key)
            selected_books = []
            for book in event.get("bookmakers", []):
                selected_book = canonical_selected_book(book.get("title", book.get("key", "")))
                if selected_book is None or region_status(selected_book) == "excluded":
                    continue
                matching = next((candidate for candidate in book.get("markets", []) if candidate.get("key") == market_key and [outcome_label(item) for item in candidate.get("outcomes", [])] == outcome_names), None)
                if matching is None:
                    continue
                book_prices = [item.get("price") for item in matching.get("outcomes", [])]
                if len(book_prices) == 2 and all(isinstance(price, (int, float)) and abs(price) >= 100 for price in book_prices):
                    selected_books.append({"book": selected_book, "prices": [int(book_prices[0]), int(book_prices[1])], "source_time": book.get("last_update") or matching.get("last_update"), "region_status": region_status(selected_book)})
            if len(selected_books) >= 2:
                games.append({"id": f"{event.get('id', 'event')}:{market_key}:{':'.join(outcome_names)}", "sport": event.get("sport_key", "unknown"), "league": event.get("sport_title", event.get("sport_key", "Unknown")), "away": event.get("away_team", "Away"), "home": event.get("home_team", "Home"), "commence_time": event.get("commence_time"), "market": market_key, "period": "provider_declared", "outcomes": outcome_names, "quotes": selected_books})
            else:
                coverage["rejection_counts"]["one_eligible_book"] += 1
    coverage["normalized_event_count"] = len({game["id"].split(":", 1)[0] for game in games})
    coverage["accepted_market_count"] = len(games)
    return {"mode": "live", "provider": "the-odds-api", "region": region, "as_of": None, "credit_state": {"status": "available", "remaining": remaining}, "capabilities": {"sports": [], "markets": [], "props": []}, "games": games, "coverage_summary": coverage}


def persist_validated_provider_market(session: Any, observations: list[dict[str, Any]], *, received_at: Any, ttl_seconds: int = 90) -> list[Any]:
    """Persist only a complete, explicitly normalized two-way provider market.

    Raw provider boards are intentionally not passed here: a fetch alone lacks
    settlement semantics and must remain provider-observed rather than revalidated.
    """
    required = {"provider", "region", "book", "event_id", "sport", "league", "away", "home", "market", "period", "settlement_assumptions", "outcome", "position", "price", "source_timestamp", "quote_status"}
    normalized: list[dict[str, Any]] = []
    for observation in observations:
        missing = sorted(field for field in required if observation.get(field) in (None, ""))
        if missing:
            raise QuoteLifecycleError(f"Provider observation is incomplete: {', '.join(missing)}.")
        if observation.get("quote_status") != "active":
            raise QuoteLifecycleError("Only explicitly active provider observations are supported for candidate revalidation.")
        if observation.get("fee") not in (None, 0, "0", "0.00") or observation.get("fx") not in (None, "CAD"):
            raise QuoteLifecycleError("Provider observations with fees or FX are unsupported and cannot be revalidated.")
        accepted = dict(observation)
        accepted["status"] = accepted.pop("quote_status")
        normalized.append(accepted)
    return ingest_market_observations(session, normalized, received_at=received_at, ttl_seconds=ttl_seconds)
