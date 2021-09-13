import json
import requests
from datetime import datetime, timedelta
import bets
from util import bet_adder


class KampiOddsInfo(bets.Bet.Bet.OddsInfo):
    def _extract_odds(self, bet_offer, outcome_types):
        for outcome in bet_offer['outcomes']:
            if outcome['status'] != 'OPEN':
                continue
            outcome_types[outcome['type']](float(outcome['odds'] / 1000))


    def extract_single_odds(self, market):
        self._extract_odds(market,
                           {'OT_ONE': self.set_home,
                            'OT_TWO': self.set_away,
                            'OT_CROSS': self.set_tie}
                           )

    def extract_double_chance_odds(self, market):
        raise NotImplementedError()


def get_events(days, offset_hours, provider, provider_url):
    from_date = datetime.now() + timedelta(hours=offset_hours)
    to_date = from_date + timedelta(days=1)
    events = []
    for _ in range(days):
        from_string = from_date.strftime('%Y%m%dT%H%M%S+0200')
        to_string = to_date.strftime('%Y%m%dT%H%M%S+0200')
        from_date += timedelta(days=1)
        to_date += timedelta(days=1)

        payload = {
            'lang': 'en_GB',
            'market': 'DK',
            'client_id': '2',
            'channel_id': '1',
            'ncid': '1629387795925',
            'useCombined': 'true',
            'from': from_string,
            'to': to_string
        }
        request = requests.get(
            'https://eu-offering.kambicdn.org/offering/v2018/' + provider_url + '/listView/all/all/all/all/starting-within.json',
            params=payload)
        print(f'getting {provider}: ' + request.url)
        events.extend(json.loads(request.text)['events'])

    return events


def get_event_team_names(event):
    return event['event']['homeName'], event['event']['awayName']


def get_event_time(event):
    return datetime.strptime(event['event']['start'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)


def get_event_odds_info(event):
    odds_info = KampiOddsInfo()
    for bet_offer in event['betOffers']:
        odds_info.extract_single_odds(bet_offer)
    return odds_info


def process_event(bets, event, provider):
    if 'awayName' not in event['event'] or 'homeName' not in event['event']:
        return False
    home_name, away_name = get_event_team_names(event)
    time = get_event_time(event)
    odds_info = get_event_odds_info(event)
    bet_adder.add_bet_to_bets(bets,
                              home_name, away_name,
                              odds_info,
                              provider,
                              time)
    return True


def get_kambi(provider, provider_url, days, offset_hours=2):
    bets = dict()
    total_bets = 0
    for event in get_events(days, offset_hours, provider, provider_url):
        if process_event(bets, event, provider):
            total_bets += 1

    print('Events total: ' + str(total_bets))
    print('success')
    return bets
