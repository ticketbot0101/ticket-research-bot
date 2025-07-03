# File: ticket_flipper_ui.py
# Purpose: Streamlit UI for monitoring artist demand and resale potential

import streamlit as st
import pandas as pd
import json
import os

from get_billboard_top_artists import get_billboard_artists
from ask_deepseek import evaluate_artist_with_deepseek

st.set_page_config(page_title="Ticket Flipper AI Dashboard", layout="wide")
st.title("🎟️ Ticket Flipper AI Dashboard")

st.markdown("""
This dashboard auto-evaluates trending artists from Billboard using DeepSeek via OpenRouter,
and helps you decide which artists are 🔥 hot for ticket flips.
""")

# Option to fetch new Billboard list
if st.button("🔄 Refresh Billboard Artist List"):
    with st.spinner("Fetching Billboard artists..."):
        artists = get_billboard_artists()
        with open("billboard_artists.json", "w") as f:
            json.dump(artists, f)
else:
    if os.path.exists("billboard_artists.json"):
        with open("billboard_artists.json", "r") as f:
            artists = json.load(f)
    else:
        st.warning("Click refresh to load Billboard artists.")
        st.stop()

# Evaluate with DeepSeek
results = []
if st.button("🤖 Run DeepSeek Evaluations"):
    with st.spinner("Evaluating artists..."):
        for artist in artists:
            res = evaluate_artist_with_deepseek(artist)
            results.append(res)
        df = pd.DataFrame(results)
        df.to_csv("deepseek_artist_scores.csv", index=False)
else:
    if os.path.exists("deepseek_artist_scores.csv"):
        df = pd.read_csv("deepseek_artist_scores.csv")
    else:
        st.info("Click 'Run DeepSeek Evaluations' to analyze artist demand.")
        st.stop()

# UI Table
st.markdown("### 🧠 Artist Demand Analysis")
emoji_map = {"Great buy": "✅", "Medium risk": "🟡", "Avoid": "❌"}
df["rating"] = df["label"].map(emoji_map)
st.dataframe(df[["artist", "label", "rating", "verdict"]].sort_values("label"), use_container_width=True)

# Filter for hot buys
hot_df = df[df["label"] == "Great buy"]
st.markdown("### 🚀 Top Picks to Flip")
st.table(hot_df[["artist", "verdict"]])
