from pytubefix import YouTube
import os
from media.media_converters import bytes_to_mb
from time import sleep
import sys
from interface.user_input import confirm
from utils.utils import select_from_list
from pathlib import Path


def get_download_streams(yt_object,chosen_format):
    if chosen_format == 'video':
        # streamquery here                    filter audio+video files                order by decreasing resolution                        
        download_formats = yt_object.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc()
    elif chosen_format == 'audio':
# abr orders by bitrates, descending order(most bitrates first, best quality first)
        download_formats = yt_object.streams.filter(only_audio=True).order_by("abr").desc()
    return download_formats

def options_and_choice(download_formats,chosen_format):
    if len(download_formats) == 1:
         only_stream = download_formats[0]
         label = format_label(only_stream,chosen_format)
         print (f"Only one option available {label}")
         return only_stream

    print("Avaible options for download:")
    for i,stream in enumerate(download_formats,start=1):
        print(f"[{i}] {format_label(stream,chosen_format)}")
    user_choice = select_from_list(download_formats,message="Type the corresponding number to select a resolution. 0 to exit the program.")
    if user_choice is None:
        sys.exit("Bye!")
    return user_choice

def download_file(chosen_file,chosen_format):
    download_folder = Path("downloads") / chosen_format
    download_folder.mkdir(parents=True,exist_ok=True)
    print("Please wait",end='',flush=True)
    for _ in range(5):
        sleep(0.5)
        print(".",end='',flush=True)
    try:
        output_path = chosen_file.download(output_path=download_folder)
        if not output_path or not Path(output_path).exists():
            raise FileNotFoundError("Failed!")
        print("\nDownload completed.")
        return output_path
    except Exception as erro:
        print(f"Download failed\n{erro}")
        return None
def validate_yt_object(url):
     try:
          yt = YouTube(url)
          return yt
     except Exception:
          print(f"Invalid url")
          return None

def get_youtube_video():
     while True:
        url = input("Type the URL from the youtube video you want to download. \n If you want to exit press enter without typing anything.").strip()
        if not url:
            print("Bye!")
            sys.exit(1)
        yt_video = validate_yt_object(url)
        if yt_video is None:
             continue
        elif confirm(f" {yt_video.title} is the video you want to download?"):
             return yt_video

def select_and_download(yt_object,chosen_format):
    streams = get_download_streams(yt_object,chosen_format)
    chosen_file = options_and_choice(streams,chosen_format)
    file_path = download_file(chosen_file,chosen_format)
    return file_path

def format_label(stream,chosen_format):
    if chosen_format == 'video':
         return f"{stream.resolution} - {bytes_to_mb(stream.filesize)} MB"
    else:
         return f"{stream.abr} - {bytes_to_mb(stream.filesize)} MB"


def available_captions(yt_object):
# instanciates a captionquery object and treat errors
    try:
        captions_query = yt_object.captions
    except Exception as erro:
        print(f"Couldn't access the captions.\n {erro}")
        return None
    
    if not captions_query:
        print("There's no captions available for this video.")
        return None
# creates a list of the contents of the object, caption code represents the "en" or "pt" and caption is the actual caption object, pass as touple to deal with each pair of values   
    captions_items = []
    for caption in captions_query:
        try:
            caption_code = caption.code
            captions_items.append((caption_code,caption))
        except AttributeError: #
            continue

    if not captions_items:
        print("No captions available")
        return None
# iterates and print over that list       
    print("Available captions :")
    for i, (caption_code,caption) in enumerate(captions_items,start=1):
        name = caption.name or ""
        print(f"[{i}] - {caption_code} {name}")
# user select caption
    try:
        chosen_caption = select_from_list(captions_items,message="Choose a caption by its corresponding number (0 to cancel)")
    except Exception as erro:
        print(f"Selection interrupted or invalid: {erro}")
        return None
        
    if chosen_caption is None:
        return None
# unpacks the touple and use generate srt method in the caption object, returns the srt caption.      
    _,caption_file = chosen_caption
    return caption_file

    
    

    
