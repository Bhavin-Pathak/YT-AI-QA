"""Web search and scraping utilities"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from duckduckgo_search import DDGS
from app.core.config import WEB_SEARCH_RESULTS, MAX_WEBPAGE_CONTENT


def search_web(query: str, num_results: int = WEB_SEARCH_RESULTS) -> List[Dict[str, str]]:
    """Search the web using DuckDuckGo and return results"""
    try:
        ddgs = DDGS()
        results = []
        
        search_results = ddgs.text(query, max_results=num_results)
        
        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "body": result.get("body", ""),
                "url": result.get("href", "")
            })
        
        return results
    except Exception as e:
        print(f"Web search error: {e}")
        return []


def fetch_webpage_content(url: str) -> str:
    """Fetch and extract text content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:MAX_WEBPAGE_CONTENT]
        
        return ""
    except Exception as e:
        print(f"Webpage fetch error: {e}")
        return ""
