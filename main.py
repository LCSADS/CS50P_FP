from pytube import YouTube
def main():
    youtube_url = get_video_url()
# instanciating a youtube object from pytube library
    yt_object = YouTube(youtube_url)
    ask_format()
# get youtube url
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
            break
        elif choice == "1":
            return "video"
        elif choice == "2":
            return "audio"
        else:
            print("Please choose a valid option.")


# choose quality

def video_resolution_choice()
    

# transcribe audio

main()