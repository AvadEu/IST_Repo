import csv
from collections import namedtuple
from typing import Dict, NamedTuple, List

Station = namedtuple('Station', [
    'nr', 'kod_stacji', 'kod_miedzynarodowy', 'nazwa_stacji', 
    'stary_kod', 'data_uruchomienia', 'data_zamkniecia', 
    'typ_stacji', 'typ_obszaru', 'rodzaj_stacji', 
    'wojewodztwo', 'miejscowosc', 'adres', 'lat', 'lon'
])

Measurement = namedtuple('Measurement', [
    'data', 'kod_stacji', 'wartosc', 'wskaznik', 'jednostka'
])


def parse_stations(file_path: str) -> Dict[str, NamedTuple]:
    stations_dict = {}
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 
        
        for row in reader:
            if len(row) < 15:
                continue
                
            station = Station(*row[:15])
            stations_dict[station.kod_stacji] = station
            
    return stations_dict


def parse_measurements(file_path: str) -> List[NamedTuple]:
    measurements_list = []
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        next(reader) 
        row_kod_stacji = next(reader)
        row_wskaznik = next(reader)
        next(reader) 
        row_jednostka = next(reader)
        next(reader) 
        
        kody_stacji = row_kod_stacji[1:]
        wskazniki = row_wskaznik[1:]
        jednostki = row_jednostka[1:]
        
        for row in reader:
            if not row:
                continue
                
            data_pomiaru = row[0]
            wartosci = row[1:]
            
            for i, wartosc_str in enumerate(wartosci):
                if wartosc_str.strip() == '':
                    continue 
                    
                try:
                    wartosc = float(wartosc_str)
                    pomiar = Measurement(
                        data=data_pomiaru,
                        kod_stacji=kody_stacji[i],
                        wartosc=wartosc,
                        wskaznik=wskazniki[i],
                        jednostka=jednostki[i]
                    )
                    measurements_list.append(pomiar)
                except ValueError:
                    pass 
                    
    return measurements_list


if __name__ == "__main__":
    output = parse_measurements('./data/measurements/2023_As(PM10)_24g.csv')
    print(output[1])