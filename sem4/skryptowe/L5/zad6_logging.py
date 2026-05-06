import sys
import random
import argparse
import logging
from pathlib import Path
from datetime import datetime

from zad1_parse_data import parse_stations, parse_measurements

import numpy as np

DEFAULT_YEAR = 2023

logger = logging.getLogger("AirQualityApp")

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level
    def filter(self, record):
        return record.levelno <= self.max_level

def setup_logging():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)


def get_units(data_path: str) -> set:
    units = set()
    path_to_data = Path(data_path)
    csv_files = list(path_to_data.glob("*csv"))
    logger.debug(f"Found {len(csv_files)} files with measurements.")
    
    csv_files = [str(file).split("/")[-1] for file in csv_files]
    for file in csv_files:
        parts = file.split("_")
        if len(parts) > 1:
            raw_unit = parts[1]
            if raw_unit != "PrekursoryZielonka":
                units.add(raw_unit)
    return units


def validate_date_range(start: str, end: str) -> bool:
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        return start_date <= end_date
    except ValueError:
        return False


def is_in_range(date_str: str, start: str, end: str) -> bool:
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        dt = datetime.strptime(date_str, "%m/%d/%y %H:%M")
        return start_date <= dt <= end_date
    except ValueError:
        return False


def main():
    setup_logging()
    
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-u", "--unit", required=True)
    common.add_argument("-df", "--date_first", default="2023-01-01")
    common.add_argument('-dl', '--date_last', default='2023-12-31')
    common.add_argument("-f", "--freq", default="24g")
    common.add_argument("-p", "--path", default=".")

    parser = argparse.ArgumentParser(description="Measurement search system")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Random station
    parser_one = subparsers.add_parser("random", parents=[common])

    # Statistical values
    parser_two = subparsers.add_parser("stats", parents=[common])
    parser_two.add_argument("-s", "--station", required=True, help="Station name (ex. 'DsBialka')")

    args = parser.parse_args()
    base_path = Path(args.path)
    stations_file = base_path / "data" / "stacje.csv"
    measurements_files = base_path / "data" / "measurements"

    if not stations_file.exists():
        logger.error(f"File {stations_file} does not exists!")
        sys.exit(1)

    stations_data = parse_stations(stations_file)

    # Units validation
    units = get_units(measurements_files)
    if args.unit not in units:
        logger.warning(f"Bad unit has been provided: {args.unit}")
        sys.exit(1)

    # Dates validation
    if not validate_date_range(args.date_first, args.date_last):
        logger.error(f"Given date information are not correct, use RRRR-MM-DD format!")
        sys.exit(1)

    filename_year = str(DEFAULT_YEAR)
    measurement_file = filename_year + '_' + args.unit + '_' + args.freq + '.csv'
    measurements_data = []
    
    try:
        measurements_data = parse_measurements(measurements_files / measurement_file)
    except FileNotFoundError:
        logger.error(f"File does not exist: {measurement_file}")
        sys.exit(1)

    if args.command == "random":
            stations = set()
            for data_row in measurements_data:
                if is_in_range(data_row.data, args.date_first, args.date_last):
                    stations.add(data_row.kod_stacji)
            
            if not stations:
                logger.info("No measurements found for give criteria.")
                return

            chosen_station = random.choice(list(stations))
            chosen_station_data = (stations_data[chosen_station])
            
            logger.info(f"Station: {chosen_station}")
            logger.info(f"Name: {chosen_station_data.nazwa_stacji}")
            logger.info(f"Address: {chosen_station_data.miejscowosc} {chosen_station_data.adres}")


    if args.command == "stats":
        measurements_list = []
        for data_row in measurements_data:
            if is_in_range(data_row.data, args.date_first, args.date_last) and args.station == data_row.kod_stacji:
                measurements_list.append(data_row.wartosc)

        if not measurements_list:
            logger.info(f"No measurements for station: {args.station}.")
            return

        mean = np.mean(measurements_list)
        std = np.std(measurements_list)

        logger.info(f"Station: {args.station}")
        logger.info(f"Unit: {args.unit}")
        logger.info(f"Mean: {mean}")
        logger.info(f"Std: {std}")


if __name__ == "__main__":
    main()