import src.scanning.dk.kambi.scanner as kambi
from scanning.dk.scanner_runner import run_scanner


def get_leo_vegas(days=1, offset_hours=2):
    return kambi.get_kambi('LeoVegas', 'leodk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scanner(get_leo_vegas)
