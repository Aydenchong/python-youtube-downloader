import tkinter as tk
import os
from tkinter import filedialog
from checkyt import is_valid_url
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import AudioFileClip

def selfolder():
    savepath = filedialog.askdirectory()
    fldrpath.set(savepath)
    # print(savepath)

def dwnldvid():
    url = url_en.get()
    save_path = fldrpath.get()
    # if not save_path:
    # if os.path.exists(save_path) == False:
    #     messagebox.showerror("Error", "Please select a folder to save the video")
    #     return

    if not is_valid_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL")

    mp3success = False
    mp4success = False

    try:
        yt = YouTube(url)
        if mp3var.get():
            aud_strim = yt.streams.filter(only_audio = True).first()
            if aud_strim:
                out_file = aud_strim.download(output_path = save_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + ".mp3"
                aud_clip = AudioFileClip(out_file)
                aud_clip.write_audiofile(new_file)
                aud_clip.close()
                os.remove(out_file)
                mp3success = True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download audio {e}")

    try:
        yt = YouTube(url)
        # print(yt.streams)
        if mp4var.get():
            vid_strim =yt.streams.filter(progressive = True, file_extension = "mp4").order_by("resolution").desc().first()

            if vid_strim:
                vid_strim.download(save_path)
                mp4success = True

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video {e}")

    if mp4success or mp3success:
        message = "Successfully downloaded:\n"
        if mp3success:
            message += "MP3\n"
        if mp4success:
            message += "MP4\n"
        messagebox.showinfo("Success", message)

window = tk.Tk()

fldrpath = tk.StringVar()
mp3var = tk.BooleanVar()
mp4var = tk.BooleanVar()

window.title("YouTube Video Downloader")
yturl = tk.Label(window, text = "YouTube URL: ")
yturl.pack()
url_en = tk.Entry(window, width = 50)
url_en.pack(padx=20)
mp4 = tk.Checkbutton(window, text = "Download MP4", variable = mp4var)
mp4.pack()
mp3 = tk.Checkbutton(window, text = "Download MP3", variable = mp3var)
mp3.pack()
foldr = tk.Button(window, text = "Choose Folder", command = selfolder)
foldr.pack()
folder = tk.Entry(window, textvariable = fldrpath, width = 50)
folder.pack(padx=20)
dwnld = tk.Button(window, text = "Download", command = dwnldvid)
dwnld.pack(pady=10)

window.mainloop()