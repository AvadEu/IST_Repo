import sys
import subprocess
from pathlib import Path
from typing import List

METADATA_SCRIPT = "zad4_text_metadata.py"

def argument_validation() -> str:
    if len(sys.argv) == 2:
        path = Path(sys.argv[1])
        if path.is_dir():
            return sys.argv[1]
        else:
            raise RuntimeError("Provide a correct path!")
    else:
        raise RuntimeError("Usage: script.py <directory_path>!")


def get_file_paths(path: str) -> List[str]:
    return [str(file) for file in Path(path).glob("*.txt")]


def process_files(file_paths: List[str]) -> List[dict]:
    dict_list = []
    for file in file_paths:
        process = subprocess.run(
            ['python', METADATA_SCRIPT],
            input=file,
            text=True,
            capture_output=True
        )

        output = process.stdout.strip()
        current_dict = {}
        splitted_csv = output.split('\n')
        for k, v in zip(splitted_csv[0].split(','), splitted_csv[1].split(',')):
            current_dict[k] = v
        dict_list.append(current_dict)
    return dict_list


def process_output(processed_data: List[dict]) -> dict:
    sum_chars = 0
    sum_words = 0
    sum_lines = 0
    common_char = ''
    common_char_num = 0
    common_word = ''
    common_word_num = 0
    for meta_dict in processed_data:
        sum_chars += int(meta_dict['NumChars'])
        sum_words += int(meta_dict['NumWords'])
        sum_lines += int(meta_dict['NumLines'])
        curr_common_char_num = int(meta_dict['MCCharNum'])
        curr_common_word_num = int(meta_dict['MCWordNum'])
        if curr_common_char_num > common_char_num:
            common_char = meta_dict['MCChar']
            common_char_num = curr_common_char_num
        if curr_common_word_num > common_word_num:
            common_word = meta_dict['MCWord']
            common_word_num = curr_common_word_num
        return {
            'FilesRead': len(processed_data),
            'SumChars': sum_chars,
            'SumWords': sum_words,
            'SumLines': sum_lines,
            'MCChar': common_char,
            'MCWord': common_word
        }


if __name__ == "__main__":
    try:
        path = argument_validation()
    except RuntimeError as e:
        print(f'Error: {e}')
    
    file_paths = get_file_paths(path)
    processed_data  = process_files(file_paths)
    outcome = process_output(processed_data)
    
    for k, v in outcome.items():
        print(f'{k}: {v}')