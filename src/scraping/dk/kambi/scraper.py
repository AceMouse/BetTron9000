import json
import requests
from datetime import datetime, timedelta

from util import bet_adder


def get_kambi(provider, provider_url, days, offset_hours=2):
    bets = dict()
    total_bets = 0
    from_date = datetime.now() + timedelta(hours=offset_hours)
    for _ in range(days):
        from_string = from_date.strftime('%Y%m%dT%H%M%S+0200')
        to_date = from_date + timedelta(days=1)
        to_string = to_date.strftime('%Y%m%dT%H%M%S+0200')

        from_date += timedelta(days=1)

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
        if request.ok:
            JSON = json.loads(request.text)
            for event in JSON['events']:
                if 'awayName' not in event['event'] or 'homeName' not in event['event']:
                    continue
                home_name = event['event']['homeName']
                away_name = event['event']['awayName']
                time = datetime.strptime(event['event']['start'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
                try:
                    home_odds = event['betOffers'][0]['outcomes'][0]['odds'] / 1000
                    tie_odds = 0
                    if len(event['betOffers'][0]['outcomes']) == 3:
                        tie_odds = event['betOffers'][0]['outcomes'][1]['odds'] / 1000
                    away_odds = event['betOffers'][0]['outcomes'][-1]['odds'] / 1000
                except:
                    continue
                if bet_adder.try_to_add_bet_to_bets(bets,
                                                    home_name, away_name,
                                                    away_odds, tie_odds, home_odds,
                                                    provider,
                                                    time):
                    total_bets += 1
        else:
            print('request failure')
    print('Events total: ' + str(total_bets))
    print('success')
    return bets
