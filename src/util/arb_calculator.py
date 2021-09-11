def get_2arb_percentage(a, b):
    if float(a) == 0 or float(b) == 0:
        return 1000
    return _get_2arb_percentage(a, b)


def _get_2arb_percentage(a, b):
    arb1 = 1 / float(a) * 100
    arb2 = 1 / float(b) * 100
    return arb1 + arb2


def get_3arb_percentage(a, b, c):
    if float(a) == 0 or float(c) == 0:
        return 1000
    if float(b) == 0:
        return _get_2arb_percentage(a, c)
    arb1 = 1 / float(a) * 100
    arb2 = 1 / float(b) * 100
    arb3 = 1 / float(c) * 100
    return arb1 + arb2 + arb3
