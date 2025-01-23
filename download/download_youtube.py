import yt_dlp
from pytube import Playlist
import os
import subprocess
from multiprocessing import Pool

class YouTubeDownloader:
    """
    A class to download videos from YouTube, Instagram, and other platforms using yt-dlp and pytube.
    """

    def __init__(self, download_path):
        """
        Initialize the downloader with a specific download path.

        :param download_path: The path where videos will be saved.
        """
        self.download_path = download_path

    def download_video(self, command):
        """
        Execute a download command using subprocess.

        :param command: The download command to execute.
        :return: The result of the subprocess.run command.
        """
        try:
            result = subprocess.run(command, check=True)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}. Skipping to the next video.")
    
    def execute_commands(self, commands):
        """
        Execute multiple download commands concurrently using multiprocessing.

        :param commands: A list of download commands to execute.
        """
        print(f"No. of videos = {len(commands)}")
        with Pool(processes=min(len(commands), os.cpu_count())) as pool:
            pool.map(self.download_video, commands)

    def download_single_video(self, video_url):
        """
        Download a single video from a given URL.

        :param video_url: The URL of the video to download.
        """
        command = ['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                   '--merge-output-format', 'mp4',
                    '-o', os.path.join(self.download_path, '%(title)s.%(ext)s'), video_url]
        result = self.download_video(command)
        print(result)

    def get_playlist_name(self, playlist_url):
        """
        Retrieve the name of a YouTube playlist.

        :param playlist_url: The URL of the playlist.
        :return: The title of the playlist.
        """
        playlist = Playlist(playlist_url)
        return playlist.title

    def fetch_video_urls(self, playlist_url):
        """
        Get all video URLs from a YouTube playlist.

        :param playlist_url: The URL of the playlist.
        :return: A list of video URLs.
        """
        playlist = Playlist(playlist_url)
        return [video.watch_url for video in playlist.videos]

    def download_playlist(self, playlist_url):
        """
        Download all videos from a YouTube playlist.

        :param playlist_url: The URL of the playlist.
        """
        playlist_name = self.get_playlist_name(playlist_url)
        download_path = os.path.join(self.download_path, playlist_name)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(self.fetch_video_urls(playlist_url), download_path)
        self.execute_commands(commands)

    def download_many_videos(self, urls, folder_name):
        """
        Download multiple videos given their URLs and save them in a specified folder.

        :param urls: A list of video URLs.
        :param folder_name: The name of the folder to save the videos.
        """
        download_path = os.path.join(self.download_path, folder_name)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(urls, download_path)
        self.execute_commands(commands)

    def create_commands(self, urls, download_path):
        """
        Create a list of download commands for a list of URLs.

        :param urls: A list of video URLs.
        :param download_path: The path where videos will be saved.
        :return: A list of download commands.
        """
        return [
            ['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                '--merge-output-format', 'mp4',
                '-o', os.path.join(download_path, '%(title)s.%(ext)s'), url]
            for url in urls
        ]

    def get_all_video_urls(self, channel_url):
        """
        Retrieve all video URLs from a YouTube channel.

        :param channel_url: The URL of the YouTube channel.
        :return: A list of video URLs.
        """
        ydl_opts = {
            'extract_flat': True,  # Extract video URLs without downloading them
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)

        if 'entries' in result:
            video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in result['entries']]
            return video_urls
        else:
            print("No videos found.")
            return []

    def download_channel(self, video, foldername, short=None):
        """
        Download all videos and shorts from a YouTube channel.

        :param video: The URL of the channel's videos.
        :param short: The URL of the channel's shorts.
        :param foldername: The name of the folder to save the videos.
        """
        channel_video_urls = self.get_all_video_urls(video)
        short = short

        if short:
            channel_short_urls = self.get_all_video_urls(short)
            channel_video_urls.extend(channel_short_urls)

        download_path = os.path.join(self.download_path, foldername)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        commands = self.create_commands(channel_video_urls, download_path)
        self.execute_commands(commands)

    def __call__(self):
        """
        Call function to enable the callability of this class.
        """
        print("1. Download single Youtube video \n2. Download Youtube playlist \n3. Download many Youtube videos \n4. Download whole youtube channel ")
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

            if not short:
                self.download_channel(video,foldername,)
            else:
                self.download_channel(video,  foldername,short)
            

if __name__ == "__main__":
    # Replace 'C:\\Users\\Suraj\\Desktop\\down_videos' with your desired download path
    downloader = YouTubeDownloader('C:\\Users\\admin\\Desktop\\down_videos')
    downloader()