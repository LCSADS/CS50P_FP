import os
import subprocess
from pathlib import Path
from interface import confirm

def bytes_to_mb(size_in_bytes):
    return round(size_in_bytes / (1024 * 1024), 2)

def convert_to_mp3(input_path):
    if not input_path.endswith(".m4a"):
        return input_path
    output_path = input_path.replace(".m4a",".mp3")
    try:
        subprocess.run(["ffmpeg","-y","-i",input_path,"-acodec","libmp3lame",output_path],check=True)
        os.remove(input_path)
        print("MP3 conversion sucessfull.")
        return output_path
    except subprocess.CalledProcessError as erro:
        print(f"Error in the conversion\n{erro}")   
        return None    
    
def burn_in_captions(video_path,caption_path):
    video_path = Path(video_path)
    if not Path(caption_path).exists():
        print("Caption file wasn't found. Burn in failed.")
        return None
# the caption path, is interpreted by ffmpeg not by python/cmd so this method from pathlib replaces all "\" with "/"
# for the same reason i need to escape "":" in "C:", on ffmpeg, filter="" has ":" as a parameter, so it conflicts with the path in the captions, but not the video.
# because the video doesn't pass through the filter="" argument in the ffmpeg command.
    caption_path = Path(caption_path).as_posix()
    caption_path = caption_path.replace("C:","C\\:")
# stem removes the extension from the file name, .suffix adds it back after adding _"burned" to the name of the video. 
    captioned_video = f"{video_path.stem}_burned{video_path.suffix}"
# with name method creates the complete path, to the same directory, "C://..."" again, using the new name attributed to captioned_video above
    output_path = video_path.with_name(captioned_video)
# escapes the double quotes with simple quotes to protect the captions path being passed for the ffmpeg filter=""    
    subtitles_filter = f"subtitles='{caption_path}'"


# "ffmpeg" calls ffmpeg. "y" overwrites the video without asking, add because maybe you can use the program more than one time and it wont crash even if you download the same video
# "i" is the input file, str with the video path, "-vf" is video filter, in this case, subtitles filter. "-c:a" is the audio coded, "copy" for only copying the audio, no re-encoding
    command = ["ffmpeg","-y","-i",str(video_path),"-vf",subtitles_filter,"-c:a","copy",str(output_path)]
    try:
        subprocess.run(command,check=True)
        print(f"Burn in complete!: {output_path}")
        return str(output_path)
    except subprocess.CalledProcessError as erro:
        print(f"Burning captions failed!\n{erro}")
        return None
