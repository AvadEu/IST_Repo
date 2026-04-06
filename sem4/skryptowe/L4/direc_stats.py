import sys 
import subprocess
import os
from typing import List
import json

EXECUTABLE_FILE = "/Users/macbookair/Studia/IST_Repo/sem4/skryptowe/L4/file_stats.py"

def get_files_list(dir_path: str) -> List[str]:
    try:
        command = subprocess.run(
            ["find", dir_path, "-type", "f"],
            capture_output=True,
            text=True,
            check=True
        )
        
        full_paths = command.stdout.splitlines()
        return full_paths
    
    except subprocess.CalledProcessError as e:
        print(f"Error running find: {e}")
        return []
    
def process_file(file_path: str):
    try:
        command = subprocess.run(
            [file_path, " | ", "python3 ", EXECUTABLE_FILE],
            capture_output=True,
            text=True,
            check=True
        )

        json_stats = command.stdout
        stats = json.loads(json_stats)
        return stats
    
    except subprocess.CalledProcessError as e:
        print(f"Error running find: {e}")
        return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py /path/to/directory")
    else:
        path = sys.argv[1]
        lista_plikow = get_files_list(path)
        print(process_file(lista_plikow[0]))