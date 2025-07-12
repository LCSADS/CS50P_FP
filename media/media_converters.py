import os
import subprocess

def bytes_to_mb(size_in_bytes):
    return round(size_in_bytes / (1024 * 1024), 2)

def convert_to_mp3(input_path):
    if not input_path.endswith(".m4a"):
        return input_path
    output_path = input_path.replace(".m4a",".mp3")
    try:
        subprocess.run(["ffmpeg","-y","-i",input_path,"-acodec","libmp3lame",output_path],check=True)
        os.remove(input_path)
        print("MP3 conversion sucessfull.")
        return output_path
    except subprocess.CalledProcessError:
        print("Error in the conversion")
        return input_path    
    
