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

    def __init__(self, home_name, away_name, home_odds, tie_odds, away_odds, provider, time,
                 home_x_odds=0, x_away_odds=0, home_away_odds=0,
                 sport=''):
        self.home_axioms = [self.Axiom(_sanitize(home_name), home_odds, provider)]
        self.tie_axioms = [self.Axiom('x', tie_odds, provider)]
        self.away_axioms = [self.Axiom(_sanitize(away_name), away_odds, provider)]

        self.home_x_axioms = [self.Axiom(f'{_sanitize(home_name)} or x', home_x_odds, provider)]
        self.x_away_axioms = [self.Axiom(f'x or {_sanitize(away_name)}', x_away_odds, provider)]
        self.home_away_axioms = [
            self.Axiom(f'{_sanitize(home_name)} or {_sanitize(away_name)}', home_away_odds, provider)]
        self.time = time
        self.sport = sport

        self.arb = \
            self.arb_match_result = \
            self.arb_double_x_away = \
            self.arb_double_home_x = \
            self.arb_double_home_away = 0

    def sort_axioms(self):
        self.home_axioms.sort(reverse=True)
        self.tie_axioms.sort(reverse=True)
        self.away_axioms.sort(reverse=True)
        self.home_x_axioms.sort(reverse=True)
        self.x_away_axioms.sort(reverse=True)
        self.home_away_axioms.sort(reverse=True)
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
        list.append(
            f'{self.time}'
            f'\n'
        )

        if self.sport != '':
            list.append(
                f'Sport: {self.sport}'
                f'\n'
            )

        if self.arb_match_result == self.arb:

            if self.tie_odds() != 0:
                h, t, a = bet_size.get_3bet_sizes(self.home_axioms[0], self.tie_axioms[0], self.away_axioms[0], self.arb)
                list.append(
                    f'|{"HOME":^50}|{"TIE":^50}|{"AWAY":^50}|\n'
                    f'{"_" * 154}\n'
                    f'|{"name":^28}|{"provider":^13}|{"odds":^7}|'
                    f'{"name":^28}|{"provider":^13}|{"odds":^7}|'
                    f'{"name":^28}|{"provider":^13}|{"odds":^7}|'
                    f'\n'
                )
                for i in range(len(self.home_axioms)):
                    list.append(
                        f'|{self.home_axioms[i].name:^28}|{self.home_axioms[i].provider:^13}|{self.home_axioms[i].odds:^7}|'
                        f'{self.tie_axioms[i].name:^28}|{self.tie_axioms[i].provider:^13}|{self.tie_axioms[i].odds:^7}|'
                        f'{self.away_axioms[i].name:^28}|{self.away_axioms[i].provider:^13}|{self.away_axioms[i].odds:^7}|'
                        f'\n'
                    )
                list.append(
                    f'{"_" * 154}\n'
                    f'|{"bet size":^50}|{"bet size":^50}|{"bet size":^50}|\n'
                    f'|{str(round(h, 5)) + " dkk":^50}|{str(round(t, 5)) + " dkk":^50}|{str(round(a, 5)) + " dkk":^50}|'
                    f'\n'
                )
            else:
                self._add_2way_string_to_list(list, "HOME", "AWAY", self.home_axioms, self.away_axioms)

        elif self.arb_double_home_x == self.arb:
            self._add_2way_string_to_list(list, "HOME or X", "AWAY", self.home_x_axioms, self.away_axioms)

        elif self.arb_double_x_away == self.arb:
            self._add_2way_string_to_list(list, "HOME", "X or AWAY", self.home_axioms, self.x_away_axioms)

        elif self.arb_double_home_away == self.arb:
            self._add_2way_string_to_list(list, "HOME or AWAY", "X", self.home_away_axioms, self.tie_axioms)

        list.append(
            f'Total arbitrage (%) {self.arb}'
            f'\n'
        )

    def _add_3way_string_to_list(self, list, col1, col2, col3, axioms1, axioms2, axioms3):
        bet_size1, bet_size2, bet_size3 = bet_size.get_3bet_sizes(axioms1[0], axioms2[0], axioms3[0], self.arb)
        list.append(
            f'|{col1:^50}|{col2:^50}|{col3:^50}|\n'
            f'{"_" * 103}\n'
            f'|{"name":^28}|{"provider":^13}|{"odds":^7}|'
            f'{"name":^28}|{"provider":^13}|{"odds":^7}|\n'
        )
        for i in range(len(axioms1)):
            list.append(
                f'|{axioms1[i].name:^28}|{axioms1[i].provider:^13}|{str(round(axioms1[i].odds, 7)):^7}|'
                f'{axioms2[i].name:^28}|{axioms2[i].provider:^13}|{str(round(axioms2[i].odds, 7)):^7}|'
                f'{axioms3[i].name:^28}|{axioms3[i].provider:^13}|{str(round(axioms3[i].odds, 7)):^7}|'
                f'\n'
            )
        list.append(
            f'{"_" * 154}\n'
            f'|{"bet size":^50}|{"bet size":^50}|{"bet size":^50}|\n'
            f'|{str(round(bet_size1, 5)) + " dkk":^50}|{str(round(bet_size2, 5)) + " dkk":^50}|{str(round(bet_size3, 5)) + " dkk":^50}|'
            f'\n'
        )

    def _add_2way_string_to_list(self, list, col1, col2, axioms1, axioms2):
        bet_size1, bet_size2 = bet_size.get_2bet_sizes(axioms1[0], axioms2[0], self.arb)
        list.append(
            f'|{col1:^75}|{col2:^75}|\n'
            f'{"_" * 153}\n'
            f'|{"name":^53}|{"provider":^13}|{"odds":^7}|'
            f'{"name":^53}|{"provider":^13}|{"odds":^7}|\n'
        )
        for i in range(len(axioms1)):
            list.append(
                f'|{axioms1[i].name:^53}|{axioms1[i].provider:^13}|{str(round(axioms1[i].odds, 7)):^7}|'
                f'{axioms2[i].name:^53}|{axioms2[i].provider:^13}|{str(round(axioms2[i].odds, 7)):^7}|'
                f'\n'
            )
        list.append(
            f'{"_" * 153}\n'
            f'|{"bet size":^75}|{"bet size":^75}|\n'
            f'|{str(round(bet_size1, 5)) + " dkk":^75}|{str(round(bet_size2, 5)) + " dkk":^75}|'
            f'\n'
        )

    def __eq__(self, other):
        return self.arb == other.arb

    def __lt__(self, other):
        return self.arb < other.arb

    def __le__(self, other):
        return self.arb <= other.arb
