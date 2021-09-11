import json
import requests
from datetime import datetime, timedelta
from util import bet_adder
import util.bet_size_calculator as bc


def get_bwin(days=1, offset_hours=2):
    bets = dict()
    total_bets = 0
    provider = 'Bwin'
    from_date = datetime.now() + timedelta(hours=offset_hours)
    from_string = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    to_date = from_date + timedelta(days=days)
    to_string = to_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
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
            home_away_odds = x_away_odds = home_x_odds = tie_odds = home_odds = away_odds = 0
            match_result_flag = False
            double_chance_flag = False
            for market in fixture['optionMarkets']:
                if market['name']['value'] == 'Match Result' and market['status'] != 'Suspended':
                    for option in market['options']:
                        if option['name']['value'] == 'X':
                            if option['status'] != 'Suspended':
                                tie_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == home_name:
                            if option['status'] != 'Suspended':
                                home_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == away_name:
                            if option['status'] != 'Suspended':
                                away_odds = float(option['price']['odds'])
                    match_result_flag = True
                elif market['name']['value'] == 'Double Chance' and market['status'] != 'Suspended':
                    for option in market['options']:
                        if option['name']['value'] == f'{home_name} or X':
                            if option['status'] != 'Suspended':
                                home_x_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)', ' (Women)') == f'X or {away_name}':
                            if option['status'] != 'Suspended':
                                x_away_odds = float(option['price']['odds'])
                        elif option['name']['value'].replace(' (Women) (Women)',
                                                             ' (Women)') == f'{home_name} or {away_name}':
                            if option['status'] != 'Suspended':
                                home_away_odds = float(option['price']['odds'])
                    double_chance_flag = True
                if double_chance_flag and match_result_flag:
                    break
            if bet_adder.try_to_add_bet_to_bets(bets,
                                                home_name, away_name,
                                                away_odds, tie_odds, home_odds,
                                                provider,
                                                time,
                                                home_x_odds=home_x_odds, x_away_odds=x_away_odds, home_away_odds=home_away_odds):
                total_bets += 1
        print('Events total: ' + str(total_bets))
        print('success')
        return bets

    else:
        print('request failure' + str(request))
        return {}


def main():
    bc.total_bet_amount = float(input("how much do you want to bet (dkk)?\n\t>>>"))
    bets = get_bwin()

    list = []
    for bet_list in bets.values():
        list.extend(bet_list)
    for bet in list:
        bet.sort_axioms()
    list.sort(reverse=True)
    to_print = []
    for bet in list:
        to_print.append('\n')
        bet.add_string_to_list(to_print)
        to_print.append('\n')
    print(''.join(to_print))

    print(f'Total bets: {len(list)}')
    print('last scrape at: ' + str(datetime.now()))


if __name__ == '__main__':
    main()
