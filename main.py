from pytubefix import YouTube
import sys
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
        confirmation = input(f"{title} is the video you want to download?\n Y/N")
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
# the youtube object generates stream objects inside of it, listed in another object, streamquery
# manipulating the stream obj inside streamquery obj enables me to use methods like .download and atributes like filesize
def video_resolution_choice(yt,chosen_format):
    if chosen_format == 'video':
        # streamquery here
        download_formats = yt.streams.filter(progressive=True,file_extension="mp4").order_by("resolution")
    

# transcribe audio

main()