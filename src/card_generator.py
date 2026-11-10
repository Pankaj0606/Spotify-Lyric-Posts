"""
Minimal Spotify Lyric Card Generator via Playwright.
Modeled after Spotify's official 'Share Lyrics' widget:
- No clunky scrubber bars
- Sleek frosted glassmorphism (backdrop blur)
- Official album art & verified Devanagari typography
- Native Spotify logo badge
"""

import os
from playwright.sync_api import sync_playwright


def create_spotify_lyric_post(
    bg_image_path: str,
    song_title: str,
    artist_name: str,
    album_art_url: str,
    devanagari_lyrics: str,
    output_path: str
):
    abs_bg_path = os.path.abspath(bg_image_path)
    abs_output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output_path), exist_ok=True)

    # Convert multiline lyrics to clean HTML line breaks
    formatted_lyrics = "<br>".join([
        line.strip() for line in devanagari_lyrics.replace("\\n", "\n").split("\n") if line.strip()
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
      <meta charset="UTF-8">
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

        * {{
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }}

        body {{
          width: 1080px;
          height: 1350px;
          overflow: hidden;
          position: relative;
          background: #000;
          font-family: 'Inter', sans-serif;
        }}

        /* Full 4:5 Aesthetic Photography Background */
        .background-image {{
          position: absolute;
          top: 0;
          left: 0;
          width: 1080px;
          height: 1350px;
          object-fit: cover;
          z-index: 1;
        }}

        /* Subtle Bottom Vignette for seamless card floating */
        .vignette {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.45) 70%, rgba(0,0,0,0.85) 100%);
          z-index: 2;
        }}

        /* Minimal Spotify Lyrics Card (Official Share Style) */
        .card-container {{
          position: absolute;
          bottom: 110px;
          left: 50%;
          transform: translateX(-50%);
          width: 880px;
          background: rgba(18, 18, 22, 0.74);
          backdrop-filter: blur(35px);
          -webkit-backdrop-filter: blur(35px);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 28px;
          padding: 36px 42px;
          box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
          z-index: 3;
          display: flex;
          flex-direction: column;
          gap: 28px;
        }}

        /* Header Row: Album Art + Song & Artist + Spotify Mark */
        .card-header {{
          display: flex;
          align-items: center;
          justify-content: space-between;
        }}

        .song-identity {{
          display: flex;
          align-items: center;
          gap: 20px;
        }}

        .album-art {{
          width: 82px;
          height: 82px;
          border-radius: 14px;
          object-fit: cover;
          box-shadow: 0 6px 16px rgba(0,0,0,0.35);
        }}

        .track-meta {{
          display: flex;
          flex-direction: column;
          gap: 4px;
        }}

        .track-title {{
          color: #ffffff;
          font-size: 27px;
          font-weight: 700;
          letter-spacing: -0.2px;
        }}

        .track-artist {{
          color: rgba(255, 255, 255, 0.62);
          font-size: 19px;
          font-weight: 500;
        }}

        .spotify-badge {{
          display: flex;
          align-items: center;
          gap: 8px;
        }}

        .spotify-logo {{
          width: 34px;
          height: 34px;
        }}

        /* Central Lyrics Display */
        .lyrics-section {{
          padding: 6px 4px 10px 4px;
          text-align: left;
        }}

        .lyrics-text {{
          font-family: 'Noto Serif Devanagari', serif;
          font-size: 38px;
          font-weight: 700;
          line-height: 1.55;
          color: #ffffff;
          letter-spacing: 0.3px;
          text-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
        }}
      </style>
    </head>
    <body>
      <img class="background-image" src="file://{abs_bg_path}" alt="Background">
      <div class="vignette"></div>

      <div class="card-container">
        <!-- Header -->
        <div class="card-header">
          <div class="song-identity">
            <img class="album-art" src="{album_art_url}" alt="Album Art">
            <div class="track-meta">
              <div class="track-title">{song_title}</div>
              <div class="track-artist">{artist_name}</div>
            </div>
          </div>
          <!-- Spotify Green Icon -->
          <div class="spotify-badge">
            <svg class="spotify-logo" viewBox="0 0 168 168">
              <path fill="#1ED760" d="M83.996.002C37.607.002 0 37.608 0 84c0 46.395 37.607 83.999 83.996 83.999 46.402 0 84.004-37.604 84.004-84 0-46.392-37.602-83.998-84.004-83.998zm38.483 121.144c-1.531 2.506-4.795 3.308-7.301 1.777-20.027-12.238-45.236-15.004-74.927-8.216-2.868.655-5.719-1.147-6.374-4.015-.655-2.868 1.147-5.719 4.015-6.374 32.504-7.424 60.364-4.254 82.81 9.527 2.506 1.531 3.308 4.795 1.777 7.301zm10.274-22.843c-1.924 3.13-6.027 4.133-9.157 2.209-22.923-14.09-57.874-18.176-84.992-9.945-3.522 1.069-7.25-.936-8.319-4.458-1.069-3.522.936-7.25 4.458-8.319 30.985-9.404 69.431-4.881 95.799 11.356 3.132 1.924 4.135 6.027 2.211 9.157zm.882-23.724C106.19 60.59 60.852 59.102 34.613 67.065c-4.149 1.258-8.544-1.106-9.802-5.255-1.258-4.149 1.106-8.544 5.255-9.802 30.134-9.145 80.203-7.447 111.966 11.408 3.731 2.216 4.949 7.028 2.733 10.759-2.216 3.731-7.028 4.949-10.759 2.733z"/>
            </svg>
          </div>
        </div>

        <!-- Lyrics -->
        <div class="lyrics-section">
          <div class="lyrics-text">{formatted_lyrics}</div>
        </div>
      </div>
    </body>
    </html>
    """

    temp_html_path = abs_output_path.replace(".jpg", ".html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto(f"file://{temp_html_path}", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=abs_output_path, quality=95, type="jpeg")
        browser.close()

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    return output_path