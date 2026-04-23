import os
import csv
import mimetypes
from datetime import datetime

def get_converted_dir() -> str:
    default_dir = os.path.join(os.getcwd(), 'converted')
    converted_dir = os.environ.get('CONVERTED_DIR', default_dir)
    
    os.makedirs(converted_dir, exist_ok=True)
    return converted_dir

def find_files(directory: str) -> list:
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Given path '{directory}' is not an existing directory.")
    
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

def detect_tool(filepath: str) -> str:
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(filepath)
    
    if mime_type:
        if mime_type.startswith('image/'):
            return 'magick'
        elif mime_type.startswith('video/') or mime_type.startswith('audio/'):
            return 'ffmpeg'
            
    ext = filepath.lower().rsplit('.', 1)[-1]
    if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff']:
        return 'magick'
    elif ext in ['mp4', 'mp3', 'wav', 'webm', 'avi', 'mkv', 'flac', 'ogg']:
        return 'ffmpeg'
        
    return None

def log_conversion(history_path: str, orig_path: str, target_format: str, out_path: str, tool: str):
    file_exists = os.path.isfile(history_path)
    
    with open(history_path, mode='a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Timestamp", 
                "OriginalPath", 
                "OutputFormat", 
                "OutputPath", 
                "ProgramUsed"
            ])
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, orig_path, target_format, out_path, tool])
