import re
from pathlib import Path
from typing import Dict, Tuple


def group_measurement_files_by_key(path: Path) -> Dict[Tuple, Path]:
    grouped_files = {}
    
    file_pattern = re.compile(r"^(\d{4})_(.+)_(\d+[A-Za-z]+)\.csv$")
    
    if not path.is_dir():
        return grouped_files
        
    for item in path.iterdir():
        if item.is_file():
            match = file_pattern.match(item.name)
            
            if match:
                year = match.group(1)
                unit = match.group(2)
                freq = match.group(3)
                
                key = (year, unit, freq)
                
                grouped_files[key] = item
                
    return grouped_files


if __name__ == "__main__":
    output = group_measurement_files_by_key(Path("./data/measurements"))
    print(*output.items(), sep="\n")