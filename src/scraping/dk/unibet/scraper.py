import src.scraping.dk.kambi.scraper as kambi


def get_unibet():
    return kambi.get_kambi('Unibet', 'ubdk')

