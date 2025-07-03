# File: main.py
# Purpose: End-to-end pipeline to gather and evaluate concert opportunities

import json
import os
from scrape_google_news import scrape_recent_concert_announcements
from ask_deepseek import evaluate_artist_with_deepseek

EVENTS_FILE = "data/events.json"
RESULTS_FILE = "data/evaluated_events.json"

os.makedirs("data", exist_ok=True)

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def enrich_events_with_ai(events):
    enriched = []
    for event in events:
        artist = event.get("artist")
        print(f"🎤 Evaluating: {artist}")
        eval_data = evaluate_artist_with_deepseek(artist)
        enriched.append({**event, **eval_data})
    return enriched

def run():
    print("🔍 Scraping Google News for fresh concerts...")
    fresh_events = scrape_recent_concert_announcements()
    print(f"🎯 Found {len(fresh_events)} new events.")

    save_json(EVENTS_FILE, fresh_events)

    print("🤖 Evaluating artist demand using DeepSeek...")
    enriched_events = enrich_events_with_ai(fresh_events)

    save_json(RESULTS_FILE, enriched_events)
    print(f"✅ Evaluation complete. Saved to {RESULTS_FILE}")

if __name__ == "__main__":
    run()
