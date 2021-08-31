import src.scraping.dk.kambi.scraper as kambi


def get_mr_green(days=1):
    return kambi.get_kambi('Mr Green', 'mgdk', days)
