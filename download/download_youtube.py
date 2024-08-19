import os
from pytube import Playlist
import subprocess
from multiprocessing import Pool

class YouTubeDownloader:
    def __init__(self, download_path):
        self.download_path = download_path

    def download_video(self, command):
        return subprocess.run(command, check=True)

    def download_single_video(self, video_url):
        command = ['yt-dlp', '-f', 'mp4', '-o', os.path.join(self.download_path, '%(title)s.%(ext)s'), video_url]
        result = self.download_video(command)
        print(result)

    def get_playlist_name(self, playlist_url):
        playlist = Playlist(playlist_url)
        return playlist.title

    def fetch_video_urls(self, playlist_url):
        playlist = Playlist(playlist_url)
        return [video.watch_url for video in playlist.videos]

    def download_playlist(self, playlist_url):
        playlist_name = self.get_playlist_name(playlist_url)
        download_path = os.path.join(self.download_path, playlist_name)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(self.fetch_video_urls(playlist_url), download_path)
        self.execute_commands(commands)

    def download_many_videos(self, urls, folder_name):
        download_path = os.path.join(self.download_path, folder_name)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(urls, download_path)
        self.execute_commands(commands)

    def create_commands(self, urls, download_path):
        return [
            ['yt-dlp', '-o', os.path.join(download_path, '%(title)s.%(ext)s'), '-f', 'mp4', url]
            for url in urls
        ]

    def execute_commands(self, commands):
        print(f"No. of videos = {len(commands)}")
        with Pool(processes=min(len(commands), os.cpu_count())) as pool:
            pool.map(self.download_video, commands)

    def main(self):
        print("1. Download single Youtube video \n2. Download Youtube playlist \n3. Download many Youtube videos")
        choice = int(input("Enter the number: "))

        if choice == 1:
            video_url = input("Enter the video url: ")
            self.download_single_video(video_url)

        elif choice == 2:
            playlist_url = input("Enter the playlist url: ")
            self.download_playlist(playlist_url)

        elif choice == 3:
            urls = []
            while True:
                url = input("Enter a video url (or type 'done' to finish): ")
                if url.lower() == 'done':
                    break
                urls.append(url)
            folder_name = input("Enter the folder name: ")
            self.download_many_videos(urls, folder_name)


if __name__ == "__main__":
    downloader = YouTubeDownloader('C:\\Users\\admin\\Desktop\\down_videos')
    downloader.main()
