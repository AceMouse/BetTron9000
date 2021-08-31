import src.scraping.dk.kambi.scraper as kambi


def get_leo_vegas(days=1):
    return kambi.get_kambi('LeoVegas', 'leodk', days)
