from pytube import Playlist
import os
import subprocess
from multiprocessing import Pool

# Function to execute the command
def down_videos(command):
    subprocess.run(command, check=True)

def download_playlist():
    # Function to get playlist name using pytube
    def get_playlist_name(playlist_url):
        playlist = Playlist(playlist_url)
        return playlist.title

    # Function to fetch video URLs from a playlist
    def fetch_video_urls(playlist_url):
        playlist = Playlist(playlist_url)
        video_urls = []
        for video in playlist.videos:
            video_urls.append(video.watch_url)
        return video_urls

    # Get playlist URL from the user
    playlist_url = input("Enter the playlist URL: ")
    playlist_name = get_playlist_name(playlist_url)
    
    # Specify the download path
    download_path = f'C:\\Users\\Suraj\\Desktop\\down_videos\\%s' % playlist_name
    
    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Function to build the yt-dlp command
    def build_command(url):
        return [
            'yt-dlp',
            '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
            '-f', 'mp4',
            url
        ]

    # Fetch the playlist URLs
    playlist_urls = fetch_video_urls(playlist_url)
    commands = [build_command(url) for url in playlist_urls]

    # Use multiprocessing to download videos in parallel
    with Pool(processes=len(commands)) as pool:
        pool.map(down_videos, commands)

download_playlist()
