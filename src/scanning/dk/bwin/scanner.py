import json
import requests
from datetime import datetime, timedelta
from scanning.dk.scanner_runner import run_scanner
from util import bet_adder
import bets


class BwinOddsInfo(bets.Bet.Bet.OddsInfo):
    def __init__(self, names):
        super().__init__()
        self.home_name = names[0].lower()
        self.away_name = names[1].lower()

    def _extract_odds(self, market, market_name, outcomes):
        if market['name']['value'] != market_name or market['status'] == 'Suspended':
            return
        for option in market['options']:
            if option['status'] == 'Suspended':
                continue
            name = option['name']['value'].replace(' (Women) (Women)', ' (Women)').lower()
            outcomes[name](float(option['price']['odds']))

    def extract_single_odds(self, market):
        self._extract_odds(market, 'Match Result',
                           {self.home_name: self.set_home,
                            self.away_name: self.set_away,
                            'X'.lower(): self.set_tie}
                           )

    def extract_double_chance_odds(self, market):
        self._extract_odds(market, 'Double Chance',
                           {f'{self.home_name} or X'.lower(): self.set_home_x,
                            f'X or {self.away_name}'.lower(): self.set_x_away,
                            f'{self.home_name} or {self.away_name}'.lower(): self.set_home_away}
                           )


def get_events(days, offset_hours):
    from_date = datetime.now() + timedelta(hours=offset_hours)
    from_string = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    to_date = from_date + timedelta(days=days)
    to_string = to_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    payload = {
        'x-bwin-accessid': 'MjJmMjBkY2QtZmNjOS00YjUyLTk4M2MtNzY4M2Y5NzdjNWEy',
        'lang': 'en',
        'country': 'DK',
        'userCountry': 'DK',
        'fixtureTypes': 'Standart',
        'state': 'Latest',
        'offerMapping': 'Filtered',
        'offerCategories': 'Gridable',
        'fixtureCategories': 'Gridable,NonGridable,Other,Specials,Outrights',
        'sportIds': '4',
        'regionIds': '',
        'competitionIds': '',
        'skip': '0',
        'take': '20000',
        'sortBy': 'StartDate',
        'from': from_string,
        'to': to_string
    }

    request = requests.get(
        'https://cds-api.bwin.dk/bettingoffer/fixtures',
        params=payload,
        headers=headers
    )

    print(f'getting Bwin: ' + request.url)
    return json.loads(request.text)['fixtures']


def get_event_names(event):
    home_name = ''
    away_name = ''
    for participant in event['participants']:
        if participant['properties']['type'] == 'HomeTeam':
            home_name = participant['name']['value']
        elif participant['properties']['type'] == 'AwayTeam':
            away_name = participant['name']['value']
    return home_name, away_name


def get_event_time(event):
    return datetime.strptime(event['startDate'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)


def get_event_odds_info(event):
    odds_info = BwinOddsInfo(get_event_names(event))
    for market in event['optionMarkets']:
        odds_info.extract_single_odds(market)
        odds_info.extract_double_chance_odds(market)
    return odds_info


def process_event(event, bets):
    if event['fixtureType'] != 'PairGame':
        return False

    home_name, away_name = get_event_names(event)

    if home_name == '' or away_name == '':
        return False

    time = get_event_time(event)
    odds_info = get_event_odds_info(event)

    bet_adder.add_bet_to_bets(bets,
                              home_name, away_name,
                              odds_info,
                              'Bwin',
                              time)
    return True


def get_bwin(days=1, offset_hours=2):
    bets = dict()
    total_bets = 0
    for event in get_events(days, offset_hours):
        if process_event(event, bets):
            total_bets += 1

    print('Events total: ' + str(total_bets))
    print('success')
    return bets


if __name__ == '__main__':
    run_scanner(get_bwin)
