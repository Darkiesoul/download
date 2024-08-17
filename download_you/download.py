import os
from pytube import Playlist
import subprocess
from multiprocessing import Pool

# Functin to download whole playlist at once woth multiprocessing.
def download_video(command):
        # Execute the command in multi-processing
        return subprocess.run(command, check=True)

# Function to download a single Youtube video.
def download_single_video():
    # URL of the YouTube video you want to download
    video_url = input("Enter the video url: ")
    
    # Command to download the  video in mp4 format using yt-dlp
    command = ['yt-dlp', '-f', 'mp4','-o',f'C:\\Users\\admin\\Desktop\\down_videos\\%(title)s.%(ext)s', video_url]

    # Execute the command
    result = download_video(command)

    # Output the result
    print(result)

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
    playlist_url = input("Enter the playlist url: ")
    # Fetch the playlist name.
    playlist_name = get_playlist_name(playlist_url)
    # Specify the downloaded video file path
    download_path = f'C:\\Users\\admin\\Desktop\\down_videos\\%s' % playlist_name

    
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
    
    


    commands = every_command()
    print(f"No. of videos = {len(commands)}")

    try :
        with Pool(processes=len(commands)) as pool:
            pool.map(download_video, commands)

    except:
        RuntimeError

# Function to download many videos at on (given urls).
def download_many_videos():
    
    def url_list():
        # Initialize an empty list to store inputs
        urls = []

        # Start an infinite loop
        while True:
            # Prompt the user for input
            url = input("Enter a value (or type 'done' to finish): ")
            
            # Check if the user wants to exit the loop
            if url.lower() == 'done':
                break
            
            # Append the input to the list
            urls.append(url)

        # Print the resulting list
        return urls


    # Fetch the playlist/file folder  name.
    playlist_name = input("Enter the folder name: ")
    # Specify the downloaded video file path
    download_path = f'C:\\Users\\admin\\Desktop\\down_videos\\%s' % playlist_name

    
    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    def every_command():
        # Calling the get url of playlist function
        all_urls = url_list()
        commands_in = []
        for url in all_urls:
            # Build the yt-dlp command
            command = [
                'yt-dlp',
                '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
                '-f','mp4',
                url
            ]
            commands_in.append(command)
        return commands_in
    
    

    commands = every_command()
    print(commands)
    print(len(commands))

    try :
        with Pool(processes=len(commands)) as pool:
            pool.map(download_video, commands)

    except:
        RuntimeError

# Main function.
def main():

    print("1.Download single Youtube video \n2.Download Youtube playlist \n3.Download many Youtube videos")
    number = int(input("Enter the number: "))

    if number==1:
        # To download a single video
        download_single_video()

    elif number==2:
        # To downlod whole playlist
        download_playlist()

    else:
        # To download many videos
        download_many_videos()


if __name__ == "__main__":
    main()