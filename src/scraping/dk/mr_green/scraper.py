import src.scraping.dk.kambi.scraper as kambi
from scraping.dk.scraper_runner import run_scraper


def get_mr_green(days=1, offset_hours=2):
    return kambi.get_kambi('Mr Green', 'mgdk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scraper(get_mr_green)
