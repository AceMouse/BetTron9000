from datetime import datetime, timedelta
import json
import requests
import bets.Bet as Bet


def get_oddset():
    bets = dict()
    total_bets = 0
    from_date = datetime.today()
    from_string = from_date.date().strftime('%Y-%m-%d') + 'T22:00:00Z'
    to_date = from_date+timedelta(days=1)
    to_string = to_date.date().strftime('%Y-%m-%d') + 'T21:59:59Z'
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
            time = datetime.strptime(event['startTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
            sport = event['category']['name']
            tie_odds = '0'
            home_odds = '0'
            away_odds = '0'
            for market in event['markets']:
                if market['name'] == 'Match Winner' and market['active']:
                    for i in market['outcomes']:
                        if len(i['prices']) == 1:
                            if i['subType'] == 'H':
                                home_odds = str(i['prices'][0]['decimal'])
                            elif i['subType'] == 'A':
                                away_odds = str(i['prices'][0]['decimal'])
                            else:
                                tie_odds = str(i['prices'][0]['decimal'])
                break
            if home_odds == '0' or away_odds == '0':
                continue

            if bets.get(str(time)) is None:
                bets[str(time)] = []
            bets[str(time)].append(
                  Bet.Bet(
                      home_name, away_name,
                      home_odds, tie_odds, away_odds,
                      provider, provider, provider,
                      time, sport
                  )
            )
            total_bets += 1

        print('Events total: ' + str(total_bets))
        print('success')
        return bets
    else:
        print('request failure')
        return {}




