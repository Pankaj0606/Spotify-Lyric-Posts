"""
Fetches high-resolution aesthetic photography for Instagram posts.
Uses curated Unsplash CDN endpoints matching aesthetic photography themes.
"""

import requests
import urllib.parse
from PIL import Image
import io


def fetch_aesthetic_background(theme: str, output_path: str, width: int = 1080, height: int = 1350) -> str:
    """
    Fetches a 1080x1350 portrait aesthetic photo based on the theme.
    Example themes: 'monsoon rain car window bokeh', 'vintage golden hour 35mm', 'retro night drive'
    """
    clean_theme = urllib.parse.quote(theme)
    # Using Unsplash direct curated high-res source
    url = f"https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w={width}&h={height}&q=85"
    
    # Theme-based fallbacks for aesthetic photography
    theme_lower = theme.lower()
    if "rain" in theme_lower or "monsoon" in theme_lower:
        url = f"https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w={width}&h={height}&q=85"
    elif "sunset" in theme_lower or "golden" in theme_lower:
        url = f"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w={width}&h={height}&q=85"
    elif "night" in theme_lower or "city" in theme_lower or "drive" in theme_lower:
        url = f"https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w={width}&h={height}&q=85"
    elif "cozy" in theme_lower or "room" in theme_lower or "coffee" in theme_lower:
        url = f"https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w={width}&h={height}&q=85"

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch background photo: Status {response.status_code}")

    # Center crop and fit exactly to 1080x1350
    img = Image.open(io.BytesIO(response.content)).convert("RGB")
    img_ratio = img.width / img.height
    target_ratio = width / height

    if img_ratio > target_ratio:
        new_width = int(target_ratio * img.height)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))

    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    final_img.save(output_path, quality=95)
    return output_path