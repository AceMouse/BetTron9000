import json
import requests
from datetime import datetime
import bets
from scanning.dk.scanner_runner import run_scanner
from util import bet_adder


class Bet25OddsInfo(bets.Bet.Bet.OddsInfo):
    def _extract_odds(self, market, market_name, outcome_types):
        if market['marketTypeName'] != 'Fuldtid' or market['marketName'] != market_name:
            return
        for item in market['itemList']:
            outcome_types[item['homeDrawAway']](float(item['odds']))

    def extract_single_odds(self, market):
        self._extract_odds(market, 'Vinder',
                           {'1': self.set_home,
                            '2': self.set_away,
                            'X': self.set_tie}
                           )

    def extract_double_chance_odds(self, market):
        raise NotImplementedError()


def get_events(hours):
    request = requests.get('https://www.bet25.dk/rest/sports/events/hours/' + str(hours))
    print(f'getting Bet25: ' + request.url)
    return json.loads(request.text)['data']


def get_event_odds_info(event):
    odds_info = Bet25OddsInfo()
    for market in event['marketList']:
        odds_info.extract_single_odds(market)
    return odds_info


def get_event_time(event):
    return datetime.strptime(event['kickoffDate'] + event['kickoffTime'], '%d.%m.%Y%H:%M')


def get_event_team_names(event):
    return event['homeTeam'], event['awayTeam']


def process_event(event, bets):
    if 'awayTeam' not in event or 'homeTeam' not in event:
        return False

    home_name, away_name = get_event_team_names(event)
    if home_name is None or away_name is None:
        return False

    time = get_event_time(event)
    odds_info = get_event_odds_info(event)
    bet_adder.add_bet_to_bets(bets,
                              home_name, away_name,
                              odds_info,
                              'Bet25',
                              time)
    return True


def get_bet25(hours=48):
    bets = dict()
    total_bets = 0
    for event in get_events(hours):
        if process_event(event, bets):
            total_bets += 1
    print('Events total: ' + str(total_bets))
    print('success')
    return bets


if __name__ == '__main__':
    run_scanner(get_bet25)
