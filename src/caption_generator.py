"""
Instagram Caption and Hashtag Generator:
Formats song quotes, artist credits, and auto-generates clean hashtags.
"""

import re


def clean_hashtag(text: str) -> str:
    """Removes special characters to produce a clean camelCase hashtag."""
    clean = re.sub(r"[^\w\s]", "", text)
    words = clean.split()
    return "#" + "".join([w.capitalize() for w in words])


def generate_caption(song_title: str, artist_name: str, lyrics: str) -> str:
    """Creates an aesthetic Instagram caption ready to paste/post."""
    # Build song and artist hashtags
    song_tag = clean_hashtag(song_title)
    
    # Split multiple artists (comma or '&' separated)
    artists = re.split(r"[,&]", artist_name)
    artist_tags = " ".join([clean_hashtag(a.strip()) for a in artists if a.strip()])

    generic_tags = (
        "#SpotifyLyrics #HindiSongs #IndieIndia #AestheticQuotes "
        "#SongLyrics #IndianMusic #BollyAesthetic #MusicLovers #DailyLyrics"
    )

    caption = f"""✨ {lyrics.strip()}

🎵 Song: {song_title}
🎙️ Artist: {artist_name}

Follow for daily aesthetic lyrics.
Save & share with someone who loves this song ❤️

.
.
{song_tag} {artist_tags} {generic_tags}
"""
    return caption.strip()