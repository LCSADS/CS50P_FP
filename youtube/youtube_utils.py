from pytubefix import YouTube
import os
from media.media_converters import bytes_to_mb
from time import sleep
import sys
from interface.user_input import confirm


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
            if chosen_format == 'video':
                print(f"Only one option available: {download_formats[0].resolution}")
                chosen_file = download_formats[0]
                return chosen_file
            else:
                print(f"Only one option available : {download_formats[0].abr}")
                chosen_file = download_formats[0]
                return chosen_file
    elif chosen_format == 'video':
        print("Available options for download: ")
        for i, video in enumerate(download_formats, start=1):
            print(f"[{i}]{video.resolution} - {bytes_to_mb(video.filesize)} MB")
    elif chosen_format =='audio':
        print("Available options for download: ")
        for i, audio in enumerate(download_formats, start=1):
            print(f"[{i}]- {audio.abr} - {bytes_to_mb(audio.filesize)} MB")
    while True:
                try:
                    user_choice = int(input("Type the corresponding number to select a resolution."))
                    if user_choice in range(1,len(download_formats)+1):
                        chosen_file = download_formats[user_choice - 1]
                        break
                    else:
                        print("Please type the corresponding number with the option you want to select.")
                except ValueError:
                    print("Please type a valid number")
    return chosen_file

def download_file(chosen_file):
    os.makedirs("downloads",exist_ok=True)
    print("Please wait",end='',flush=True)
    for _ in range(5):
        sleep(0.5)
        print(".",end='',flush=True)
    output_path = chosen_file.download(output_path="downloads")
    print("\nDownload completed.")
    return output_path

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
    file_path = download_file(chosen_file)
    return file_path