# 🎵 Spotify Lyric Card Generator for Instagram

An automated Instagram post generator that creates aesthetic **Spotify Lyric Share Cards (1080x1350 4:5 portrait)** with verified Devanagari lyrics, official Apple Music album artwork, and curated 4K photography.

Orchestrated through **Google Sheets**, the engine reads your favorite song lyrics, generates mood-matched aesthetic backgrounds, renders clean frosted-glass Spotify cards (without clunky scrubber bars), and formats ready-to-post captions with song-specific hashtags.

---

## ✨ Key Features

- **HarfBuzz / Chromium Devanagari Engine:** Uses Playwright to render complex Indian language scripts (matras, half-letters, and ligatures) with 100% typographic precision (no broken conjuncts or missing tofu boxes).
- **Official Music Metadata:** Automatically pulls official song titles, artist names, and 4K album art using the Apple Music / iTunes API.
- **Minimal Spotify Design:** Modeled after Spotify's official "Share Lyrics" widget (frosted glassmorphism, rounded album art, verified typography, and native Spotify logo).
- **Dynamic 4K Backgrounds:** Fetches high-resolution aesthetic photography (monsoon rain, vintage 35mm film, golden hour, city bokeh).
- **Auto-Generated Captions & Hashtags:** Generates Instagram captions with lyrics quotes, song credits, and dynamic camelCase artist/track hashtags (`#Iktara #AmitTrivedi #KavitaSeth`).
- **Google Sheets Orchestration:** Reads pending tracks directly from the `Spotify_Lyrics` tab in your master Google Sheet and marks them completed upon generation.

---

## 🛠️ Tech Stack

- **Renderer:** Python + Playwright (Headless Chromium)
- **Metadata API:** Apple Music / iTunes Search API
- **Photography:** Curated Unsplash CDN
- **Orchestration:** `gspread` (Google Sheets API)
- **Typography:** Google Fonts (*Noto Serif Devanagari*, *Inter*)

---

## 🚀 Setup & Local Execution

### 1. Clone & Setup Environment
```bash
git clone https://github.com/Pankaj0606/Spotify-Lyric-Posts.git
cd Spotify-Lyric-Posts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium