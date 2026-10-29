from __future__ import annotations

from typing import Literal

RegionStatus = Literal["unknown", "unresolved", "excluded"]

# This is a scope allow-list, not a statement of legal eligibility or account readiness.
SELECTED_BOOKS = (
    "Mise-o-jeu+", "bet365", "Sports Interaction", "BET99", "Stake", "Betway",
    "TonyBet", "BetVictor", "ToonieBet", "PowerPlay", "Rainbet",
)
BOOK_REGION_STATUS: dict[str, RegionStatus] = {
    "TonyBet": "unresolved",
    "ToonieBet": "excluded",
}


def canonical_selected_book(raw_name: object) -> str | None:
    """Return the selected identity for a provider label, never an unselected book."""
    normalized = "".join(character for character in str(raw_name).lower() if character.isalnum())
    aliases = {
        "miseojeu": "Mise-o-jeu+", "miseojeuplus": "Mise-o-jeu+", "bet365": "bet365",
        "sportsinteraction": "Sports Interaction", "sia": "Sports Interaction", "bet99": "BET99",
        "stake": "Stake", "betway": "Betway", "tonybet": "TonyBet", "betvictor": "BetVictor",
        "tooniebet": "ToonieBet", "powerplay": "PowerPlay", "rainbet": "Rainbet",
    }
    return aliases.get(normalized)


def region_status(book: str) -> RegionStatus:
    return BOOK_REGION_STATUS.get(book, "unknown")
