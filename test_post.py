"""
Test Runner:
Generates 1 complete aesthetic Instagram Spotify lyric post.
"""

from src.music_metadata import fetch_song_details
from src.image_fetcher import fetch_aesthetic_background
from src.card_generator import create_spotify_lyric_post

# Real Iktara Song Details
SONG = "Iktara"
ARTIST = "Amit Trivedi"
MOOD = "monsoon rain car window bokeh"

# Authentic Lyrics with matras (ह्रस्व 'ि' and दीर्घ 'ी' verified)
LYRICS = "गूंजा सा कोई इकतारा, इकतारा\nदिल संभलता नहीं, क्या कीजिए"

OUTPUT_BG = "output/aesthetic_bg.jpg"
OUTPUT_POST = "output/iktara_spotify_post.jpg"


def main():
    print(f"🎵 Querying Apple Music metadata for '{SONG}'...")
    meta = fetch_song_details(SONG, ARTIST)
    print(f"  ├── Track: {meta['title']}")
    print(f"  ├── Artist: {meta['artist']}")
    print(f"  └── Album Art URL: {meta['album_art_url']}")

    print("\n📸 Fetching 4K aesthetic photography...")
    fetch_aesthetic_background(MOOD, OUTPUT_BG)
    print(f"  └── Saved background to: {OUTPUT_BG}")

    print("\n🎨 Compositing floating Spotify lyric card (1080x1350)...")
    create_spotify_lyric_post(
        bg_image_path=OUTPUT_BG,
        song_title=meta["title"],
        artist_name=meta["artist"],
        album_art_url=meta["album_art_url"],
        devanagari_lyrics=LYRICS,
        output_path=OUTPUT_POST,
        current_time="01:42",
        total_time="04:13",
        progress_pct=0.40
    )

    print("\n" + "="*60)
    print(f"🎉 POST CREATED SUCCESSFULLY!")
    print(f"   Image saved to: {OUTPUT_POST}")
    print(f"   Launch preview with: open {OUTPUT_POST}")
    print("="*60)


if __name__ == "__main__":
    main()