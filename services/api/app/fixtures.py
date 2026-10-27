from datetime import datetime, timezone

BOOKS = ["BetRivers (CA-ON)", "BetMGM (CA-ON)", "Betano (CA-ON)", "Sports Interaction", "Pinnacle"]


def fixture_board(sport: str = "icehockey_nhl", market: str = "h2h") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    games = [
        {"id": "nhl-mtl-tor", "sport": "icehockey_nhl", "league": "NHL", "away": "Montréal Canadiens", "home": "Toronto Maple Leafs", "commence_time": "2026-10-28T23:00:00Z", "market": "h2h", "period": "full_game", "outcomes": ["Montréal Canadiens", "Toronto Maple Leafs"], "quotes": [{"book": BOOKS[0], "prices": [-110, -105]}, {"book": BOOKS[1], "prices": [-108, -112]}, {"book": BOOKS[2], "prices": [115, -135]}, {"book": BOOKS[3], "prices": [-105, -115]}, {"book": BOOKS[4], "prices": [-102, -118]}]},
        {"id": "nhl-van-edm", "sport": "icehockey_nhl", "league": "NHL", "away": "Vancouver Canucks", "home": "Edmonton Oilers", "commence_time": "2026-10-29T00:30:00Z", "market": "h2h", "period": "full_game", "outcomes": ["Vancouver Canucks", "Edmonton Oilers"], "quotes": [{"book": BOOKS[0], "prices": [120, -140]}, {"book": BOOKS[1], "prices": [125, -145]}, {"book": BOOKS[2], "prices": [130, -150]}, {"book": BOOKS[3], "prices": [118, -138]}, {"book": BOOKS[4], "prices": [122, -142]}]},
        {"id": "nba-bos-ny", "sport": "basketball_nba", "league": "NBA", "away": "Boston Celtics", "home": "New York Knicks", "commence_time": "2026-10-29T00:00:00Z", "market": "h2h", "period": "full_game", "outcomes": ["Boston Celtics", "New York Knicks"], "quotes": [{"book": BOOKS[0], "prices": [-110, -110]}, {"book": BOOKS[1], "prices": [-112, -108]}, {"book": BOOKS[2], "prices": [-105, -115]}, {"book": BOOKS[3], "prices": [-108, -112]}, {"book": BOOKS[4], "prices": [-107, -113]}]},
        {"id": "nba-bos-ny-tatum-points", "sport": "basketball_nba", "league": "NBA", "away": "Boston Celtics", "home": "New York Knicks", "commence_time": "2026-10-29T00:00:00Z", "market": "player_points", "period": "full_game", "outcomes": ["Jayson Tatum over 27.5 points", "Jayson Tatum under 27.5 points"], "quotes": [{"book": BOOKS[0], "prices": [-110, -110]}, {"book": BOOKS[1], "prices": [-105, -115]}, {"book": BOOKS[2], "prices": [110, -130]}, {"book": BOOKS[3], "prices": [-108, -112]}, {"book": BOOKS[4], "prices": [-102, -118]}]},
    ]
    return {"mode": "fixture", "provider": "deterministic-fixture", "region": "ca", "as_of": now, "credit_state": {"status": "fixture", "remaining": None}, "capabilities": {"sports": ["icehockey_nhl", "basketball_nba"], "markets": ["h2h", "spreads", "totals"], "props": ["player_points"]}, "games": [game for game in games if (sport == "all" or game["sport"] == sport) and (market == "all" or game["market"] == market)]}
