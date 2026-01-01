import tkinter as tk
from tkinter import filedialog
import os
from yt_dlp import YoutubeDL

# Function to download the video
def downloadvid(url, save_path):
    try:
        # Ensure the save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Define download options with stealth settings
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],
                }
            },
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        }

        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Video downloaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")




def openfile():
    folder = filedialog.askdirectory()
    if folder:
        print (f"selected folder is {folder}")

    return folder

root = tk.Tk()
root.withdraw()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    video_url = input ("please enter url: ")
    save_dir = openfile()

    if not save_dir:
        print("please select folder bro")

    else:
        print("starting download...")
        downloadvid(video_url, save_dir)