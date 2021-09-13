import util.editing_distance as ed


def merge(bets1, bets2):
    for time in bets2.keys():
        if time in bets1.keys():
            for bet_2 in bets2[time]:
                merged = False
                for bet_1 in bets1[time]:
                    if (ed.is_similar(bet_1.home_name(), bet_2.home_name()) and ed.is_similar(bet_1.away_name(),
                                                                                              bet_2.away_name())) or (
                            ed.is_similar(bet_1.away_name(), bet_2.home_name()) and ed.is_similar(bet_1.home_name(),
                                                                                                  bet_2.away_name())):
                        bet_1.merge(bet_2)
                        merged = True
                        break
                if not merged:
                    bets1[time].append(bet_2)
        else:
            bets1[time] = bets2[time]