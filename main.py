from pytubefix import YouTube
from time import sleep
import sys
import os
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
    chosen_file = video_resolution_choice(yt_object,chosen_format)
    download_file(chosen_file)
    





def get_video_url():
    while True:
        url = input(" Type the URL from the youtube video you want to download. \n If you want to exit press enter without typing anything.")
        if url.startswith("https://") or not url:
            return url
        else:
            print("Invalid URL. Make sure it's a safe URL that starts with 'https://' ")

# download video

# allow user to choose mp3 or mp4

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


# choose quality
# the youtube object generates stream objects inside of it, listed inside another object, streamquery
# manipulating the stream obj inside streamquery obj enables me to use methods like .download and atributes like filesize
def video_resolution_choice(yt_object,chosen_format):
    if chosen_format == 'video':
        # streamquery here                    filter audio+video files                order by decreasing resolution                        
        download_formats = yt_object.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc()
# in case there's only one download option avaible
        if len(download_formats) == 1:
            print(f"Only one option avaible: {download_formats[0].resolution}")
            chosen_file = download_formats[0]
            return chosen_file
# in case there are multiple avaible options for the user to select. Iterates over the list, returns the video choice. While loop for catching errors and better ux.
        else:
            print("Avaible options for download: ")
            for i, video in enumerate(download_formats, start=1):
                print(f"[{i}]{video.resolution} - {round(video.filesize / (1024*1024), 2)} MB")

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
    for _ in range(3):
        sleep(0.5)
        print(".",end='',flush=True)
    chosen_file.download(output_path="downloads")
    print("\nDownload completed.")

        

    

# transcribe audio

main()