from bets import Bet


def try_to_add_bet_to_bets(bets, home_name, away_name, away_odds, tie_odds, home_odds, provider, time, home_x_odds=0, x_away_odds=0, home_away_odds=0, sport=''):
    if home_odds == 0 or away_odds == 0:
        return False
    if bets.get(str(time)) is None:
        bets[str(time)] = []
    bets[str(time)].append(
        Bet.Bet(
            home_name, away_name,
            home_odds, tie_odds, away_odds,
            provider,
            time,
            home_x_odds=home_x_odds, x_away_odds=x_away_odds, home_away_odds=home_away_odds,
            sport=sport
        )
    )
    return True
