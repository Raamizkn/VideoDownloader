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

        # Define download options with robust headers
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'cachedir': False,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Origin': 'https://www.youtube.com',
                'Referer': 'https://www.youtube.com/',
            },
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