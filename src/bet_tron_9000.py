import scanning.dk.oddset.scanner as oddset
import scanning.dk.unibet.scanner as unibet
import scanning.dk.sport888.scanner as sport888
import scanning.dk.mr_green.scanner as mr_green
import scanning.dk.leo_vegas.scanner as leo_vegas
import scanning.dk.bwin.scanner as bwin
import scanning.dk.bet25.scanner as bet25
import scanning.dk.betstars.scanner as betstars
import util.editing_distance as ed
import util.bet_size_calculator as bc
import time
import winsound
from datetime import datetime


def run_scrapers(days=1, offset_hours=2):
    bets = oddset.get_oddset(days=days, offset_hours=offset_hours)
    merge(bets, unibet.get_unibet(days=days, offset_hours=offset_hours))
    merge(bets, sport888.get_sport888(days=days, offset_hours=offset_hours))
    merge(bets, mr_green.get_mr_green(days=days, offset_hours=offset_hours))
    merge(bets, leo_vegas.get_leo_vegas(days=days, offset_hours=offset_hours))
    merge(bets, bwin.get_bwin(days=days, offset_hours=offset_hours))
    merge(bets, bet25.get_bet25(hours=(days + 1) * 24))
    merge(bets, betstars.get_betstars(days=days, offset_hours=offset_hours))
    return bets


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


def main():
    bc.total_bet_amount = float(input("How much do you want to bet (dkk)?\n\t>>>"))
    i = 0
    while True:
        if i % 3 == 2:
            days = 5
        else:
            days = 2
        try:
            bets = run_scrapers(days=days, offset_hours=0)
        except:
            duration = 500  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            time.sleep(1)
            winsound.Beep(freq, duration)
            time.sleep(30)
            main()
        list = []
        for bet_list in bets.values():
            list.extend(bet_list)
        for bet in list:
            bet.sort_axioms()
        list.sort(reverse=True)
        to_print = []
        for bet in list[-10:]:
            to_print.append('\n')
            bet.add_string_to_list(to_print)
            to_print.append('\n')
        print(''.join(to_print))

        print(f'Total bets: {len(list)}')
        print('Last scan at: ' + str(datetime.now()))
        duration = 500  # milliseconds
        freq = 440  # Hz
        if list[-1].arb < 100:
            winsound.Beep(freq, duration)
            time.sleep(1)
            winsound.Beep(freq, duration)

        i += 1
        time.sleep(60 * 15)


if __name__ == '__main__':
    main()
