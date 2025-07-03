# File: ask_deepseek.py
# Purpose: Query OpenRouter's DeepSeek LLM to evaluate artist demand and enhance with Billboard trend filtering

import requests
import json
import os
from get_billboard_top_artists import get_billboard_top_artists

# Environment variable OPENROUTER_API_KEY must be set
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek-chat"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPT_TEMPLATE = """
You're an expert in music industry trends. Based on current data, evaluate whether the following artist is:
1. Blowing up (✅ Great buy),
2. Stable demand (🟡 Medium risk), or
3. Fading (❌ Avoid).
Use recent Billboard performance, streaming stats, social relevance, and expected tour hype.
Return a 1-sentence verdict and a label: (Great buy / Medium risk / Avoid).

Artist: {artist}

Respond in JSON format:
{
  "artist": "{artist}",
  "verdict": "",
  "label": "Great buy|Medium risk|Avoid",
  "billboard_top_100": true|false
}
"""

def evaluate_artist_with_deepseek(artist, billboard_artists=None):
    billboard_match = artist.lower() in (a.lower() for a in billboard_artists) if billboard_artists else False
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a music industry analyst bot."},
            {"role": "user", "content": PROMPT_TEMPLATE.format(artist=artist)}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=payload)
        res.raise_for_status()
        parsed = res.json()
        message = parsed["choices"][0]["message"]["content"]
        output = json.loads(message)
        output["billboard_top_100"] = billboard_match
        return output
    except Exception as e:
        print(f"❌ Failed to evaluate {artist}: {e}")
        return {"artist": artist, "verdict": "Unknown", "label": "Medium risk", "billboard_top_100": billboard_match}


if __name__ == "__main__":
    billboard_top = get_billboard_top_artists()
    print(evaluate_artist_with_deepseek("Sabrina Carpenter", billboard_top))
