import json
import requests
import bets.Bet as Bet
from datetime import datetime, timedelta


def get_bet25():
    bets = {}
    provider = 'Bet25'
    request = requests.get('https://www.bet25.dk/rest/sports/events/hours/48')
    print(f'getting {provider}: ' + request.url)
    if request.ok:
        JSON = json.loads(request.text)
        for event in JSON['data']:
            if 'awayTeam' not in event or 'homeTeam' not in event:
                continue
            home_name = event['homeTeam']
            away_name = event['awayTeam']
            time = datetime.strptime(event['kickoffDate']+event['kickoffTime'], '%d.%m.%Y%H:%M')
            if time.date() != (datetime.today()+timedelta(days=1)).date():
                continue
            tie_odds = '0'
            home_odds = '0'
            away_odds = '0'
            for market in event['marketList']:
                if market['marketTypeName'] == 'Fuldtid' and market['marketName'] == 'Vinder':
                    for item in market['itemList']:
                        if item['competitor'] == 'Uafgjort' or item['bet'] == 'X':
                            tie_odds = str(item['odds'])
                        elif item['competitor'] == home_name:
                            home_odds = str(item['odds'])
                        elif item['competitor'] == away_name:
                            away_odds = str(item['odds'])
                    break
            if home_odds == '0' or away_odds == '0':
                continue
            bet = Bet.Bet(home_name, away_name,
                          home_odds, tie_odds, away_odds,
                          provider, provider, provider,
                          time)
            bets[bet.__hash__()] = bet
        print('Events total: ' + str(len(bets)))
        print('success')
        return bets
    else:
        print('request failure')
        return {}
