from bets import Bet


def try_to_add_bet_to_bets(bets, home_name, away_name, away_odds, tie_odds, home_odds, provider, time, sport=''):
    if home_odds == 0 or away_odds == 0:
        return False
    if bets.get(str(time)) is None:
        bets[str(time)] = []
    bets[str(time)].append(
        Bet.Bet(
            home_name, away_name,
            home_odds, tie_odds, away_odds,
            provider, provider, provider,
            time, sport
        )
    )
    return True
