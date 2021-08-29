import util.arb_calculator as ac
import util.editing_distance as ed

class Bet:
    def __init__(self, home_name, away_name, home_odds, tie_odds, away_odds, home_odds_provider, tie_odds_provider,
                 away_odds_provider, time, sport=''):
        self.home_name = self.sanitize(home_name)
        self.away_name = self.sanitize(away_name)
        self.merged_in_home_names = set()
        self.merged_in_away_names = set()
        self.merged_in_home_names.add(self.home_name)
        self.merged_in_away_names.add(self.away_name)
        self.home_odds = home_odds
        self.away_odds = away_odds
        self.tie_odds = tie_odds
        self.home_odds_provider = home_odds_provider
        self.away_odds_provider = away_odds_provider
        self.tie_odds_provider = tie_odds_provider
        self.time = time
        self.arb = ac.get_arb_percentage(home_odds, tie_odds, away_odds)
        self.sport = sport

    def merge(self, other):
        if ed.is_similar(self.home_name.lower(), other.home_name.lower()):
            self.merged_in_home_names.add(other.home_name)
            self.merged_in_away_names.add(other.away_name)
            if float(self.home_odds) < float(other.home_odds):
                self.home_odds = other.home_odds
                self.home_odds_provider = other.home_odds_provider
            if float(self.tie_odds) < float(other.tie_odds):
                self.tie_odds = other.tie_odds
                self.tie_odds_provider = other.tie_odds_provider
            if float(self.away_odds) < float(other.away_odds):
                self.away_odds = other.away_odds
                self.away_odds_provider = other.away_odds_provider
        else:
            if float(self.home_odds) < float(other.away_odds):
                self.home_odds = other.away_odds
                self.home_odds_provider = other.away_odds_provider
            if float(self.tie_odds) < float(other.tie_odds):
                self.tie_odds = other.tie_odds
                self.tie_odds_provider = other.tie_odds_provider
            if float(self.away_odds) < float(other.home_odds):
                self.away_odds = other.home_odds
                self.away_odds_provider = other.home_odds_provider
        self.arb = ac.get_arb_percentage(self.home_odds, self.tie_odds, self.away_odds)
        if len(other.sport) > len(self.sport):
            self.sport = other.sport

    def sanitize(self, name):
        if ',' in name:
            x = name.split(', ')
            name = x[-1] + ' ' + x[0]
        return name

    def tostring(self):
        s = str(self.time) + '\n' + 'HOME: ' + self.home_name + ' vs AWAY: ' + self.away_name + '\n'
        s += 'HOME: ' + str(self.merged_in_home_names) + ' vs AWAY: ' + str(self.merged_in_away_names) + '\n'
        if self.sport != '':
            s += 'Sport:' + self.sport + '\n'
        if self.tie_odds == '0':
            s += '2 outcomes: HOME: ' + self.home_odds_provider + ' vs AWAY: ' + self.away_odds_provider + '\n'
            s += '            HOME: ' + str(self.home_odds) + ' vs AWAY: ' + str(self.away_odds)
        else:
            s += '3 outcomes: HOME: ' + self.home_odds_provider + ' vs TIE: ' + self.tie_odds_provider + ' vs AWAY: ' + self.away_odds_provider + '\n'
            s += '            HOME: ' + str(self.home_odds) + ' vs TIE: ' + str(self.tie_odds) + ' vs AWAY: ' + str(
                self.away_odds)
        s += '\nTotal arbitrage (%) ' + str(self.arb)
        return s

    def __eq__(self, other):
        return self.arb == other.arb

    def __lt__(self, other):
        return self.arb < other.arb

    def __le__(self, other):
        return self.arb <= other.arb
