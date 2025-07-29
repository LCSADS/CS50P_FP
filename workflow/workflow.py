from transcriber import convert_and_transcribe
from utils import save_as_txt, save_as_srt
from interface import confirm
from youtube import available_captions
from media import burn_in_captions

def handle_audio(file_path,model_size="base",language=""):
    if confirm("Do you want to transcribe the audio?"):
        file_path, transcription = convert_and_transcribe(file_path,model_size=model_size,language=language)
        if file_path and transcription:
            save_as_txt(file_path,transcription)
            return file_path,transcription
        else:
            print(f"Transcription failed.")
            return None,None
    
def handle_video(yt_object,file_path):
    if confirm("Do you want to download captions for this video?"):
        captions = available_captions(yt_object)
        if captions:
            srt_caption = captions.generate_srt_captions()
            caption_path = save_as_srt(file_path,srt_caption)
        if confirm("Do you want to burn in captions for the video?"):
            burn_in_captions(file_path,caption_path)
            
        