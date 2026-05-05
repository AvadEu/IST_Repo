import csv
import re


def read_station_data(file_path: str) -> list:
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        return [row for row in reader if len(row) >= 15]


def get_dates(rows: list) -> set:
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    dates = set()
    for row in rows:
        date_start = row[5]
        date_stop = row[6]
        if date_pattern.match(date_start):
            dates.add(date_start)
        if date_pattern.match(date_stop):
            dates.add(date_stop)
    return dates


def get_coordinates(rows: list) -> set:
    coord_pattern = re.compile(r"^\d{1,2}\.\d{6}$")
    coords = set()
    for row in rows:
        lat = row[13]
        lon = row[14]
        if coord_pattern.match(lat):
            coords.add(lat)
        if coord_pattern.match(lon):
            coords.add(lon)
    return coords


def get_two_part_names(rows: list) -> list:
    two_part_pattern = re.compile(r"^[^-\n]+-[^-\n]+$")
    names = []
    for row in rows:
        station_name = row[3]
        if two_part_pattern.match(station_name):
            names.append(station_name)
    return names


def get_modified_names(rows: list) -> list:
    space_pattern = re.compile(r"\s+")
    pl_pattern = re.compile(r"[ąćęłńóśżźĄĆĘŁŃÓŚŻŹ]")
    
    pl_chars = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ż': 'Z', 'Ź': 'Z'
    }
    
    def remove_diacritics(match):
        return pl_chars[match.group(0)]
        
    modified_names = []
    for row in rows:
        station_name = row[3]
        name_underscored = space_pattern.sub("_", station_name)
        name_cleaned = pl_pattern.sub(remove_diacritics, name_underscored)
        modified_names.append(name_cleaned)
    return modified_names


def validate_mob_stations(rows: list) -> bool:
    mob_pattern = re.compile(r"MOB$")
    for row in rows:
        station_code = row[1]
        station_type = row[9]
        if mob_pattern.search(station_code):
            if station_type.lower() != 'mobilna':
                return False
    return True


def get_three_part_locations(rows: list) -> list:
    three_part_pattern = re.compile(r"^[^-\n]+-[^-\n]+-[^-\n]+$")
    locations = []
    for row in rows:
        station_name = row[3]
        
        if three_part_pattern.match(station_name):
            locations.append(station_name)
    return locations


def get_comma_street_locations(rows: list) -> list:
    comma_street_pattern = re.compile(r",.*\b(?:ul\.|al\.)", re.IGNORECASE)
    locations = []
    for row in rows:
        station_name = row[3]

        if comma_street_pattern.search(station_name):
            locations.append(station_name)
    return locations


if __name__ == "__main__":
    dane_stacji = read_station_data("data/stacje.csv")
    
    dates = get_dates(dane_stacji)
    coordinates = get_coordinates(dane_stacji)
    two_word_names = get_two_part_names(dane_stacji)
    modified_names = get_modified_names(dane_stacji)
    mobile_validation = validate_mob_stations(dane_stacji)
    three_word_names = get_three_part_locations(dane_stacji)
    adres_colon = get_comma_street_locations(dane_stacji)
    print(three_word_names)