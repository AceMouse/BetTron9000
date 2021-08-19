import json
import requests
import bets.Bet as Bet
from datetime import datetime, timedelta


def get_unibet():
    bets = {}
    url = 'https://eu-offering.kambicdn.org/offering/v2018/ub/listView/all/all/all/all/starting-within.json'
    payload = {
        'lang': 'en_GB',
        'market': 'ZZ',
        'client_id': '2',
        'channel_id': '1',
        'ncid': '1629387795925',
        'useCombined': 'true',
        'from': '20210820T000000+0200',
        'to': '20210821T000000+0200'
    }
    provider = "Unibet"
    request = requests.get(
        'https://eu-offering.kambicdn.org/offering/v2018/ub/listView/all/all/all/all/starting-within.json',
        params=payload)
    print('getting Unibet: ' + request.url)
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
                tie_odds = '0'
                if len(event['betOffers'][0]['outcomes']) == 3:
                    tie_odds = event['betOffers'][0]['outcomes'][1]['odds'] / 1000
                away_odds = event['betOffers'][0]['outcomes'][-1]['odds'] / 1000
            except:
                continue
            bet = Bet.Bet(home_name, away_name, home_odds, tie_odds, away_odds,
                          provider, provider, provider,
                          time)
            bets[bet.__hash__()] = bet
        print('Events total: ' + str(len(JSON['events'])))
        print('success')
        return bets
    else:
        print('request failure')
        return set()

