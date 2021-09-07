import json
#import requests
import urllib

import requests

import bets.Bet as Bet
from datetime import datetime, timedelta


def get_bwin(days=1, offset_hours=2):
    bets = dict()
    total_bets = 0
    provider = 'Bwin'
    from_date = datetime.now() + timedelta(hours=offset_hours)
    from_string = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    to_date = from_date + timedelta(days=days)
    to_string = to_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
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
    
    print(f'getting {provider}: ' + request.url)
    if request.ok:
        JSON = json.loads(request.text)

        for fixture in JSON['fixtures']:
            if fixture['fixtureType'] != 'PairGame':
                continue

            home_name = ''
            away_name = ''
            for participant in fixture['participants']:
                if participant['properties']['type'] == 'HomeTeam':
                    home_name = participant['name']['value']
                elif participant['properties']['type'] == 'AwayTeam':
                    away_name = participant['name']['value']

            if home_name == '' or away_name == '':
                continue

            time = datetime.strptime(fixture['startDate'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
            tie_odds = 0
            home_odds = 0
            away_odds = 0
            for market in fixture['optionMarkets']:
                if market['name']['value'] == 'Match Result' and market['status'] != "Suspended":
                    for option in market['options']:
                        if option['name']['value'] == 'X':
                            tie_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == home_name:
                            home_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == away_name:
                            away_odds = float(option['price']['odds'])
                    break
            if home_odds == 0 or away_odds == 0:
                continue
            if bets.get(str(time)) is None:
                bets[str(time)] = []
            bets[str(time)].append(
                Bet.Bet(
                    home_name, away_name,
                    home_odds, tie_odds, away_odds,
                    provider, provider, provider,
                    time
                )
            )
            total_bets += 1
        print('Events total: ' + str(total_bets))
        print('success')
        return bets

    else:
        print('request failure' + str(request))
        return {}

