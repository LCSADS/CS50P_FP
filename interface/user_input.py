import sys


def get_video_url():
    while True:
        url = input(" Type the URL from the youtube video you want to download. \n If you want to exit press Enter without typing anything.")
        if url.startswith("https://") or not url:
            return url
        else:
            print("Invalid URL. Make sure it's a safe URL that starts with 'https://' ")

def ask_format():
    while True:
        print("Choose the download format \n[1] Video \n[2] Audio")
        user_choice = input("Type 1 to download the video(mp4) or type 2 to download just the audio(mp3) or press Enter to exit.")
        if not user_choice:
            sys.exit("Bye!")
        elif user_choice == "1":
            return "video"
        elif user_choice == "2":
            return "audio"
        else:
            print("Please choose a valid option.")

def confirm(message):
    while True:
        user_answer = input(f"{message} \n Type [Y] for yes or [N] for no or press Enter to exit.").strip().upper()
        if not user_answer:
            sys.exit("Bye!")             
        elif user_answer in 'YN':               
            if user_answer == 'Y':
                return True
            elif user_answer == 'N':
                return False            
        else:
            print(f"Please type [Y] for yes or [N] for no or press Enter to exit")
 