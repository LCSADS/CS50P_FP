from pytubefix import YouTube
import sys
import youtube
import transcriber
import media
import interface
import utils
import workflow
def main():
    yt_object = youtube.get_youtube_video()
    chosen_format = interface.ask_format()
    file_path = youtube.select_and_download(yt_object,chosen_format)
    if chosen_format == 'audio':
        workflow.handle_audio(file_path,model_size="small",language="en")
    if chosen_format == 'video':
        workflow.handle_video(yt_object,file_path)

if __name__ == "__main__":
    main()
    