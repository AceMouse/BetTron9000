import src.scraping.dk.kambi.scraper as kambi
from scraping.dk.scraper_runner import run_scraper


def get_leo_vegas(days=1, offset_hours=2):
    return kambi.get_kambi('LeoVegas', 'leodk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scraper(get_leo_vegas)
