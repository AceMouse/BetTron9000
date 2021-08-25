import json
import requests
import bets.Bet as Bet
from datetime import datetime, timedelta


def get_zigzag_sport():
    bets = {}
    from_date = datetime.today()
    from_date_str = from_date.date().strftime('%Y-%m-%d') + 'T22:00:00.000Z'
    to_date = from_date + timedelta(days=1)
    to_date_str = to_date.date().strftime('%Y-%m-%d') + 'T22:00:00.000Z'
    provider = 'Zigzag'

    payload = {
        'startDate': from_date_str,
        'endDate': to_date_str,
        'timeZone': -120,
        'sportId': 4,
        'channel': '',
        'langId': 2,
        'partnerId': 81,
        'countryCode': 'DK'
    }
    for sport in [1, 4, 10, 13, 19, 36, 53, 80]:
        payload['sportId'] = sport
        request = requests.get(
            'https://sport.zigzagsport.com/Live/GetScheduledEventsByDate', payload)
        print(f'getting {provider} ({sport}): ' + request.url)
        if request.ok:
            JSON = json.loads(request.text)
            for event in JSON:
                away_team = event['AT']
                home_team = event['HT']
                time = datetime.strptime(event['D'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2)
                home_odds = 0
                tie_odds = 0
                away_odds = 0
                if event['StakeTypes'] == None:
                    continue
                for t in event['StakeTypes']:
                    if t['N'] == 'Result':
                        for stake in t['Stakes']:
                            if stake['N'] == 'Win1':
                                home_odds = stake['F']
                            elif stake['N'] == 'Win2':
                                away_odds = stake['F']
                            elif stake['N'] == 'Draw':
                                tie_odds = stake['F']
                        break
                if home_odds == 0 or away_odds == 0:
                    continue
                bet = Bet.Bet(home_team, away_team,
                              home_odds, tie_odds, away_odds,
                              provider, provider, provider,
                              time)
                bets[bet.__hash__()] = bet
        else:
            print('request failure')
            continue
    print('Events total: ' + str(len(bets)))
    print('success')
    return bets
