# File: ask_deepseek.py
# Purpose: Query OpenRouter's DeepSeek LLM to evaluate artist demand

import requests
import json
import os

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
  "label": "Great buy|Medium risk|Avoid"
}
"""


def evaluate_artist_with_deepseek(artist):
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
        return json.loads(message)
    except Exception as e:
        print(f"❌ Failed to evaluate {artist}: {e}")
        return {"artist": artist, "verdict": "Unknown", "label": "Medium risk"}


if __name__ == "__main__":
    # Test mode
    print(evaluate_artist_with_deepseek("Sabrina Carpenter"))
