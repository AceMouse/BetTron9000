#'https://eu-offering.kambicdn.org/offering/v2018/888dk/listView/all/all/all/all/starting-within.json?lang=da_DK&market=DK&client_id=2&channel_id=1&ncid=1629473012968&useCombined=true&from=20210821T000000%2B0200&to=20210822T000000%2B0200'
import src.scraping.dk.kambi.scraper as kambi


def get_sport888(days=1, offset_hours=2):
    return kambi.get_kambi('888Sport', '888dk', days, offset_hours=offset_hours)
