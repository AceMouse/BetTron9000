import scraping.dk.oddset.scraper as oddset
import scraping.dk.unibet.scraper as unibet
import scraping.dk.sport888.scraper as sport888
import scraping.dk.mr_green.scraper as mr_green
import scraping.dk.leo_vegas.scraper as leo_vegas
import scraping.dk.bwin.scraper as bwin
import scraping.dk.bet25.scraper as bet25
import scraping.dk.betstars.scraper as betstars
import scraping.dk.zigzag_sport.scraper as zigzag_sport
import time
import winsound
import datetime


def run_scrapers():
    bets = oddset.get_oddset()
    merge(bets, unibet.get_unibet())
    merge(bets, sport888.get_sport888())
    merge(bets, mr_green.get_mr_green())
    merge(bets, leo_vegas.get_leo_vegas())
    merge(bets, bwin.get_bwin())
    merge(bets, bet25.get_bet25())
    merge(bets, betstars.get_betstars())
    merge(bets, zigzag_sport.get_zigzag_sport())
    return bets.values()


def merge(bets1, bets2):
    for key in bets2.keys():
        if key in bets1.keys():
            bets1[key].merge(bets2[key])
        else:
            bets1[key] = bets2[key]


start_date = datetime.date.today()
while start_date == datetime.date.today():
    bets = list(run_scrapers())
    bets.sort()
    bets.reverse()
    for bet in bets:
        print()
        print(bet.tostring())
        print()

    print(f'Total bets: {len(bets)}')
    print('last scrape at: ' + str(datetime.datetime.now()))
    duration = 500  # milliseconds
    freq = 440  # Hz
    if bets[-1].arb < 100:
        winsound.Beep(freq, duration)
        time.sleep(1)
        winsound.Beep(freq, duration)

    time.sleep(60 * 60)
