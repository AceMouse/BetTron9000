import src.scraping.dk.kambi.scraper as kambi


def get_mr_green(days=1, offset_hours=2):
    return kambi.get_kambi('Mr Green', 'mgdk', days, offset_hours=offset_hours)
