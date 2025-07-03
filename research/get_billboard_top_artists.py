
# File: get_billboard_top_artists.py
# Purpose: Scrape top Billboard artists for artist trend validation

import requests
from bs4 import BeautifulSoup

BILLBOARD_URL = "https://www.billboard.com/charts/artist-100/"

def get_billboard_top_artists():
    try:
        response = requests.get(BILLBOARD_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.select("li.o-chart-results-list__item h3")

        artists = []
        for entry in entries:
            artist = entry.get_text(strip=True)
            if artist:
                artists.append(artist)

        return artists

    except Exception as e:
        print(f"❌ Error fetching Billboard data: {e}")
        return []

if __name__ == "__main__":
    top_artists = get_billboard_top_artists()
    print(f"🎵 Top Billboard Artists: ({len(top_artists)} found)")
    for artist in top_artists:
        print("-", artist)
