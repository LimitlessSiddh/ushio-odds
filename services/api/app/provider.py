from __future__ import annotations

from dataclasses import dataclass
from os import getenv

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
        return {"payload": response.json(), "remaining": remaining, "region": status.region}
