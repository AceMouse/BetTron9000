def _get_arb_percentage(a, b):
    if a == '0' or b == '0':
        return 1000

    arb1 = 1 / float(a) * 100
    arb2 = 1 / float(b) * 100
    return arb1 + arb2


def get_arb_percentage(a, b, c):
    if a == '0' or c == '0':
        return 1000
    if b == '0':
        return _get_arb_percentage(a, c)
    arb1 = 1 / float(a) * 100
    arb2 = 1 / float(b) * 100
    arb3 = 1 / float(c) * 100
    return arb1 + arb2 + arb3
