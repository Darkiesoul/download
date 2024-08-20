import yt_dlp
import instaloader
from pytube import Playlist
import os
import subprocess
from multiprocessing import Pool


class YouTubeDownloader:
    def __init__(self, download_path):
        self.download_path = download_path

    def download_video(self, command):
        return subprocess.run(command, check=True)
    
    def execute_commands(self, commands):
        print(f"No. of videos = {len(commands)}")
        with Pool(processes=min(len(commands), os.cpu_count())) as pool:
            pool.map(self.download_video, commands)

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

    def get_all_video_urls(self, channel_url):
        ydl_opts = {
            'extract_flat': True,  # Extract video URLs without downloading them
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)

        # Check if it's a playlist or a channel
        if 'entries' in result:
            # Extract video URLs
            video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in result['entries']]
            return video_urls
        else:
            print("No videos found.")
            return []

    def download_channel(self, video, short, foldername):
        channel_video_urls = self.get_all_video_urls(video)
        channel_short_urls = self.get_all_video_urls(short)

        channel_video_urls.extend(channel_short_urls)

        download_path = os.path.join(self.download_path, foldername)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(channel_video_urls, download_path)
        self.execute_commands(commands)

    def main(self):
        print("1. Download single Youtube/Instagram video \n2. Download Youtube playlist \n3. Download many Youtube/Instagram videos \n4. Download whole youtube channel \n5. Download whole instagram profile reels.")
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

        elif choice == 4:
            video = input("Enter the video channel channel url : ")
            short = input("Enter the short channel channel url : ")
            foldername = input("Enter the channel name : ")

            self.download_channel(video, short, foldername)
            

if __name__ == "__main__":
    downloader = YouTubeDownloader('C:\\Users\\Suraj\\Desktop\\down_videos')
    downloader.main()
