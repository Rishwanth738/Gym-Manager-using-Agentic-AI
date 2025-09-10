import os
import requests
from crewai.tools import tool



# Make sure you set: export SERPER_API_KEY="your_api_key"
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool("YouTubeSearchTool")
def youtube_search_tool(query: str) -> str:
    """
    Search YouTube for exercise or recipe videos using Serper API.
    Returns top 2-3 video links.
    """
    if not SERPER_API_KEY:
        return "Error: SERPER_API_KEY not set in environment."

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": f"site:youtube.com {query}"}

    try:
        resp = requests.post(url, headers=headers, json=payload)
        results = resp.json()
        links = [item["link"] for item in results.get("organic", [])[:3]]
        if not links:
            return "No YouTube results found."
        return "\n".join(links)
    except Exception as e:
        return f"Error during YouTube search: {e}"
