import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.downloader import VideoDownloader


class VideoDownloaderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Professional Video Downloader")
        self.root.geometry("600x420")
        self.root.resizable(False, False)

        self.download_path = os.getcwd()
        self.ffmpeg_path = "C:\\ffmpeg\\bin"  # change if needed

        self.create_widgets()

    def create_widgets(self):

        # URL
        tk.Label(self.root, text="Video URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=70)
        self.url_entry.pack(pady=5)

        # Resolution
        tk.Label(self.root, text="Resolution:").pack(pady=5)
        self.resolution = ttk.Combobox(
            self.root,
            values=["best", "1080", "720", "480", "360"]
        )
        self.resolution.current(0)
        self.resolution.pack(pady=5)

        # Folder Button
        tk.Button(self.root, text="Choose Download Folder",
                  command=self.choose_folder).pack(pady=10)

        self.folder_label = tk.Label(
            self.root,
            text=f"Folder: {self.download_path}"
        )
        self.folder_label.pack()

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

        # Download Button
        self.download_btn = tk.Button(
            self.root,
            text="Download",
            width=20,
            command=self.start_download
        )
        self.download_btn.pack(pady=15)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.folder_label.config(text=f"Folder: {self.download_path}")

    def start_download(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        self.download_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_label.config(text="Starting download...")

        threading.Thread(
            target=self.download_thread,
            args=(url,),
            daemon=True
        ).start()

    def download_thread(self, url):
        resolution = self.resolution.get()

        downloader = VideoDownloader(
            self.download_path,
            self.ffmpeg_path
        )

        try:
            downloader.download(
                url,
                resolution,
                self.progress_hook
            )
            self.update_status("Download Completed ✅")
        except Exception as e:
            self.update_status("Download Failed ❌")
            messagebox.showerror("Download Error", str(e))
        finally:
            self.download_btn.config(state="normal")

    def progress_hook(self, d):

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)

            if total:
                percent = downloaded / total * 100
                self.root.after(0, self.update_progress, percent)

        elif d["status"] == "finished":
            self.root.after(0, self.update_status, "Merging video & audio...")

    def update_progress(self, percent):
        self.progress["value"] = percent
        self.status_label.config(text=f"Downloading... {percent:.1f}%")

    def update_status(self, message):
        self.status_label.config(text=message)