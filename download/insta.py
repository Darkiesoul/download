import subprocess

def download_instagram_post(post_url, path, cookies_path=None,):
    """
    Downloads a single Instagram post using yt-dlp.
    
    Parameters:
    - post_url (str): URL of the Instagram post.
    - cookies_path (str, optional): Path to the cookies.txt file for authentication. Default is None.
    - output_path (str): Directory where the downloaded file will be saved. Default is the current directory.
    """
    # Base yt-dlp command
    command = ['yt-dlp','-f','b', '-o', f'{path}/%(title)s.%(ext)s', post_url]
    
    # Add cookies if provided
    if cookies_path:
        command.extend(['--cookies', cookies_path])
    
    try:
        # Run the command
        subprocess.run(command, check=True)
        print("Download completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
# Download an Instagram post without cookies
path = 'C:\\Users\\Suraj\\Desktop\\down_videos'
download_instagram_post('https://www.instagram.com/reel/C-2g04UIVbD/',path)


# Download an Instagram post with cookies
# download_instagram_post('https://www.instagram.com/p/POST_SHORTCODE/', cookies_path='/path/to/cookies.txt')
