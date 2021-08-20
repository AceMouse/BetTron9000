import src.scraping.dk.kambi.scraper as kambi


def get_leo_vegas():
    return kambi.get_kambi('LeoVegas', 'leodk')
