import util.arb_calculator as ac
import util.editing_distance as ed
import util.bet_size_calculator as bet_size


def _sanitize(name):
    if ',' in name:
        x = name.split(', ')
        name = x[-1] + ' ' + x[0]
    return name.lower()


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

    def __init__(self, home_name, away_name, home_odds, tie_odds, away_odds, home_odds_provider, tie_odds_provider,
                 away_odds_provider, time, sport=''):
        self.home_axioms = [self.Axiom(_sanitize(home_name), home_odds, home_odds_provider)]
        self.tie_axioms = [self.Axiom('x', tie_odds, tie_odds_provider)]
        self.away_axioms = [self.Axiom(_sanitize(away_name), away_odds, away_odds_provider)]

        self.time = time
        self.sport = sport

        self.arb = ac.get_arb_percentage(home_odds, tie_odds, away_odds)

    def merge(self, other):
        if ed.is_similar(self.home_axioms[0].name, other.home_axioms[0].name):
            for axiom in other.home_axioms:
                self.home_axioms.append(axiom)
            for axiom in other.tie_axioms:
                self.tie_axioms.append(axiom)
            for axiom in other.away_axioms:
                self.away_axioms.append(axiom)
        else:
            for axiom in other.away_axioms:
                self.home_axioms.append(axiom)
            for axiom in other.tie_axioms:
                self.tie_axioms.append(axiom)
            for axiom in other.home_axioms:
                self.away_axioms.append(axiom)

        if len(other.sport) > len(self.sport):
            self.sport = other.sport

        self.home_axioms.sort(reverse=True)
        self.tie_axioms.sort(reverse=True)
        self.away_axioms.sort(reverse=True)
        self.arb = ac.get_arb_percentage(self.home_axioms[0].odds,
                                         self.tie_axioms[0].odds,
                                         self.away_axioms[0].odds)

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
    
    def tostring(self):
        s = f'{self.time}\n'

        if self.sport != '':
            s += f'Sport: {self.sport}\n'

        h, t, a = bet_size.get_bet_sizes(self)
        if self.tie_odds() != 0:
            s += f'|{"HOME":^50}|{"TIE":^50}|{"AWAY":^50}|\n'
            s += f'{"_"*154}\n'
            s += f'|{"name":^28}|{"provider":^13}|{"odds":^7}|'
            s += f'{"name":^28}|{"provider":^13}|{"odds":^7}|'
            s += f'{"name":^28}|{"provider":^13}|{"odds":^7}|\n'
            for i in range(len(self.home_axioms)):
                s += f'|{self.home_axioms[i].name:^28}|{self.home_axioms[i].provider:^13}|{self.home_axioms[i].odds:^7}|'
                s += f'{self.tie_axioms[i].name:^28}|{self.tie_axioms[i].provider:^13}|{self.tie_axioms[i].odds:^7}|'
                s += f'{self.away_axioms[i].name:^28}|{self.away_axioms[i].provider:^13}|{self.away_axioms[i].odds:^7}|\n'
            s += f'{"_"*154}\n'
            s += f'|{"bet size":^50}|{"bet size":^50}|{"bet size":^50}|\n'
            s += f'|{str(int(h)) + " dkk":^50}|{str(int(t)) + " dkk":^50}|{str(int(a)) + " dkk":^50}|\n'
        else:
            s += f'|{"HOME":^50}|{"AWAY":^50}|\n'
            s += f'{"_"*103}\n'
            s += f'|{"name":^28}|{"provider":^13}|{"odds":^7}|'
            s += f'{"name":^28}|{"provider":^13}|{"odds":^7}|\n'
            for i in range(len(self.home_axioms)):
                s += f'|{self.home_axioms[i].name:^28}|{self.home_axioms[i].provider:^13}|{self.home_axioms[i].odds:^7}|'
                s += f'{self.away_axioms[i].name:^28}|{self.away_axioms[i].provider:^13}|{self.away_axioms[i].odds:^7}|\n'
            s += f'{"_"*103}\n'
            s += f'|{"bet size":^50}|{"bet size":^50}|\n'
            s += f'|{str(int(h)) + " dkk":^50}|{str(int(a)) + " dkk":^50}|\n'
        s += f'Total arbitrage (%) {self.arb}\n'
        return s

    def __eq__(self, other):
        return self.arb == other.arb

    def __lt__(self, other):
        return self.arb < other.arb

    def __le__(self, other):
        return self.arb <= other.arb
