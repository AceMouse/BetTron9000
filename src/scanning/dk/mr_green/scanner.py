import src.scanning.dk.kambi.scanner as kambi
from scanning.dk.scanner_runner import run_scanner


def get_mr_green(days=1, offset_hours=2):
    return kambi.get_kambi('Mr Green', 'mgdk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scanner(get_mr_green)
