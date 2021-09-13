from bets import Bet


def add_bet_to_bets(bets, home_name, away_name, odds_info, provider, time, sport=''):
    if bets.get(str(time)) is None:
        bets[str(time)] = []
    bets[str(time)].append(
        Bet.Bet(
            home_name, away_name,
            odds_info,
            provider,
            time,
            sport=sport
        )
    )
