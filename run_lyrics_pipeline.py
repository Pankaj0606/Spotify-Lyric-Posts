"""
Master Execution Pipeline:
1. Reads pending songs from 'DSA_Instagram_Automation' (Tab: 'Spotify_Lyrics').
2. Uses exact user lyrics from Google Sheets (zero LLM hallucination).
3. Fetches official album art & 4K photography.
4. Renders minimal Spotify lyric card (no timer/scrubber).
5. Generates caption + song-specific hashtags.
6. Marks row as Completed in Google Sheets.
"""

import os
import sys
import time
import re
import gspread
from src.music_metadata import fetch_song_details
from src.image_fetcher import fetch_aesthetic_background
from src.card_generator import create_spotify_lyric_post
from src.caption_generator import generate_caption


def connect_sheet():
    """Connects to Google Sheet with credential fallback."""
    cred_paths = ["credentials.json", "config/credentials.json", "../Daily-Tech-Bytes/credentials.json"]
    cred_file = next((p for p in cred_paths if os.path.exists(p)), None)
    
    if not cred_file:
        sys.exit("✗ credentials.json not found! Please place credentials.json in project root.")

    for attempt in range(1, 4):
        try:
            gc = gspread.service_account(filename=cred_file)
            sh = gc.open("DSA_Instagram_Automation")
            return sh.worksheet("Spotify_Lyrics")
        except Exception as e:
            print(f"⚠ Attempt {attempt}/3 connecting to Google Sheets failed: {e}")
            time.sleep(3)
    sys.exit("✗ Could not connect to 'Spotify_Lyrics' tab in Google Sheet.")


def slugify(text: str) -> str:
    return re.sub(r'[\s_]+', '_', re.sub(r'[^\w\s]', '', text)).strip().lower()


def main():
    print("📡 Connecting to Google Sheet: DSA_Instagram_Automation -> 'Spotify_Lyrics'...")
    ws = connect_sheet()
    records = ws.get_all_records()
    headers = ws.row_values(1)

    if "Status" not in headers:
        sys.exit("✗ 'Status' column not found in Google Sheet. Please add it.")
    status_col_idx = headers.index("Status") + 1

    pending_rows = [(idx + 2, r) for idx, r in enumerate(records) if str(r.get("Status", "")).strip().lower() == "pending"]
    if not pending_rows:
        print("✓ All lyrics posts are completed! Add more pending songs in Google Sheets.")
        return

    row_num, row_data = pending_rows[0]
    song_name = str(row_data.get("Song Name", "")).strip()
    artist_name = str(row_data.get("Artist Name", "")).strip()
    lyrics = str(row_data.get("Lyrics (Devanagari)", "")).strip()
    mood = str(row_data.get("Mood / Theme", "")).strip() or "monsoon rain car window bokeh"

    print(f"\n🎯 Found Pending Song: '{song_name}' by '{artist_name}'")
    print(f"📝 Lyrics:\n{lyrics}")

    # 1. Official Metadata & Album Artwork
    print("\n🎵 Querying Apple Music metadata...")
    meta = fetch_song_details(song_name, artist_name)
    title = meta["title"]
    artist = meta["artist"]
    album_art = meta["album_art_url"]

    # 2. 4K Aesthetic Photography
    slug = f"{slugify(title)}_{slugify(artist)[:10]}"
    bg_path = f"output/{slug}_bg.jpg"
    final_post_path = f"output/{slug}_post.jpg"
    caption_path = f"output/{slug}_caption.txt"

    print(f"📸 Fetching 4K aesthetic background matching mood: '{mood}'...")
    fetch_aesthetic_background(mood, bg_path)

    # 3. Render Sleek Spotify Lyric Post
    print("🎨 Rendering minimal Spotify Lyric Card (1080x1350)...")
    create_spotify_lyric_post(
        bg_image_path=bg_path,
        song_title=title,
        artist_name=artist,
        album_art_url=album_art,
        devanagari_lyrics=lyrics,
        output_path=final_post_path
    )

    # 4. Generate Caption & Hashtags
    caption = generate_caption(title, artist, lyrics)
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption)

    # 5. Mark Row as Completed
    ws.update_cell(row_num, status_col_idx, "Completed")
    print(f"✓ Google Sheet row {row_num} marked as 'Completed'!")

    print("\n" + "="*70)
    print("🎉 INSTAGRAM POST & CAPTION READY!")
    print(f"   Image File  : {final_post_path}")
    print(f"   Caption File: {caption_path}")
    print("="*70)
    print("\n📋 GENERATED CAPTION PREVIEW:\n")
    print(caption)
    print("="*70)
    print(f"\nLaunch preview with: open {final_post_path}")


if __name__ == "__main__":
    main()