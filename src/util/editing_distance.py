import editdistance


def is_similar(a, b, multiplier=0.3):
    return editdistance.eval(a, b) < ((len(a) + len(b)) / 2) * multiplier
