from datetime import datetime, timedelta
import json
import requests
from util import bet_adder


def get_oddset(days=1, offset_hours=2):
    timezone_dif = 2
    bets = dict()
    total_bets = 0
    from_date = datetime.now() + timedelta(hours=offset_hours-timezone_dif)
    from_string = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    to_date = from_date+timedelta(hours=24*days)
    to_string = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    payload = {
        'startTimeFrom': from_string,
        'startTimeTo': to_string,
        'maxEvents': '2000',
        'orderEventsBy': 'displayOrder',
        'maxMarkets': '10',
        'orderMarketsBy': 'displayOrder',
        'marketSortsIncluded': '--,HH,HL,MR,WH',
        'eventSortsIncluded': 'MTCH',
        'includeChildMarkets': 'true',
        'prioritisePrimaryMarkets': 'true',
        'includeCommentary': 'true',
        'includeIncidents': 'true',
        'includeMedia': 'true',
        'lang': 'en'
    }
    request = requests.get('https://content.sb.danskespil.dk/content-service/api/v1/q/event-list', params=payload)
    provider = "Oddset"
    print('getting Oddset: ' + request.url)
    if request.ok:
        JSON = json.loads(request.text)
        for event in JSON['data']['events']:
            if len(event['teams']) != 2:
                continue
            if event['teams'][0]['side'] == 'HOME':
                home_name = event['teams'][0]['name']
                away_name = event['teams'][1]['name']
            else:
                home_name = event['teams'][1]['name']
                away_name = event['teams'][0]['name']
            time = datetime.strptime(event['startTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=timezone_dif)
            sport = event['category']['name']
            tie_odds = home_odds = away_odds = 0
            for market in event['markets']:
                if market['name'] == 'Match Winner' and market['active']:
                    for i in market['outcomes']:
                        if len(i['prices']) == 1:
                            if i['subType'] == 'H':
                                home_odds = float(i['prices'][0]['decimal'])
                            elif i['subType'] == 'A':
                                away_odds = float(i['prices'][0]['decimal'])
                            else:
                                tie_odds = float(i['prices'][0]['decimal'])
                break
            if bet_adder.try_to_add_bet_to_bets(bets,
                                                home_name, away_name,
                                                away_odds, tie_odds, home_odds,
                                                provider,
                                                time,
                                                sport):
                total_bets += 1

        print('Events total: ' + str(total_bets))
        print('success')
        return bets
    else:
        print('request failure')
        return {}




