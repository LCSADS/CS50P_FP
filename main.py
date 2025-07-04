from pytubefix import YouTube
from time import sleep
import sys
import os
import subprocess
def main():
    while True:
        youtube_url = get_video_url()
        if not youtube_url:
            sys.exit(1)
# instanciating a youtube object from pytube library, handle error with try except catching all exceptions in a generic way
        try:
            yt_object = YouTube(youtube_url)
            print(yt_object.watch_url)
            title = yt_object.title
        except Exception as erro:
            print("Something went wrong")
            continue
# check if its' the correct video for better user experience
        confirmation = input(f"{title} is the video you want to download?\n Type [Y] or [N] ")
        while confirmation not in "YyNn":
            confirmation = input("Invalid choice. Type only 'Y' or 'N'")
        if confirmation in 'Yy':
# gives user the choice to download the video or just the audio
            chosen_format = ask_format()
            if chosen_format is None:
                print("Bye")
                sys.exit(1)
            break
        else:
            print("Ok, let's start again.")
    streams = get_download_streams(yt_object,chosen_format)
    chosen_file = options_and_choice(streams,chosen_format)
    file_path = download_file(chosen_file)
    if chosen_format == 'audio':
        convert_to_mp3(file_path)


def get_video_url():
    while True:
        url = input(" Type the URL from the youtube video you want to download. \n If you want to exit press enter without typing anything.")
        if url.startswith("https://") or not url:
            return url
        else:
            print("Invalid URL. Make sure it's a safe URL that starts with 'https://' ")

def ask_format():
    while True:
        choice = input("Type 1 to download the video(mp4) or type 2 to download just the audio(mp3). Press enter without typing anything to exit.")
        if not choice:
            return None
        elif choice == "1":
            return "video"
        elif choice == "2":
            return "audio"
        else:
            print("Please choose a valid option.")

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
        for i, audio, in enumerate(download_formats, start=1):
            print(f"{i}{audio.abr} - {bytes_to_mb(audio.filesize)} MB")
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
    except subprocess.CalledProcessError:
        print("Error in the conversion")
        return input_path    


main()