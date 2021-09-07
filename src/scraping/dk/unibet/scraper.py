import src.scraping.dk.kambi.scraper as kambi


def get_unibet(days=1, offset_hours=2):
    return kambi.get_kambi('Unibet', 'ubdk', days, offset_hours=offset_hours)

