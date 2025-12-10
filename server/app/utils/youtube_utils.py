"""YouTube video utilities"""
import re
import requests
from typing import Dict, Any
from app.core.config import YOUTUBE_API_KEY


def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'([a-zA-Z0-9_-]{11})'  # Direct video ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL")


def fetch_youtube_metadata(video_id: str) -> Dict[str, Any]:
    """Fetch YouTube video metadata using YouTube Data API or scraping"""
    metadata = {
        "title": "Unknown Title",
        "description": "",
        "channel_name": "Unknown Channel",
        "tags": [],
        "category": "",
        "view_count": 0,
        "like_count": 0
    }
    
    # Try YouTube Data API if key is available
    if YOUTUBE_API_KEY:
        try:
            from googleapiclient.discovery import build
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            request = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if response.get('items'):
                item = response['items'][0]
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})
                
                metadata.update({
                    "title": snippet.get('title', 'Unknown Title'),
                    "description": snippet.get('description', ''),
                    "channel_name": snippet.get('channelTitle', 'Unknown Channel'),
                    "publish_date": snippet.get('publishedAt', '')[:10],  # Extract date YYYY-MM-DD
                    "tags": snippet.get('tags', []),
                    "category": snippet.get('categoryId', ''),
                    "view_count": int(statistics.get('viewCount', 0)),
                    "like_count": int(statistics.get('likeCount', 0))
                })
                return metadata
        except Exception as e:
            print(f"YouTube API error: {e}")
    
    # Fallback: scrape basic info from YouTube page
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Extract title from page
            title_match = re.search(r'"title":"([^"]+)"', response.text)
            if title_match:
                metadata["title"] = title_match.group(1).encode().decode('unicode_escape')
            
            # Extract channel name
            channel_match = re.search(r'"author":"([^"]+)"', response.text)
            if channel_match:
                metadata["channel_name"] = channel_match.group(1).encode().decode('unicode_escape')
            
            # Extract description
            desc_match = re.search(r'"shortDescription":"([^"]+)"', response.text)
            if desc_match:
                metadata["description"] = desc_match.group(1).encode().decode('unicode_escape')[:500]
                
            # Extract publish date
            date_match = re.search(r'"publishDate":"([^"]+)"', response.text)
            if date_match:
                metadata["publish_date"] = date_match.group(1)
    except Exception as e:
        print(f"Scraping error: {e}")
    
    return metadata


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"
