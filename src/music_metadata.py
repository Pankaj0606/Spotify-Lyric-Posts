"""
Fetches official song metadata and high-resolution album art
using the free Apple Music / iTunes Search API.
"""

import requests
from typing import Dict, Optional


def fetch_song_details(song_name: str, artist: str = "") -> Dict:
    """Queries iTunes API for official song metadata and album artwork."""
    query = f"{song_name} {artist}".strip()
    url = f"https://itunes.apple.com/search?term={requests.utils.quote(query)}&media=music&limit=1"

    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ConnectionError(f"Could not reach iTunes API: Status {response.status_code}")

    results = response.json().get("results", [])
    if not results:
        # Fallback if no exact match found
        return {
            "title": song_name,
            "artist": artist or "Unknown Artist",
            "album_art_url": None
        }

    track = results[0]
    # iTunes provides artwork at 100x100, replace with 600x600 for crisp 4K rendering
    raw_art_url = track.get("artworkUrl100", "")
    hi_res_art_url = raw_art_url.replace("100x100bb", "600x600bb") if raw_art_url else None

    return {
        "title": track.get("trackName", song_name),
        "artist": track.get("artistName", artist),
        "album_art_url": hi_res_art_url
    }