import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
import re

# Constants
SEARCH_TERMS = [
    "concert announced",
    "tour announced",
    "on tour",
    "live in concert",
    "2025 tour",
]
EXCLUDE_TERMS = ["paw patrol", "disney on ice", "monster jam", "nfl", "nba", "wwe"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TicketBot/1.0; +https://github.com/yourrepo)"
}
RESULT_LIMIT = 25
OUTPUT_FILE = "data/events.json"

def clean_snippet(text):
    # Normalize and remove formatting junk
    return re.sub(r"\s+", " ", text).strip()

def looks_like_concert_announcement(snippet):
    text = snippet.lower()
    if any(ex in text for ex in EXCLUDE_TERMS):
        return False
    return True

def extract_artist_and_location(snippet):
    # Try naive name + city extract
    m = re.search(r"([A-Z][a-zA-Z\s&]+)\s+(?:announces?|reveals?|brings?)\s+.*\s+to\s+([A-Z][a-zA-Z\s]+)", snippet)
    if m:
        artist = m.group(1).strip()
        city = m.group(2).strip()
        return artist, city
    return None, None

def fetch_concert_news():
    results = []
    now = datetime.utcnow()
    from_time = (now - timedelta(days=1)).strftime('%Y-%m-%d')

    for term in SEARCH_TERMS:
        print(f"🔍 Searching Google News for: {term}")
        search_url = (
            f"https://news.google.com/search?q={term.replace(' ', '%20')}%20after:{from_time}&hl=en-US&gl=US&ceid=US:en"
        )
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article")

        for article in articles[:RESULT_LIMIT]:
            title_tag = article.select_one("h3") or article.select_one("h4")
            snippet_tag = article.select_one("span")
            link_tag = article.select_one("a")

            if not title_tag or not link_tag:
                continue

            snippet = snippet_tag.text if snippet_tag else title_tag.text
            if not looks_like_concert_announcement(snippet):
                continue

            artist, city = extract_artist_and_location(snippet)
            url = "https://news.google.com" + link_tag["href"][1:]

            results.append({
                "artist": artist or title_tag.text,
                "city": city or "unknown",
                "headline": clean_snippet(title_tag.text),
                "snippet": clean_snippet(snippet),
                "url": url,
                "scraped_at": now.strftime("%Y-%m-%d %H:%M:%S")
            })

    return results

def save_results(events):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(events, f, indent=2)
    print(f"✅ Saved {len(events)} events to {OUTPUT_FILE}")

if __name__ == "__main__":
    events = fetch_concert_news()
    save_results(events)
