import util.arb_calculator as ac
import util.editing_distance as ed
import util.bet_size_calculator as bet_size


def _sanitize(name):
    if ',' in name:
        x = name.split(', ')
        name = x[-1] + ' ' + x[0]
    return name


def flip_names(name):
    x = name.split(' or ')
    return x[-1] + ' or ' + x[0]


class Bet:
    class OddsInfo:
        def __init__(self):
            self.home_away_odds = 1
            self.x_away_odds = 1
            self.home_x_odds = 1
            self.tie_odds = 1
            self.home_odds = 1
            self.away_odds = 1

        def set_home(self, odds):
            self.home_odds = odds

        def set_away(self, odds):
            self.away_odds = odds

        def set_tie(self, odds):
            self.tie_odds = odds

        def set_home_x(self, odds):
            self.home_x_odds = odds

        def set_x_away(self, odds):
            self.x_away_odds = odds

        def set_home_away(self, odds):
            self.home_away_odds = odds

    class Axiom:
        def __init__(self, name, odds, provider):
            self.name = name
            self.odds = float(odds)
            self.provider = provider

        def __eq__(self, other):
            return self.odds == other.odds

        def __lt__(self, other):
            return self.odds < other.odds

        def __le__(self, other):
            return self.odds <= other.odds

    def __init__(self, home_name, away_name, odds_info, provider, time, sport=''):
        self.home_axioms = [self.Axiom(_sanitize(home_name), odds_info.home_odds, provider)]
        self.tie_axioms = [self.Axiom('x', odds_info.tie_odds, provider)]
        self.away_axioms = [self.Axiom(_sanitize(away_name), odds_info.away_odds, provider)]

        self.home_x_axioms = [self.Axiom(f'{_sanitize(home_name)} or x', odds_info.home_x_odds, provider)]
        self.x_away_axioms = [self.Axiom(f'x or {_sanitize(away_name)}', odds_info.x_away_odds, provider)]
        self.home_away_axioms = [
            self.Axiom(f'{_sanitize(home_name)} or {_sanitize(away_name)}', odds_info.home_away_odds, provider)]

        self.time = time
        self.sport = sport

        self.arb = 0
        self.arb_match_result = 0
        self.arb_double_x_away = 0
        self.arb_double_home_x = 0
        self.arb_double_home_away = 0

    def sort_axioms(self):
        self.home_axioms.sort(reverse=True)
        self.tie_axioms.sort(reverse=True)
        self.away_axioms.sort(reverse=True)
        self.home_x_axioms.sort(reverse=True)
        self.x_away_axioms.sort(reverse=True)
        self.home_away_axioms.sort(reverse=True)
        self.set_arb()

    def set_arb(self):
        self.arb_match_result = ac.get_3arb_percentage(self.home_axioms[0].odds,
                                                       self.tie_axioms[0].odds,
                                                       self.away_axioms[0].odds)
        self.arb_double_x_away = ac.get_2arb_percentage(self.home_axioms[0].odds, self.x_away_axioms[0].odds)
        self.arb_double_home_x = ac.get_2arb_percentage(self.away_axioms[0].odds, self.home_x_axioms[0].odds)
        self.arb_double_home_away = ac.get_2arb_percentage(self.tie_axioms[0].odds, self.home_away_axioms[0].odds)
        self.arb = min(self.arb_match_result, self.arb_double_home_x, self.arb_double_x_away, self.arb_double_home_away)

    def merge(self, other):
        if ed.is_similar(self.home_axioms[0].name, other.home_axioms[0].name):
            for axiom in other.home_axioms:
                self.home_axioms.append(axiom)
            for axiom in other.tie_axioms:
                self.tie_axioms.append(axiom)
            for axiom in other.away_axioms:
                self.away_axioms.append(axiom)
            for axiom in other.home_x_axioms:
                self.home_x_axioms.append(axiom)
            for axiom in other.x_away_axioms:
                self.x_away_axioms.append(axiom)
            for axiom in other.home_away_axioms:
                self.home_away_axioms.append(axiom)
        else:
            for axiom in other.away_axioms:
                self.home_axioms.append(axiom)
            for axiom in other.tie_axioms:
                self.tie_axioms.append(axiom)
            for axiom in other.home_axioms:
                self.away_axioms.append(axiom)
            for axiom in other.home_x_axioms:
                axiom.name = flip_names(axiom.name)
                self.x_away_axioms.append(axiom)
            for axiom in other.x_away_axioms:
                axiom.name = flip_names(axiom.name)
                self.home_x_axioms.append(axiom)
            for axiom in other.home_away_axioms:
                axiom.name = flip_names(axiom.name)
                self.home_away_axioms.append(axiom)

        if len(other.sport) > len(self.sport):
            self.sport = other.sport

    def home_name(self):
        return self.home_axioms[0].name

    def tie_name(self):
        return self.tie_axioms[0].name

    def away_name(self):
        return self.away_axioms[0].name

    def home_odds(self):
        return float(self.home_axioms[0].odds)

    def tie_odds(self):
        return float(self.tie_axioms[0].odds)

    def away_odds(self):
        return float(self.away_axioms[0].odds)

    def home_provider(self):
        return self.home_axioms[0].provider

    def tie_provider(self):
        return self.tie_axioms[0].provider

    def away_provider(self):
        return self.away_axioms[0].provider

    def add_string_to_list(self, list):
        list.append(f'{self.time}\n')

        if self.sport != '':
            list.append(f'Sport: {self.sport}\n')

        if self.arb_match_result == self.arb:
            if self.tie_odds() != 0:
                self._add_string_to_list(list, ['HOME', 'TIE', 'AWAY'], [self.home_axioms, self.tie_axioms, self.away_axioms])
            else:
                self._add_string_to_list(list, ["HOME", "AWAY"], [self.home_axioms, self.away_axioms])

        elif self.arb_double_home_x == self.arb:
            self._add_string_to_list(list, ["HOME or X", "AWAY"], [self.home_x_axioms, self.away_axioms])

        elif self.arb_double_x_away == self.arb:
            self._add_string_to_list(list, ["HOME", "X or AWAY"], [self.home_axioms, self.x_away_axioms])

        elif self.arb_double_home_away == self.arb:
            self._add_string_to_list(list, ["HOME or AWAY", "X"], [self.home_away_axioms, self.tie_axioms])

        list.append(f'Total arbitrage (%) {self.arb}\n')

    def _add_string_to_list(self, list, cols, axioms_list):
        bet_sizes = bet_size.get_bet_sizes([axioms[0] for axioms in axioms_list], self.arb)
        col_width = 25*(5-len(cols))
        name_width = col_width-22
        total_width = 151+len(cols)

        list.extend([f'|{col:^{col_width}}' for col in cols])
        list.append(
            '|\n'
            f'{"_" * total_width}\n'
        )
        list.extend([f'|{"name":^{name_width}}|{"provider":^13}|{"odds":^7}' for _ in range(len(cols))])
        list.append('|\n')
        for i in range(min([len(axioms) for axioms in axioms_list])):
            list.extend([f'|{axioms[i].name:^{name_width}}|{axioms[i].provider:^13}|{str(round(axioms[i].odds, 7)):^7}'
                         for axioms in axioms_list])
            list.append('|\n')

        list.append(f'{"_" * total_width}\n')
        list.extend([f'|{"bet size":^{col_width}}' for _ in range(len(cols))])
        list.append(f'|\n')
        list.extend([f'|{str(round(size, 5)) + " dkk":^{col_width}}' for size in bet_sizes])
        list.append(f'|\n')

    def __eq__(self, other):
        return self.arb == other.arb

    def __lt__(self, other):
        return self.arb < other.arb

    def __le__(self, other):
        return self.arb <= other.arb
