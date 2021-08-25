import util.arb_calculator as ac
import re

class Bet:

    def __init__(self, home_name, away_name, home_odds, tie_odds, away_odds, home_odds_provider, tie_odds_provider,
                 away_odds_provider, time):
        self.home_name = self.sanitize(home_name)
        self.away_name = self.sanitize(away_name)
        self.home_odds = home_odds
        self.away_odds = away_odds
        self.tie_odds = tie_odds
        self.home_odds_provider = home_odds_provider
        self.away_odds_provider = away_odds_provider
        self.tie_odds_provider = tie_odds_provider
        self.time = time
        self.arb = ac.get_arb_percentage(home_odds, tie_odds, away_odds)

    def merge(self, other):
        if self.home_name.lower() == other.home_name.lower():
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

    def sanitize(self, original_name):
        name = re.sub(r'\s?((VMFD)|(A\.Ş\.)|(\(GUA\))|(\(KSA\))|(ZSC)|(HSK)|(HJK)|(PFC)|(PFK)|(RFK)|(MFK)|(CSD)|(CSM)|(OFK)|(OfK)|(Ofk)|(FSV)|(NK)|(CS)|(SP)|(FC)|(AP)|(EC)|(FH)|(RB)|(BA)|(AD)|(SV)|(SK)|(SC)|(AC)|(IFK)|(BK)|(IK)|(IF)|(1\.)|(FK)|(FV)|(TSV)|(TSG)|(TJ)|(CA)|(JK)|(CD))\s?', '', re.sub(r'St\.', 'St', re.sub(r'\s?\(((W(omen)?)|(k)|(Reserves))\)', '', original_name.replace('HIFK', 'Helsinki'))).replace('Utd', 'United').replace('F.C.', 'FC'))
        name = name.replace('/', ' ').replace('Ž', 'Z').replace('ı', 'u').replace('ç', 'ch').replace('Š', 'S').replace('Á', 'A').replace('š', 's').replace('ă', 'a').replace('ș', 's').replace('ß', 'ss').replace('Lok.', 'Lokomotiva').replace('â', 'a').replace('ø', 'o').replace('Ñ', 'N').replace('ü', 'u').replace('å', 'aa').replace('é', 'e').replace('Ö', 'O').replace('á', 'a').replace('-', ' ').replace('ö', 'o').replace('ó', ' ').replace('ä', 'a').replace('Í', 'I').replace('í', 'i').replace('ú', 'u').replace('Â', '').replace('\'', '').replace('´', '').replace('ñ', 'n')
        if ',' in name:
            x = name.split(', ')
            name = x[-1] + ' ' + x[0]
        synonym_table = {'Schweiz': 'Switzerland',
                         'Helsinki Helsinki': 'Helsinki',
                         'Lions Zurich': 'Lions',
                         'Athletico Paranaense PR': 'Paranaense',
                         'Athletico PR': 'Paranaense',
                         'Paranaense PR': 'Paranaense',
                         'Mannheim': 'Adler Mannheim',
                         'Zalgiris': 'Zalgiris Vilnius',
                         'VilniusZalgiris': 'Zalgiris Vilnius',
                         'Kobenhavn': 'Copenhagen',
                         'Neftchi': 'Neftchi Baku',
                         'NeftchiBaku': 'Neftchi Baku',
                         'Crvena Zvezda': 'Red Star Belgrade',
                         'KuPS': 'Kuopion Palloseura',
                         'NS Mura': 'Mura 05',
                         'Ns Mura': 'Mura 05',
                         'Zorya Luhansk': 'Zorya Lugansk',
                         'Zarya Lugansk': 'Zorya Lugansk',
                         'Coopsol': 'Deportivo Coopsol',
                         'Feyenoord': 'Feyenoord Rotterdam',
                         'Rennes': 'Stade Rennais',
                         'Zenit St Petersburg': 'Zenit',
                         'Zenit St Petersborg': 'Zenit',
                         'Celtic Glasgow': 'Celtic',
                         'Lobos UPNFM': 'Lobos de la UPNFM',
                         'RealEspana': 'Real Espana',
                         'Al Taawon': 'Al Taawon Buraidah',
                         'Raya2 Expansion': 'Raya II Expansion',
                         'Celaya': 'Club Celaya',
                         'Comunicaciones': 'Club Comunicaciones',
                         'AL Nassr': 'Al Nassr',
                         'AL Taawoun': 'Al Taawon Buraidah',
                         'Manama Club': 'Al Manama',
                         'Victoria': 'Victoria La Ceiba',
                         'FAS': 'FAS Santa Ana',
                         'Slovakiet': 'Slovakia',
                         'Østrig': 'Austria',
                         'Kansas City NWSL': 'Kansas City',
                         'Guayaquil Sc': 'Guayaquil City',
                         'Kuban': 'Urozhay Krasnodar',
                         'RW Oberhausen': 'Rot Weiss Oberhausen',
                         'Cologne II': 'Koln II',
                         'Cologne II (U23)': 'Koln II',
                         'Polen': 'Poland',
                         'Hviderusland': 'Belarus',
                         'Sp. San Lorenzo': 'Sportivo San Lorenzo',
                         'AlNajma Manama': 'Al Najma Club',
                         'Breiðablik': 'Breidablik Kopavogur',
                         'G2': 'G2 Esports',
                         'Dhamk': 'Al Dhamk',
                         'Dhamk (KSA)': 'Al Dhamk',
                         'SC Preussen 06 Munster': 'Preussen Munster',
                         'Lotte': 'VfL Sportfreunde Lotte 1929',
                         'Osteraakers': 'Osterakers',
                         'Osteraker': 'Osterakers',
                         'Osteraaker': 'Osterakers',
                         'KUerdingen 05': 'KUerdingen',
                         'Al Ahli Jeddah (KSA)': 'Al Ahli Jeddah',
                         'AlAhli SC Manama': 'Al Ahli (Manama)',
                         'Hafnarfjarðar': 'Hafnarfjordur',
                         'Frankrig': 'France',
                         'Bremer': 'Bremer1906',
                         'Huracan': 'Club Atletico Huracan',
                         'Atletico Huracan': 'Club Atletico Huracan',
                         'Platense Zacatecoluca': 'Platense Municipal Zacatecoluca',
                         'IsidroMetapan': 'Isidro Metapan',
                         'DETONA': 'DETONA Gaming',
                         'Bravos': 'Bravos Gaming',
                         'REDRAGON': 'Redragon',
                         'Misr ElMaqasha': 'Misr El Maqasha',
                         'Misr Lel Makasa': 'Misr El Maqasha',
                         'Danmark': 'Denmark',
                         'Slovenien': 'Slovenia',
                         'Osterakers': 'Osteraker',
                         'Guastatoya': 'Deportivo Guastatoya',
                         'Sporting': 'Sporting San Jose',
                         'Sharks': 'Sharks Esports',
                         'Deportes Union La Calera': 'Union La Calera',
                         'Defensa and Justicia': 'Defensa y Justicia',
                         'Atletico Lanus': 'Lanus',
                         'Gimnasia Y Esgrima La Plata': 'Gimnasia La Plata',
                         'Gimnasia L.P.': 'Gimnasia La Plata',
                         'Newport County': 'Newport County A',
                         'Newport': 'Newport County A',
                         'Municipal': 'Dep. Municipal',
                         'Vila NovaGO': 'Vila Nova-GO',
                         'Vila Nova': 'Vila Nova-GO',
                         'Vila NovaGoiania': 'Vila Nova-GO',
                         'Avai SC': 'Avai-SC',
                         'Avai': 'Avai-SC',
                         'AvaiSC': 'Avai-SC',
                         'Newcastle': 'Newcastle United',
                         'Guarani-SP': 'Guarani SP',
                         'Operário-PR': 'Operario Ferroviario EC PR',
                         'Operario PR': 'Operario Ferroviario EC PR',
                         'Guadalupe': 'Guadalupe',
                         'Racing Club': 'Racing Club Avellaneda',
                         'CA Central Cordoba SE': 'Central Córdoba de Santiago del Estero',
                         'Central Cordoba SDE': 'Central Córdoba de Santiago del Estero',
                         'Central Cordoba': 'Central Córdoba de Santiago del Estero',
                         'El Nacional (ECU)': 'Deportivo El Nacional',
                         'El Nacional': 'Deportivo El Nacional',
                         'Tepatitlan De Morelos': 'Tepatitlán de Morelos',
                         'Tepatitlan': 'Tepatitlán de Morelos',
                         'Venados': 'Venadostime',
                         'Atletico Nacional': 'Atletico Nacional Medellin',
                         'Edmonton(CAN)': 'Edmonton',
                         'Pumas Tabasco': 'Pumas de Tabasco',
                         'J. Darul Takzim II': 'Johor Darul Tazim II',
                         'Italien': 'Italy',
                         'Letland': 'Latvia',
                         'Sydkorea': 'South Korea',
                         'Norge': 'Norway',
                         'S Gloria Popesti Leordeni': 'Popesti Leordeni',
                         'Unirea 2004 Slobozia': 'Unirea Slobozia',
                         'Pumas De Tabasco': 'Pumas de Tabasco',
                         'Dorados': 'Dorados de Sinaloa',
                         'Dorados Sinaloa': 'Dorados de Sinaloa',
                         'Náutico-PE': 'Nautico Capibaribe',
                         'Nautico PE': 'Nautico Capibaribe',
                         'Nautico': 'Nautico Capibaribe',
                         'A': 'Centro Sportivo Alagoano',
                         'Alagoano AL': 'Centro Sportivo Alagoano',
                         'A-AL': 'Centro Sportivo Alagoano',
                         'Cartagena': 'Real Cartagena',
                         'Ungarn': 'Hungary',
                         'Saprissa': 'eportivo Saprissa',
                         'Jicaral': 'ADR Jicaral',
                         'Tampico Madero': 'Jaibos Tampico Madero',
                         'Khoromkhon Club': 'Khoromkhon',
                         'Thespakusatsu Gunma': 'Thespa Kusatsu',
                         'Thespakusatsu': 'Thespa Kusatsu',
                         'Hiroshima Sanfrecce': 'Hiroshima Sanfrecce',
                         'Hiroshima': 'Hiroshima Sanfrecce',
                         'Indien': 'India',
                         'Consadole Sapporo': 'Hokkaido Consadole Sapporo',
                         'Jeonbuk': 'Jeonbuk Hyundai Motors',
                         'Pohang Steelers': 'Pohang Steelers',
                         'Sendai': 'Vegalta Sendai',
                         'Incheon': 'Incheon United',
                         'ex-100PG': '100PingGods',
                         'Suwon Bluewings': 'Suwon Samsung Bluewings',
                         'Suwon': 'Suwon City',
                         'Joondalup': 'ECU Joondalup',
                         'Inglewood Utd': 'Inglewood United',
                         'Tampines Rovers': 'Tampines Rovers',
                         'Geylang International': 'Geylang International',
                         'Geylang Int.': 'Geylang International',
                         'Steinbach': 'Steinbach Haiger',
                         'Steinbach 1921': 'Steinbach Haiger',
                         'Mainz 05 II (U23)': 'Mainz 05 II',
                         'Mainz II': 'Mainz 05 II',
                         'Schalke 04 II (U23)': 'Schalke 04 II',
                         'Borussia Monchengladbach II (U23)': 'Borussia Mönchengladbach II',
                         'Kokand': 'Kokand 1912',
                         'Termez Surkhon': 'Surkhon Termez',
                         'Ararat Armenia': 'Ararat-Armenia',
                         ' Ararat Armenia': 'Ararat-Armenia',
                         'Noah': 'Noah Yerevan',
                         'Gute': 'Gute',
                         'Supersport Utd': 'Supersport United',
                         'Golden Arrows': 'Lamontville Golden Arrows',
                         'Club Rubio Nu': 'Rubio Nu',
                         'Complexity': 'Complexity Gaming',
                         'Finest': 'Team Finest',
                         'Banik Sokolov': 'FK Banik Sokolov',
                         'Sokolov': 'FK Banik Sokolov',
                         'Bohemians 1905': 'Bohemians Prague 1905',
                         'Bohemians': 'Bohemians Prague 1905',
                         'SK Lisen': 'Lisen Brno',
                         '1. FC Viktorie Prerov': 'Viktorie Prerov',
                         'Benesov': 'Benesov',
                         'Al Jazira Abu-Dhabi': 'Al Jazira SCC',
                         'Shabab Al Ahli Dubai': 'Shabab Al-Ahli Dubai',
                         'Jaro': 'FF Jaro',
                         'EIF Ekenas': 'Ekenäs IF',
                         'Ekenas Idrottsforening': 'Ekenäs IF',
                         'Ekenas Idrætsforening': 'Ekenäs IF',
                         'Eif': 'Ekenäs IF',
                         'Curico Unido': 'Curicó Unido',
                         'Melipilla': 'Deportes Melipilla',
                         'CD Melipilla': 'Deportes Melipilla',
                         'Fortuna Dusseldorf II': 'Fortuna Düsseldorf II',
                         'Fortuna Dusseldorf II (U23)': 'Fortuna Düsseldorf II',
                         'SV Rodinghausen': 'SV Rödinghausen',
                         'Rot Weiss Ahlen': 'Rot-Weiss Ahlen',
                         'SC Fortuna Cologne': 'Fortuna Köln',
                         'Fortuna Koln': 'Fortuna Köln',
                         'VfB Stuttgart II': 'VfB Stuttgart II (U21)',
                         'Froso': 'Froso IF',
                         'Al-Raed (KSA)': 'Al-Raed',
                         'Solvesborgs GIF': 'Solvesborgs',
                         'Solvesborgs GoIF': 'Solvesborgs',
                         'Prespa Birlik': 'KSF Prespa Birlik',
                         'Rosengaard 1917': 'Rosengaard',
                         'Rosengard': 'Rosengaard',
                         'Nordvarmland': 'Nordvärmland FF',
                         'ordvarmland FF': 'Nordvärmland FF',
                         'Nosaby': 'Nosaby IF',
                         'Husqvarna': 'Husqvarna FF',
                         'Wehen Wiesbaden': 'SV Wehen Wiesbaden',
                         'Duisburg': 'MSV Duisburg',
                         'Wurzburger Kickers': 'Wurzburger Kickers',
                         'Freiburg II': 'SC Freiburg II',
                         'Borussia Monchengladbach II': 'Borussia Monchengladbach II',
                         'eportivo Saprissa': 'Deportivo Saprissa',
                         'Jeonbuk Motors': 'Jeonbuk Hyundai Motors',
                         'Schalke II': 'Schalke 04 II',
                         'Mgladbach II': 'Borussia Monchengladbach II',
                         'Univ. Stellenbosch': 'Stellenbosch',
                         'Moroka Swallows': 'Swallows',
                         'Amazulu': 'AmaZulu',
                         'Unex Unicov': 'Unicov',
                         'NJS': 'Nurmijarven Jalkapalloseura',
                         'Nurmijarven JS': 'Nurmijarven Jalkapalloseura',
                         'PKKU': 'PK Keski-Uusimaa',
                         'Muharraq Club': 'Al Muharraq Sports Club',
                         'Ilves 2': 'Tampereen Ilves II',
                         'GrIFK': 'Grankulla IFK',
                         'Tampereen Viipurin Ilves Kissat': 'Ilves Kissat',
                         'Salpa': 'SalPa',
                         'Tallinna JK Kalev': 'JK Tallinna Kalev',
                         'Al-Raed': 'Al Raed',
                         'AL Raed': 'Al Raed',
                         'AL Hazem': 'Al Hazm',
                         'Al-Hazm (KSA)': 'Al Hazm',
                         'Rappe GO': 'Rappe',
                         'If Karlstad Fotbollutveckling': 'Karlstad',
                         'Karlstad II': 'Karlstad',
                         'Karlstad Fotbollutveckling': 'Karlstad',
                         'Ostersund': 'Ostersunds',
                         'Eslovs': 'Eslovs BK',
                         'Tord': 'IK Tord',
                         'Wiedenbruck 2000': 'Wiedenbruck',
                         'KUerdingen': 'Uerdingen',
                         'Uerdingen 05': 'Uerdingen',
                         'Angered BK': 'Angered MBIK',
                         'IF Karlstad Fotbollutveckling': 'IF Karlstad II',
                         'HB Koege': 'HB Koge',
                         'Asarums IF FK': 'Asarums IF',
                         'Tidaholms': 'Tidaholm',
                         'Enkoping': 'Enkopings',
                         'Täfteå': 'Taftea',
                         'VfL Osnabruck': 'VfL 1899 Osnabruck',
                         'Osnabruck': 'VfL 1899 Osnabruck'
                         }
        return synonym_table.get(name, name)

    def tostring(self):
        s = str(self.time) + '\n' + 'HOME: ' + self.home_name + ' vs AWAY: ' + self.away_name + '\n'
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

    def __hash__(self):
        return int(self.home_name.lower().__hash__() + self.away_name.lower().__hash__())# + self.time.__hash__())
