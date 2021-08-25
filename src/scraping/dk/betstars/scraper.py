import json
import requests
import bets.Bet as Bet
from datetime import datetime, timedelta
import time


def get_betstars():
    bets = {}
    date = datetime.today() + timedelta(days=1)
    date_str = date.date().strftime('%Y-%m-%d')
    provider = 'Betstars'
    sports = ['SOCCER', 'AMERICAN_FOOTBALL', 'TENNIS', 'HANDBALL', 'BASKETBALL', 'ICE_HOCKEY', 'ESPORTS', 'BASEBALL',
              'AUSSIE_RULES', 'BEACH_VOLLEYBALL', 'BOXING', 'TABLE_TENNIS', 'CRICKET', 'CYCLING', 'DARTS', 'FUTSAL',
              'GOLF', 'RALLY', 'MOTOR_SPORTS', 'PESAPALLO', 'RUGBY_LEAGUE', 'RUGBY_UNION', 'SNOOKER', 'BEACH_SOCCER',
              'VOLLEYBALL']

    for sport in sports:
        request = requests.get(
            'https://sports.pokerstarssports.dk/sportsbook/v1/api/getEventsForDay?sport=' + sport + '&date=' + date_str + '&count=2000&utcOffset=2&locale=da-dk&channelId=6&siteId=2048')
        print(f'getting {provider} ({sport}): ' + request.url)
        if request.ok:
            JSON = json.loads(request.text)
            for event in JSON:
                if len(event['participants']['participant']) < 2:
                    continue

                if event['participants']['participant'][0]['type'] == 'HOME':
                    home_name = event['participants']['participant'][0]['name']
                    away_name = event['participants']['participant'][1]['name']
                else:
                    home_name = event['participants']['participant'][1]['name']
                    away_name = event['participants']['participant'][0]['name']
                start_time = event['eventTime']
                tie_odds = '0'
                home_odds = '0'
                away_odds = '0'
                for market in event['markets']:
                    if not market['suspended'] and market['name'] in ['Kampens resultat', 'Matchvinder',
                                                                           'Money Line', 'Kampresultat',
                                                                           'Kampens resultat – 2-vejs']:
                        for selection in market['selection']:
                            if selection['type'] in ['Draw', 'D'] or selection['name'] == 'Uafgjort':
                                tie_odds = str(selection['odds']['dec'])
                            elif selection['name'] == home_name:
                                home_odds = str(selection['odds']['dec'])
                            elif selection['name'] == away_name:
                                away_odds = str(selection['odds']['dec'])
                        break
                if home_odds == '0' or away_odds == '0':
                    continue
                bet = Bet.Bet(home_name, away_name,
                              home_odds, tie_odds, away_odds,
                              provider, provider, provider,
                              start_time)
                bets[bet.__hash__()] = bet
        else:
            print('request failure')
            continue
    print('Events total: ' + str(len(bets)))
    print('success')
    return bets
