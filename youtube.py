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

        # Define download options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save file path
            'cookiesfrombrowser': ('chrome',),  # Use Chrome cookies if needed
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