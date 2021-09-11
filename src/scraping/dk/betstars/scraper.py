import json
import requests
from datetime import datetime, timedelta
from util import bet_adder


def get_betstars(days=1, offset_hours=2):
    bets = dict()
    total_bets = 0
    date = datetime.today() + timedelta(offset_hours)
    provider = 'Betstars'
    sports = ['SOCCER', 'AMERICAN_FOOTBALL', 'TENNIS', 'HANDBALL', 'BASKETBALL', 'ICE_HOCKEY', 'ESPORTS', 'BASEBALL',
              'AUSSIE_RULES', 'BEACH_VOLLEYBALL', 'BOXING', 'TABLE_TENNIS', 'CRICKET', 'CYCLING', 'DARTS', 'FUTSAL',
              'GOLF', 'RALLY', 'MOTOR_SPORTS', 'PESAPALLO', 'RUGBY_LEAGUE', 'RUGBY_UNION', 'SNOOKER', 'BEACH_SOCCER',
              'VOLLEYBALL']
    match_types = {'Kampens resultat', 'Matchvinder',
                   'Money Line', 'Kampresultat',
                   'Kampens resultat – 2-vejs'}
    time_offset = datetime(year=2021, month=8, day=27, hour=1, minute=15)
    for _ in range(days + 1):
        date_str = date.date().strftime('%Y-%m-%d')
        date += timedelta(days=1)

        for sport in sports:
            request = requests.get(
                'https://sports.pokerstarssports.dk/sportsbook/v1/api/getEventsForDay?sport=' + sport + '&date=' + date_str + '&count=2000&utcOffset=2&locale=en-gb&channelId=6&siteId=2048')
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
                    time = time_offset + timedelta(milliseconds=int(event['eventTime']) - 1630019700000)
                    tie_odds = 0
                    home_odds = 0
                    away_odds = 0
                    try:
                        for market in event['markets']:
                            if not market['suspended'] and market['name'] in match_types:
                                for selection in market['selection']:
                                    if selection['name'] == away_name:
                                        away_odds = float(selection['odds']['dec'])
                                    elif selection['name'] == home_name:
                                        home_odds = float(selection['odds']['dec'])
                                    elif selection['type'] in {'Draw', 'D'} or selection['name'] == 'Uafgjort':
                                        tie_odds = float(selection['odds']['dec'])
                                break
                    except:
                        continue

                    if bet_adder.try_to_add_bet_to_bets(bets,
                                                        home_name, away_name,
                                                        away_odds, tie_odds, home_odds,
                                                        provider,
                                                        time,
                                                        sport=sport):
                        total_bets += 1
            else:
                print('request failure')
                continue
    print('Events total: ' + str(total_bets))
    print('success')
    return bets
