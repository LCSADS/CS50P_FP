import whisper
import torch
from media import convert_to_mp3
# creates whisper model, base as parameter, can change in main if needed


def whisper_model(model_name="base"):
# checks cuda to know if it can use the gpu, if can't, uses the cpu to run the ai model
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Whisper model {model_name} running on {device}")
    model = whisper.load_model(model_name).to(device)
    return model

# language as optional parameter, "en" or "pt" for example
def audio_transcriber(model,file_path,language=None):
    print(f"Transcribing audio: {file_path}")
    if language:
        transcription = model.transcribe(file_path,language=language)
    else:
        transcription = model.transcribe(file_path)
    return transcription["text"]

def convert_and_transcribe(file_path,model_size="base",language=None):
    file_path = convert_to_mp3(file_path)
    model = whisper_model(model_size)
    transcription = audio_transcriber(model,file_path,language=language)
    return file_path,transcription