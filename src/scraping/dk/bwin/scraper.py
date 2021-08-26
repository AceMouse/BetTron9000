import json
#import requests
import urllib
import bets.Bet as Bet
from datetime import datetime, timedelta


def get_bwin():
    bets = {}
    provider = 'Bwin'

    from_date = datetime.today() #+ timedelta(days=1)
    from_string = from_date.date().strftime('%Y-%m-%d')
    to_date = from_date + timedelta(days=1)
    to_string = to_date.date().strftime('%Y-%m-%d')
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
        'take': '2000',
        'sortBy': 'StartDate',
        'from': from_string + 'T22:00:00.000Z',
        'to': to_string + 'T22:00:00.000Z'
    }
    url = 'https://cds-api.bwin.dk/bettingoffer/fixtures?' + urllib.parse.urlencode(payload)
    '''
    'https://cds-api.bwin.dk/bettingoffer/fixtures?x-bwin-accessid=MjJmMjBkY2QtZmNjOS00YjUyLTk4M2MtNzY4M2Y5NzdjNWEy&lang=en&country=DK&userCountry=DK&fixtureTypes=Standart&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other,Specials,Outrights&sportIds=4&regionIds=&competitionIds=&skip=0&take=2000&sortBy=StartDate&from=2021-08-20T22:00:00.000Z&to=2021-08-21T22:00:00.000Z'
    'https://cds-api.bwin.dk/bettingoffer/fixtures?x-bwin-accessid=MjJmMjBkY2QtZmNjOS00YjUyLTk4M2MtNzY4M2Y5NzdjNWEy&lang=en&country=DK&userCountry=DK&fixtureTypes=Standart&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other,Specials,Outrights&sportIds=4&regionIds=&competitionIds=&skip=0&take=2000&sortBy=StartDate&from=2021-08-21T22:00:00.000Z&to=2021-08-22T22:00:00.000Z'
    request = requests.get(
        'https://cds-api.bwin.dk/bettingoffer/fixtures',
        params=payload)
    
    print(f'getting {provider}: ' + request.url)
    if request.ok:
        JSON = json.loads(request.text)
    '''
    path = 'C:\\Users\\asmus\\programing\\odds_comparator\\resourses\\bwin.json'
    with open(path) as f:
        JSON = json.load(f)
        check_date = datetime.strptime(from_string, '%Y-%m-%d') + timedelta(hours=22) #datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=22)
        if datetime.strptime(JSON['fixtures'][0]['startDate'], '%Y-%m-%dT%H:%M:%SZ') < check_date:
            print(f'please get {provider} at: ' + url)
            print('manually save it to: ' + path)
            if input('continue program?') == '':
                with open(path) as ff:
                    JSON = json.load(ff)
                    if datetime.strptime(JSON['fixtures'][0]['startDate'], '%Y-%m-%dT%H:%M:%SZ') >= check_date:
                        print(f'getting {provider} locally: ' + path)
                    else:
                        return {}
            else:
                exit(1)
        else:
            print(f'getting {provider} locally: ' + path)
            print(f'please get {provider} online at: ' + url)

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
        tie_odds = '0'
        home_odds = '0'
        away_odds = '0'
        for market in fixture['optionMarkets']:
            if market['name']['value'] == 'Match Result':
                for option in market['options']:
                    if option['name']['value'] == 'X':
                        tie_odds = str(option['price']['odds'])
                    elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == home_name:
                        home_odds = str(option['price']['odds'])
                    elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == away_name:
                        away_odds = str(option['price']['odds'])
                break
        if home_odds == '0' or away_odds == '0':
            continue
        bet = Bet.Bet(home_name, away_name,
                      home_odds, tie_odds, away_odds,
                      provider, provider, provider,
                      time)
        bets[bet.__hash__()] = bet
    print('Events total: ' + str(len(JSON['fixtures'])))
    print('success')
    return bets
'''
else:
    print('request failure' + str(request))
    return {}
'''
