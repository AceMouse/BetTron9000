import src.scraping.dk.kambi.scraper as kambi


def get_unibet(days=1):
    return kambi.get_kambi('Unibet', 'ubdk', days)

