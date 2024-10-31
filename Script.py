import requests
from bs4 import BeautifulSoup
import re

def scrape_videos(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <video> tags and their sources
        video_urls = []
        
        # Collect <video> sources
        for video_tag in soup.find_all('video'):
            src = video_tag.get('src')
            if src:
                video_urls.append(src)
            else:
                # Collect sources from <source> tags inside <video>
                for source_tag in video_tag.find_all('source'):
                    src = source_tag.get('src')
                    if src:
                        video_urls.append(src)

        # Find videos embedded with direct <source> tags outside <video>
        for source_tag in soup.find_all('source'):
            src = source_tag.get('src')
            if src and src not in video_urls:
                video_urls.append(src)

        # Displaying the scraped video URLs
        if video_urls:
            print("Found video URLs:")
            for i, video_url in enumerate(video_urls, start=1):
                print(f"{i}. {video_url}")
        else:
            print("No video URLs found on this page.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

# Input URL from the user
url = input("Enter the URL to scrape videos from: ")
scrape_videos(url)
