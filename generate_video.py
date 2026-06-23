#finds new folder and creates reel out of them if not done already
import os
from text_to_audio import text_to_speech_file
import subprocess
import time

def text_to_audio(folder):
    print(folder)
    text = ""
    path = f"uploads\\{folder}\\user_text.txt"
    with open(path,"r") as f:
        text = f.read()
    print(text,folder)
    text_to_speech_file(text,folder)
    print(folder)

def create_reel(folder):
    print('running the command')
    subprocess.run([
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", f"uploads/{folder}/input.txt",
    "-i", f"uploads/{folder}/audio.mp3",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-shortest",
    "-r", "30",
    "-pix_fmt", "yuv420p",
    f"static/reels/{folder}.mp4"
], check=True)
    print('command ran')
    

if __name__=="__main__":
    while True:
        with open("done.txt","r") as f:
            done_folders = f.readlines()
        done_folders = [f.strip('\n') for f in done_folders]
        folders = os.listdir("uploads")
        for folder in folders:
            if(folder not in done_folders):    
                text_to_audio(folder)
                print('create reel method starting')
                create_reel(folder)
                print('create reel method finished')
                with open("done.txt","a") as d:
                    d.write(folder+"\n")
        print("Queue processed")
        time.sleep(3)
