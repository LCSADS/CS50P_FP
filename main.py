from pytubefix import YouTube
import sys
import youtube
import transcriber
import media
import interface
import utils
def main():
    yt_object = youtube.get_youtube_video()
    chosen_format = interface.ask_format()
    file_path = youtube.select_and_download(yt_object,chosen_format)
    if chosen_format == 'audio':
        file_path, transcription = transcriber.convert_and_transcribe(file_path,model_size="small",language="pt")
        utils.save_as_txt(file_path,transcription)
if __name__ == "__main__":
    main()