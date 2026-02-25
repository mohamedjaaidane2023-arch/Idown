import os
import yt_dlp


class VideoDownloader:
    def __init__(self, download_path, ffmpeg_path=None):
        self.download_path = download_path
        self.ffmpeg_path = ffmpeg_path

    def download(self, url, resolution, progress_callback=None):

        if resolution == "best":
            format_string = "bestvideo+bestaudio/best"
        else:
            format_string = f"bestvideo[height<={resolution}]+bestaudio/best"

        ydl_opts = {
            "format": format_string,
            "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",

            # 🔥 THIS FIXES THE OPUS PROBLEM
            "postprocessor_args": [
                "-c:v", "copy",      # keep video stream
                "-c:a", "aac",       # convert audio to AAC
                "-b:a", "192k"       # audio bitrate
            ],

            "noplaylist": True,
            "quiet": True
        }

        if self.ffmpeg_path:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_path

        if progress_callback:
            ydl_opts["progress_hooks"] = [progress_callback]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])