#activity-report.py
# Last updated: 2026-07-06
# Description: Creates a json file out of all the data for assets including the date of adjustments.
# Usage: python3 activity-report.py
#

import requests
import json
import os
from pathlib import Path
from datetime import datetime

## Standard Configuration ---
URL = "https://snipeit.camio.acep.uaf.edu"
snipeit_api_token = Path('prod.cred').read_text().strip()

header = {
  "Authorization": f"Bearer {snipeit_api_token}",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
## End Standard Configuration ---

#log the date in activity reports
current_date = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = f"snipeit_activity_report_{current_date}.json"
PAGE_SIZE = 500  

endpoint = f"{URL}/api/v1/reports/activity"
all_activities = []
offset = 0

print("Downloading Snipe-IT Activity logs...")

while True:
    query_params = {
        "limit": PAGE_SIZE,
        "offset": offset,
        "order": "desc",
        "sort": "created_at",
    }

    response = requests.get(endpoint, headers=header, params=query_params).json()

    #if there's no more data: 
    rows = response.get("rows", [])
    if not rows:
        break  

    all_activities.extend(rows)
    offset += PAGE_SIZE  

# Save raw output to json file format
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_activities, f, indent=4, ensure_ascii=False)

print(f"{len(all_activities)} items saved to '{OUTPUT_FILE}'.")