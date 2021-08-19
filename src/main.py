import scraping.dk.oddset.scraper as oddset
import scraping.dk.unibet.scraper as unibet

def run_scrapers():
    bets1 = oddset.get_oddset()
    bets2 = unibet.get_unibet()
    for key in bets2.keys():
        if key in bets1.keys():
            bets1.get(key).merge(bets2.get(key))
    return bets1.values()

bets = list(run_scrapers())
bets.sort()
bets.reverse()
for bet in bets:
    print()
    print(bet.tostring())
    print()
