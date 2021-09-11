from datetime import datetime

import util.bet_size_calculator as bc


def run_scraper(scraper):
    bets = scraper()

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
