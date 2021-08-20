import scraping.dk.oddset.scraper as oddset
import scraping.dk.unibet.scraper as unibet
import scraping.dk.sport888.scraper as sport888
import scraping.dk.mr_green.scraper as mr_green
import scraping.dk.leo_vegas.scraper as leo_vegas
import scraping.dk.bwin.scraper as bwin


def run_scrapers():
    bets1 = oddset.get_oddset()
    bets2 = unibet.get_unibet()
    bets3 = sport888.get_sport888()
    bets4 = mr_green.get_mr_green()
    bets5 = leo_vegas.get_leo_vegas()
    bets6 = bwin.get_bwin()
    merge(bets1, bets2)
    merge(bets1, bets3)
    merge(bets1, bets4)
    merge(bets1, bets5)
    merge(bets1, bets6)
    return bets1.values()


def merge(bets1, bets2):
    for key in bets2.keys():
        if key in bets1.keys():
            bets1.get(key).merge(bets2.get(key))


bets = list(run_scrapers())
bets.sort()
bets.reverse()
for bet in bets:
    print()
    print(bet.tostring())
    print()
