import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube 
import os
from PIL import Image, ImageTk
import pyperclip

# Function to download the video
def download_video():
    url = url_entry.get()
    resolution = resolution_var.get()

    progress_label.pack(pady=10)
    progress_bar.pack(pady=10)
    status_label.pack(pady=10)

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution, progressive=True).first()
        print(yt.title)

        # Download video into a generic directory (user's home directory)
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_path, f"{yt.title}.mp4")
        stream.download(output_path=downloads_path, filename=f"{yt.title}.mp4")
        
        status_label.configure(text="Downloaded!", text_color="white", fg_color="green")
        print("Available Streams:")
        for s in yt.streams:
            print(s)

    except Exception as e:
        status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    print(percentage_completed)

# Function to clear the entry box
def clear():
    url_entry.delete(0, "end")

# Function to paste the link automatically
def paste():
    url_entry.delete(0, "end")
    url_entry.insert(0, pyperclip.paste())

# Create a root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Title of the window
root.title("YouTube Video Downloader!")

# Set min and max width and height of the window
root.geometry("1080x720")
root.minsize(720, 480)

# Create a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# Create a label and entry widget for the video URL
url_label = ctk.CTkLabel(content_frame, text="Enter the URL here: ", font=('Times New Roman', 18))
url_entry = ctk.CTkEntry(content_frame, width=500, height=40)
url_label.pack(pady=10)
url_entry.pack(pady=10)

# Create a button to clear the entry label
remove_button = ctk.CTkButton(content_frame, text="⌧", command=clear, anchor="TOP", width=10, fg_color="red")
remove_button.pack()

# Create a button to paste URL in the entry label
paste_button = ctk.CTkButton(content_frame, text="⌨", command=paste, width=10, fg_color="green")
paste_button.pack(side='top', pady=10)

# Create a button for downloading
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=10)

# Create a label for the resolution selection
quality_label = ctk.CTkLabel(content_frame, text="Select the resolution: ", font=('Lucida', 15))
quality_label.pack()

# Create a resolution combo box
resolutions = ["1080p", "720p", "360p", "240p", "144p"]
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvariable=resolution_var, width=50, height=30, font=("Lucida", 10, "bold"))
resolution_combobox.pack(padx=10, pady=5)
resolution_combobox.set("720p")

# Create a label and the progress bar to display the download progress
progress_label = ctk.CTkLabel(content_frame, text="100%")
progress_bar = ctk.CTkProgressBar(content_frame, width=500)
progress_bar.set(1)

# Create a status label
status_label = ctk.CTkLabel(content_frame, text="Downloaded")

# Run the main loop
root.mainloop()
