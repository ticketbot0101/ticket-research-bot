# File: google_sheets_sync.py
# Purpose: Sync DeepSeek evaluations to Google Sheets

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Define scope and load credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Replace with your own credentials file name (downloaded from Google Cloud)
CREDS_FILE = "google-credentials.json"

# Your target spreadsheet name
SPREADSHEET_NAME = "Ticket Flipper Artist Evaluations"

# Connect to Google Sheets
def connect_to_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(SPREADSHEET_NAME).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = client.create(SPREADSHEET_NAME).sheet1
        sheet.append_row(["Timestamp", "Artist", "Verdict", "Label"])
    return sheet

# Sync results to sheet
def sync_evaluations(evaluations):
    sheet = connect_to_sheet()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for entry in evaluations:
        sheet.append_row([
            now,
            entry.get("artist", ""),
            entry.get("verdict", ""),
            entry.get("label", "")
        ])

# Example usage
if __name__ == "__main__":
    mock_data = [
        {"artist": "Sabrina Carpenter", "verdict": "Major rise in fanbase and relevance.", "label": "Great buy"},
        {"artist": "The Chainsmokers", "verdict": "Past peak relevance.", "label": "Avoid"},
    ]
    sync_evaluations(mock_data)
