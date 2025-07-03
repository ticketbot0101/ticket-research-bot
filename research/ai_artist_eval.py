import json, os
import requests

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_deepseek_about_artist(artist):
    prompt = f"""
Act like a concert ticket investor.
Rate this artist's current hype from 0 to 10.
Also say whether you'd expect resale tickets to be profitable in a big US city.

Artist: {artist}

Respond JSON like:
{{
  "artist": "NAME",
  "score": 0-10,
  "verdict": "Profitable" or "Not Profitable",
  "reason": "short explanation"
}}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "HTTP-Referer": "https://github.com/YOUR_GITHUB_USERNAME",  # Optional
            "X-Title": "Ticket-Arb-Evaluator",
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a ticket flipping analyst."},
                {"role": "user", "content": prompt}
            ]
        },
        timeout=30
    )

    return response.json()["choices"][0]["message"]["content"]

def run_evaluation():
    with open("data/events.json", "r") as f:
        events = json.load(f)

    results = []
    for event in events:
        artist = event.get("artist")
        if not artist: continue
        print(f"🔍 Evaluating: {artist}")
        try:
            analysis = ask_deepseek_about_artist(artist)
            print(analysis)
            result = json.loads(analysis)
            event.update(result)
            results.append(event)
        except Exception as e:
            print(f"⚠️ Error evaluating {artist}: {e}")

    with open("data/artist_eval.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_evaluation()
