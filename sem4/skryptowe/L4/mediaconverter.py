import argparse
import os
import subprocess
from datetime import datetime
import utils

def main():
    parser = argparse.ArgumentParser(description="Automatic media conversion tool.")
    parser.add_argument("input_dir", type=str, help="Path do directory with original files")
    parser.add_argument("format", type=str, help="Output Format")
    args = parser.parse_args()

    output_dir = utils.get_converted_dir()
    history_file = os.path.join(output_dir, "history.csv")

    try:
        files = utils.find_files(args.input_dir)
    except NotADirectoryError as e:
        print(f"Error: {e}")
        return

    if not files:
        print(f"No files in: {args.input_dir}")
        return

    print(f"Found files: {len(files)}.")
    print("-" * 50)

    for file_path in files:
        tool = utils.detect_tool(file_path)
        
        if not tool:
            print(f"Skipping {file_path} file format not detected.")
            continue

        original_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(original_name)[0]
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S") # np. 20250324153000
        output_filename = f"{timestamp_str}-{name_without_ext}.{args.format}"
        output_path = os.path.join(output_dir, output_filename)

        if tool == 'ffmpeg':
            cmd = ['ffmpeg', '-y', '-i', file_path, output_path]
        elif tool == 'magick':
            cmd = ['magick', file_path, output_path]

        print(f"Processing {original_name} -> {output_filename} (using: {tool})")
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            utils.log_conversion(history_file, file_path, args.format, output_path, tool)
            print("Success!")
            
        except subprocess.CalledProcessError:
            print("Error: Convertion failed, check file integrity.")
        except FileNotFoundError:
            print(f"Error: '{tool}' cannot be found. Please install it via your local package manager")
            
    print("-" * 50)
    print("Finished. History stored in:", history_file)

if __name__ == "__main__":
    main()