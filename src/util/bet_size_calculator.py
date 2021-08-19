import bets.Bet as Bet


def get_bet_sizes(a):
    home_size = 0
    tie_size = 0
    away_size = 0
    if a.home_odds != '0':
        home_size = ((1 / float(a.home_odds) * 100) * 100) / a.arb
    if a.tie_odds != '0':
        tie_size = ((1 / float(a.tie_odds) * 100) * 100) / a.arb
    if a.away_odds != '0':
        away_size = ((1 / float(a.away_odds) * 100) * 100) / a.arb
    return home_size, tie_size, away_size


def test():
    bet = Bet.Bet('A', 'B', '1.03', '25', '79', 'provider', 'provider', 'provider', 'time')
    print(bet.tostring())
    print(get_bet_sizes(bet))
