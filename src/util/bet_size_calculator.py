total_bet_amount = 100


def _size(axiom, arb):
    return ((1 / float(axiom.odds) * 100) / arb) * total_bet_amount


def get_3bet_sizes(axiom1, axiom2, axiom3, arb):
    return _size(axiom1, arb), _size(axiom2, arb), _size(axiom3, arb)


def get_2bet_sizes(axiom1, axiom2, arb):
    return _size(axiom1, arb), _size(axiom2, arb)
