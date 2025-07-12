from interface import confirm

def save_as_txt(file_path,transcription):
    with open(file_path.replace(".mp3",".txt"),"w", encoding="utf-8") as text:
        text.write(transcription)
    print ("Transcription sucessfull")
    confirm("Do you want to print the transcription?")
    if confirm:
        print(transcription)
    