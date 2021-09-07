total_bet_amount = 100


def get_bet_sizes(a):
    home_size = 0
    tie_size = 0
    away_size = 0
    if float(a.home_odds()) >= 1:
        home_size = ((1 / float(a.home_odds()) * 100) / a.arb)*total_bet_amount
    if float(a.tie_odds()) >= 1:
        tie_size = ((1 / float(a.tie_odds()) * 100) / a.arb)*total_bet_amount
    if float(a.away_odds()) >= 1:
        away_size = ((1 / float(a.away_odds()) * 100) / a.arb)*total_bet_amount
    return home_size, tie_size, away_size


