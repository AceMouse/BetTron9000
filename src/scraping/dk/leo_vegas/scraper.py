import src.scraping.dk.kambi.scraper as kambi


def get_leo_vegas(days=1, offset_hours=2):
    return kambi.get_kambi('LeoVegas', 'leodk', days, offset_hours=offset_hours)
