import src.scraping.dk.kambi.scraper as kambi
from scraping.dk.scraper_runner import run_scraper


def get_sport888(days=1, offset_hours=2):
    return kambi.get_kambi('888Sport', '888dk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scraper(get_sport888)
