import src.scanning.dk.kambi.scanner as kambi
from scanning.dk.scanner_runner import run_scanner


def get_sport888(days=1, offset_hours=2):
    return kambi.get_kambi('888Sport', '888dk', days, offset_hours=offset_hours)


if __name__ == '__main__':
    run_scanner(get_sport888)
