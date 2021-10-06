total_bet_amount = 3000


def _size(axiom, arb):
    return ((1 / float(axiom.odds) * 100) / arb) * total_bet_amount


def get_bet_sizes(axiom_list, arb):
    return [_size(axiom, arb) for axiom in axiom_list]


