import instaloader

def get_instagram_profile_info(profile_name):
    # Create an instance of Instaloader class
    L = instaloader.Instaloader()

    try:
        # Load the profile
        profile = instaloader.Profile.from_username(L.context, profile_name)
        
        # Get the profile name
        full_name = profile.full_name
        
        # Initialize an empty list to hold post URLs
        post_urls = []

        # Loop through all posts in the profile and append their URLs to the list
        for post in profile.get_posts():
            post_url = f"https://www.instagram.com/p/{post.shortcode}/"
            post_urls.append(post_url)

        return full_name, post_urls
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example usage
profile_name = 'akanksshha_'  # Replace with the Instagram username
profile_full_name, post_urls = get_instagram_profile_info(profile_name)

if profile_full_name and post_urls:
    print(f"Profile Name: {profile_full_name}")
    print(f"Number of Posts: {len(post_urls)}")
    for url in post_urls:
        print(url)
else:
    print("Failed to retrieve profile information.")
