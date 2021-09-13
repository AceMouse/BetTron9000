from datetime import datetime, timedelta
import json
import requests
import bets
from scanning.dk.scanner_runner import run_scanner
from util import bet_adder
import util.bet_merger as merger





class OddsetOddsInfo(bets.Bet.Bet.OddsInfo):
    def _extract_odds(self, market, market_name, market_sub_types):
        if market['name'] != market_name or not market['active']:
            return
        for outcome in market['outcomes']:
            if len(outcome['prices']) != 1 or not outcome['active']:
                continue
            market_sub_types[outcome['subType']](float(outcome['prices'][0]['decimal']))

    def extract_single_odds(self, market):
        self._extract_odds(market, 'Match Winner',
                           {'H': self.set_home,
                            'A': self.set_away,
                            'D': self.set_tie}
                           )

    def extract_double_chance_odds(self, market):
        self._extract_odds(market, 'Double Chance',
                           {'1': self.set_home_x,
                            '2': self.set_x_away,
                            '3': self.set_home_away}
                           )

def get_events(days, offset_hours, markets, timezone_dif, max_events, max_markets, prioritise_main_market):
    from_date = datetime.now() + timedelta(hours=offset_hours - timezone_dif)
    to_date = from_date + timedelta(days=days)
    from_string = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    to_string = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    prioritise_main_market_str = str(prioritise_main_market).lower()
    payload = {
        'startTimeFrom': from_string,
        'startTimeTo': to_string,
        'maxEvents': max_events,
        'maxMarkets': max_markets,
        'marketSortsIncluded': markets,
        'eventSortsIncluded': 'MTCH',
        'includeChildMarkets': 'true',
        'prioritisePrimaryMarkets': prioritise_main_market_str,
        'includeCommentary': 'false',
        'includeIncidents': 'false',
        'includeMedia': 'false',
        'lang': 'en'
    }
    request = requests.get('https://content.sb.danskespil.dk/content-service/api/v1/q/event-list', params=payload)
    print('getting Oddset: ' + request.url)
    return json.loads(request.text)['data']['events']


def get_team_names(event):
    if event['teams'][0]['side'] == 'HOME':
        return event['teams'][0]['name'], event['teams'][1]['name']
    return event['teams'][1]['name'], event['teams'][0]['name']


def get_event_time(event, timezone_dif):
    return datetime.strptime(event['startTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=timezone_dif)


def get_event_sport(event):
    return event['category']['name']


def get_event_odds_info(event):
    odds_info = OddsetOddsInfo()
    for market in event['markets']:
        odds_info.extract_single_odds(market)
        odds_info.extract_double_chance_odds(market)

    return odds_info


def process_event(bets, event, timezone_dif):
    if len(event['teams']) != 2:
        return False

    home_name, away_name = get_team_names(event)
    time = get_event_time(event, timezone_dif)
    sport = get_event_sport(event)
    odds_info = get_event_odds_info(event)
    bet_adder.add_bet_to_bets(bets,
                              home_name, away_name,
                              odds_info,
                              'Oddset',
                              time,
                              sport=sport)
    return True


def get_oddset(days=1, offset_hours=2):
    all_bets = dict()
    mr_bets = dict()
    dc_bets = dict()
    total_bets = 0
    timezone_dif = 2
    max_events = 2000
    max_markets = 10
    for event in get_events(days, offset_hours, '--,HH,HL,MR,WH', timezone_dif, max_events, max_markets, True):
        if process_event(mr_bets, event, timezone_dif):
            total_bets += 1
    for event in get_events(days, offset_hours, 'DC', timezone_dif, max_events, max_markets, False):
        if process_event(dc_bets, event, timezone_dif):
            total_bets += 1

    print('Events total: ' + str(total_bets))
    print('success')
    merger.merge(bets1=all_bets, bets2=mr_bets)
    merger.merge(bets1=all_bets, bets2=dc_bets)
    return all_bets


if __name__ == '__main__':
    run_scanner(get_oddset)
