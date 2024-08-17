from pytube import Playlist
import os
import subprocess
from multiprocessing import Pool


# Functin to download whole playlist at once.
def download_playlist():

    # Function to get playlist name uing pytube.
    def get_playlist_name(playlist_url):
        # Create a Playlist object
        playlist = Playlist(playlist_url)
        
        # Return the title of the playlist
        return playlist.title


    # Function to fetch video URLs from a playlist
    def fetch_video_urls(playlist_url):
        playlist = Playlist(playlist_url)
        video_urls = []
        for video in playlist.videos:
            video_urls.append(video.watch_url)
        return video_urls

    
    # Get playlis url from user.
    playlist_url = "https://www.youtube.com/watch?v=3jEw_atbO5M&list=PLj5GWDBCMHnZ1XApnYCAPz874rWmrlodT&pp=gAQBiAQB"
    # Fetch the playlist name.
    playlist_name = get_playlist_name(playlist_url)
    # Specify the downloaded video file path
    download_path = f'C:\\Users\\Suraj\\Desktop\\down_videos\\%s' % playlist_name

    
    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    def every_command():
        # Calling the get url of playlist function
        playlist_urls = fetch_video_urls(playlist_url)
        commands_in = []
        for url in playlist_urls:
            # Build the yt-dlp command
            command = [
                'yt-dlp',
                '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
                '-f','mp4',
                url
            ]
            commands_in.append(command)
        return commands_in
    
    def down_videos(command):
        # Execute the command in multi-processing
        return subprocess.run(command, check=True)


    commands = every_command()
    print(commands)

    #for command in commands:
        #print(down_videos(command))

    with Pool(processes=len(commands)) as pool:
        pool.map(down_videos, commands)

    


download_playlist()

