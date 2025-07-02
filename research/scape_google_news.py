import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import os

# Keywords to look for in news articles
KEYWORDS = ["tour", "concert", "presale", "on sale", "ticketmaster", "axs"]

# Cities to monitor (expand as needed)
TARGET_CITIES = ["New York", "Los Angeles", "Chicago", "Atlanta", "Las Vegas"]

# Number of Google search results pages to scrape
MAX_PAGES = 2

# Date range filter (e.g. past 1 day)
RECENT_DATE = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def fetch_news_results(query):
    results = []
    for page in range(MAX_PAGES):
        start = page * 10
        url = f"https://www.google.com/search?q={query}+site:billboard.com+OR+site:variety.com+OR+site:rollingstone.com&tbm=nws&start={start}&tbs=qdr:d"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".dbsr")

        for article in articles:
            title = article.select_one(".nDgy9d").text if article.select_one(".nDgy9d") else ""
            link = article.a['href'] if article.a else ""
            snippet = article.select_one(".Y3v8qd").text if article.select_one(".Y3v8qd") else ""
            if any(k.lower() in title.lower() + snippet.lower() for k in KEYWORDS):
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet
                })
    return results


def extract_events_from_news():
    events = []
    for city in TARGET_CITIES:
        news_hits = fetch_news_results(f"concert {city}")
        for hit in news_hits:
            events.append({
                "city": city,
                "title": hit["title"],
                "url": hit["url"],
                "snippet": hit["snippet"],
                "source": "google_news",
                "fetched_at": datetime.utcnow().isoformat()
            })
    return events


def save_events(events, path="data/events.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(events, f, indent=2)


if __name__ == "__main__":
    print("🔍 Gathering fresh concert news...")
    all_events = extract_events_from_news()
    save_events(all_events)
    print(f"✅ Saved {len(all_events)} events to data/events.json")

