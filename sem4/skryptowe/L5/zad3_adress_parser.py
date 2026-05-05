import re
import csv
from pathlib import Path

def get_addresses(path: Path, city: str) -> list:
    addresses = []
    
    if not path.is_file():
        return addresses
        
    # Wzorzec do parsowania adresu:
    # 1. (?:ul\.\s*|al\.\s*)? - opcjonalnie ignoruje przedrostki "ul." lub "al." (non-capturing group)
    # 2. (.*?) - leniwe dopasowanie nazwy ulicy (Grupa 1)
    # 3. (?:\s+([0-9]+[A-Za-z0-9\/\-]*))?$ - opcjonalny numer budynku na końcu, 
    #    zaczynający się od cyfry, mogący zawierać litery i znaki / lub - (Grupa 2)
    address_pattern = re.compile(r"^(?:ul\.\s*|al\.\s*)?(.*?)(?:\s+([0-9]+[A-Za-z0-9\/\-]*))?$")
    
    city_pattern = re.compile(rf"^{re.escape(city)}$", re.IGNORECASE)
    
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            if len(row) < 13:
                continue
                
            wojewodztwo = row[10]
            miejscowosc = row[11]
            adres_raw = row[12]
            
            if city_pattern.match(miejscowosc):
                if not adres_raw.strip():
                    addresses.append((wojewodztwo, miejscowosc, "", None))
                    continue
                    
                match = address_pattern.match(adres_raw)
                
                if match:
                    ulica = match.group(1).strip()
                    numer = match.group(2) if match.group(2) else None
                    
                    addresses.append((wojewodztwo, miejscowosc, ulica, numer))
                    
    return addresses

if __name__ == "__main__":
    output = get_addresses(Path("./data/stacje.csv"), "Bogatynia")
    print(*output, sep="\n")