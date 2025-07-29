from interface import confirm
from pathlib import Path

def save_as_txt(file_path,transcription):
    if not transcription:
        print("There was no transcription.")
        return
    file_path = Path(file_path)
    text_folder = file_path.parent / "transcriptions"
    text_folder.mkdir(exist_ok=True)
    text_path = text_folder / f"{file_path.stem}.txt"
    with open(text_path,"w",encoding="utf-8") as text_file:
        text_file.write(transcription)
    print(f"Transcription saved to {text_path}")
    if confirm("Do you want to print the transcription on the terminal?"):
        print(transcription)


def save_as_srt(file_path,srt_caption):
    file_path = Path(file_path)
    caption_folder = file_path.parent / "captions"
    caption_folder.mkdir(exist_ok=True)
    caption_path = caption_folder / f"{file_path.stem}.srt"
    with open(caption_path,"w",encoding="utf-8") as caption_file:
        caption_file.write(srt_caption)
    print(f"Caption saved to {caption_path}")
    return str(caption_path)

def select_from_list(options,message=""):
    while True:
        try:
            user_input = int(input(f"\n{message}"))
            if user_input == 0:
                return None
            if 1 <= user_input <= len(options):
                return options[user_input - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}. Type 0 to exit the program")
        except ValueError:
            print("Please enter a valid number.")