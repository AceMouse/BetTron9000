from datetime import datetime, timedelta
import time as t
import json
import requests

from scanning.dk.scanner_runner import run_scanner
from util import bet_adder


def get_oddset(days=1, offset_hours=2):
    timezone_dif = 2
    bets = dict()
    total_bets = 0
    from_date = datetime.now() + timedelta(hours=offset_hours-timezone_dif)
    end_date = from_date+timedelta(hours=24*days)
    to_date = from_date + timedelta(hours=4)
    while from_date < end_date:
        from_string = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        from_date += timedelta(hours=4)

        to_string = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        to_date += timedelta(hours=4)
        payload = {
            'startTimeFrom': from_string,
            'startTimeTo': to_string,
            'maxEvents': '100',
            'maxMarkets': '1000',
            'marketSortsIncluded': '--,HH,HL,MR,WH,DC',
            'eventSortsIncluded': 'MTCH',
            'includeChildMarkets': 'true',
            'prioritisePrimaryMarkets': 'true',
            'includeCommentary': 'false',
            'includeIncidents': 'false',
            'includeMedia': 'false',
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
                home_away_odds = x_away_odds = home_x_odds = tie_odds = home_odds = away_odds = 0
                match_result_flag = False
                double_chance_flag = False
                for market in event['markets']:
                    if market['name'] == 'Match Winner' and market['active']:
                        for outcome in market['outcomes']:
                            if len(outcome['prices']) == 1:
                                if outcome['subType'] == 'H' and outcome['active']:
                                    home_odds = float(outcome['prices'][0]['decimal'])
                                elif outcome['subType'] == 'A' and outcome['active']:
                                    away_odds = float(outcome['prices'][0]['decimal'])
                                elif outcome['subType'] == 'D' and outcome['active']:
                                    tie_odds = float(outcome['prices'][0]['decimal'])
                        match_result_flag = True
                    elif market['name'] == 'Double Chance' and market['active']:
                        for outcome in market['outcomes']:
                            if len(outcome['prices']) == 1:
                                if outcome['subType'] == '1' and outcome['active']:
                                    home_x_odds = float(outcome['prices'][0]['decimal'])
                                elif outcome['subType'] == '2' and outcome['active']:
                                    x_away_odds = float(outcome['prices'][0]['decimal'])
                                elif outcome['subType'] == '3' and outcome['active']:
                                    home_away_odds = float(outcome['prices'][0]['decimal'])
                        double_chance_flag = True
                    if match_result_flag and double_chance_flag:
                        break
                if bet_adder.try_to_add_bet_to_bets(bets,
                                                    home_name, away_name,
                                                    away_odds, tie_odds, home_odds,
                                                    provider,
                                                    time,
                                                    home_x_odds=home_x_odds, x_away_odds=x_away_odds, home_away_odds=home_away_odds,
                                                    sport=sport):
                    total_bets += 1
        else:
            print('request failure')
        t.sleep(0.5)

    print('Events total: ' + str(total_bets))
    print('success')
    return bets


if __name__ == '__main__':
    run_scanner(get_oddset)


