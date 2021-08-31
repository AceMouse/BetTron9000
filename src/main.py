import scraping.dk.oddset.scraper as oddset
import scraping.dk.unibet.scraper as unibet
import scraping.dk.sport888.scraper as sport888
import scraping.dk.mr_green.scraper as mr_green
import scraping.dk.leo_vegas.scraper as leo_vegas
import scraping.dk.bwin.scraper as bwin
import scraping.dk.bet25.scraper as bet25
import scraping.dk.betstars.scraper as betstars
import util.editing_distance as ed
import time
import winsound
import datetime


def run_scrapers(days=1):
    bets = oddset.get_oddset(days=days)
    merge(bets, unibet.get_unibet(days=days))
    merge(bets, sport888.get_sport888(days=days))
    merge(bets, mr_green.get_mr_green(days=days))
    merge(bets, leo_vegas.get_leo_vegas(days=days))
    merge(bets, bwin.get_bwin(days=days))
    merge(bets, bet25.get_bet25(hours=(days+1)*24))
    merge(bets, betstars.get_betstars(days=days))
    return bets


def merge(bets1, bets2):
    for time in bets2.keys():
        if time in bets1.keys():
            for bet_2 in bets2[time]:
                merged = False
                for bet_1 in bets1[time]:
                    if ed.is_similar(bet_1.home_name, bet_2.home_name) and ed.is_similar(bet_1.away_name, bet_2.away_name):
                        bet_1.merge(bet_2)
                        merged = True
                        break
                if not merged:
                    bets1[time].append(bet_2)
        else:
            bets1[time] = bets2[time]


i = 0
while True:
    if i % 3 == 2:
        days = 30
    else:
        days = 1
    bets = run_scrapers(days=days)
    list = []
    for bet_list in bets.values():
        list.extend(bet_list)
    list.sort()
    list.reverse()
    for bet in list:
        print()
        print(bet.tostring())
        print()

    print(f'Total bets: {len(list)}')
    print('last scrape at: ' + str(datetime.datetime.now()))
    duration = 500  # milliseconds
    freq = 440  # Hz
    if list[-1].arb < 100:
        winsound.Beep(freq, duration)
        time.sleep(1)
        winsound.Beep(freq, duration)

    i += 1
    time.sleep(60 * 30)
