import json
import requests
from datetime import datetime, timedelta
import bets
from scanning.dk.scanner_runner import run_scanner
from util import bet_adder


class BetstarsOddsInfo(bets.Bet.Bet.OddsInfo):
    def __init__(self, single_types, double_chance_types):
        super().__init__()
        self.single_types = single_types
        self.double_chance_types = double_chance_types

    def _extract_odds(self, market, market_types, outcomes):
        if market['suspended'] or market['type'] not in market_types:
            return
        for selection in market['selection']:
            outcomes[selection['type']](float(selection['odds']['dec']))

    def extract_single_odds(self, market):
        self._extract_odds(market, self.single_types,
                           {'A': self.set_home,
                            'B': self.set_away,
                            'Draw': self.set_tie,
                            'D': self.set_tie}
                           )

    def extract_double_chance_odds(self, market):
        self._extract_odds(market, self.double_chance_types,
                           {'HD': self.set_home_x,
                            'AD': self.set_x_away,
                            'HA': self.set_home_away}
                           )


def get_events(days, offset_hours, sports):
    date = datetime.today() + timedelta(offset_hours)

    events = []
    for _ in range(days + 1):
        date_str = date.date().strftime('%Y-%m-%d')
        date += timedelta(days=1)
        for sport in sports:
            request = requests.get(
                'https://sports.pokerstarssports.dk/sportsbook/v1/api/getEventsForDay?sport=' + sport + '&date=' + date_str + '&count=2000&utcOffset=2&locale=en-gb&marketTypes=SOCCER%3AFT%3AAXB,SOCCER%3AFT%3ADC&channelId=6&siteId=2048')
            print(f'getting Betstars ({sport}): ' + request.url)
            events.extend(json.loads(request.text))

    return events


def get_match_types(sports):
    single_types = set()
    double_chance_types = set()
    for sport in sports:
        single_types.add(f'{sport}:FT:AB')
        single_types.add(f'{sport}:FT:AXB')
        double_chance_types.add(f'{sport}:FT:DC')
    return single_types, double_chance_types


def get_event_time(event):
    time_offset = datetime(year=2021, month=8, day=27, hour=1, minute=15)
    return time_offset + timedelta(milliseconds=int(event['eventTime']) - 1630019700000)


def get_event_team_names(event):
    if event['participants']['participant'][0]['type'] == 'HOME':
        return event['participants']['participant'][0]['name'], event['participants']['participant'][1]['name']
    return event['participants']['participant'][1]['name'], event['participants']['participant'][0]['name']


def get_event_odds_info(event, single_types, double_chance_types):
    odds_info = BetstarsOddsInfo(single_types, double_chance_types)
    for market in event['markets']:
        odds_info.extract_single_odds(market)
        odds_info.extract_double_chance_odds(market)
    return odds_info


def get_event_sport(event):
    return event['sport']


def process_event(event, bets, single_types, double_chance_types):
    if len(event['participants']['participant']) < 2:
        return False
    home_name, away_name = get_event_team_names(event)
    time = get_event_time(event)
    odds_info = get_event_odds_info(event, single_types, double_chance_types)
    sport = get_event_sport(event)
    bet_adder.add_bet_to_bets(bets,
                              home_name, away_name,
                              odds_info,
                              'Betstars',
                              time,
                              sport=sport)
    return True


def get_betstars(days=1, offset_hours=2):
    bets = dict()
    total_bets = 0
    sports = ['SOCCER', 'AMERICAN_FOOTBALL', 'TENNIS', 'HANDBALL', 'BASKETBALL', 'ICE_HOCKEY', 'ESPORTS', 'BASEBALL',
              'AUSSIE_RULES', 'BEACH_VOLLEYBALL', 'BOXING', 'TABLE_TENNIS', 'CRICKET', 'CYCLING', 'DARTS', 'FUTSAL',
              'GOLF', 'RALLY', 'MOTOR_SPORTS', 'PESAPALLO', 'RUGBY_LEAGUE', 'RUGBY_UNION', 'SNOOKER', 'BEACH_SOCCER',
              'VOLLEYBALL']
    single_types, double_chance_types = get_match_types(sports)
    for event in get_events(days, offset_hours, sports):
        if process_event(event, bets, single_types, double_chance_types):
            total_bets += 1
    print('Events total: ' + str(total_bets))
    print('success')
    return bets


if __name__ == '__main__':
    run_scanner(get_betstars)
