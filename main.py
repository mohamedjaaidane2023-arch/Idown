from tkinter import Tk
from gui.app import VideoDownloaderApp


def main():
    root = Tk()
    root.title("Video Downloader")
    root.geometry("600x420")
    root.resizable(False, False)

    app = VideoDownloaderApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()