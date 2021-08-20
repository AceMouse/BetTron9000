from datetime import datetime, timedelta
import json
import requests
import bets.Bet as Bet


def get_oddset():
    bets = {}
    url = 'https://content.sb.danskespil.dk/content-service/api/v1/q/time-band-event-list'
    payload = {
        'maxMarkets': 10,
        'marketSortsIncluded': '--,HH,HL,MR,WH',
        'allowedEventSorts': 'MTCH',
        'includeChildMarkets': 'true',
        'prioritisePrimaryMarkets': 'true',
        'includeCommentary': 'true',
        'includeIncidents': 'true',
        'includeMedia': 'true',
        'drilldownTagIds': 1,
        'maxTotalItems': 1000,
        'maxEventsPerCompetition': 200,
        'maxCompetitionsPerSportPerBand': 200,
        'maxEventsForNextToGo': 1,
        'startTimeOffsetForNextToGo': 1
    }
    provider = "Oddset"
    request = requests.get('https://content.sb.danskespil.dk/content-service/api/v1/q/time-band-event-list', params=payload)
    print('getting Oddset: ' + request.url)
    if request.ok:
        JSON = json.loads(request.text)
        for item in JSON['data']['timeBandEvents']:
            if item['type'] == 'TOMORROW':
                for event in item['events']:
                    if len(event['teams']) != 2:
                        continue
                    if event['teams'][0]['side'] == 'HOME':
                        home_name = event['teams'][0]['name']
                        away_name = event['teams'][1]['name']
                    else:
                        home_name = event['teams'][1]['name']
                        away_name = event['teams'][0]['name']
                    time = datetime.strptime(event['startTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
                    tie_odds = '0'
                    home_odds = '0'
                    away_odds = '0'
                    for i in event['markets'][0]['outcomes']:
                        if len(i['prices']) == 1:
                            if i['subType'] == 'H':
                                home_odds = str(i['prices'][0]['decimal'])
                            elif i['subType'] == 'A':
                                away_odds = str(i['prices'][0]['decimal'])
                            else:
                                tie_odds = str(i['prices'][0]['decimal'])
                    bet = Bet.Bet(home_name.replace(" (k)", '').replace(" (W)", ''),
                                  away_name.replace(' (k)', '').replace(" (W)", ''),
                                  home_odds, tie_odds, away_odds,
                                  provider, provider, provider,
                                  time)
                    bets[bet.__hash__()] = bet
                print('Events total: ' + str(len(item['events'])))
                print('success')
                return bets
    else:
        print('request failure')
        return set()




