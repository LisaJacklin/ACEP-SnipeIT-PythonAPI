# Name: manufacture-manage.py
# Last Updated: 2026-01-22
#
# Description: a single script to manage manufacturers in Snipe-IT via API.
#   This includes addingmanufacturers.
# Usage:
#

import requests
import json
import os
from pathlib import Path

## load ManufacturerManager from manufacturers.py
from manufacturers import ManufacturerManager

## Standard Configuration ---
#url adjusted here for manufacturers
URL = "https://snipeit.camio.acep.uaf.edu/api/v1"
snipeit_api_token = Path('prod.cred').read_text().strip()

header = {
  "Authorization": f"Bearer {snipeit_api_token}",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
## End Standard Configuration ---

## Manufacturer management fields
MANUFACTURER_FIELDS = [
    ("name", "Name (Required)"),
    ("url", "URL"),
    ("support_url", "Support URL"),
    ("support_phone", "Support Phone"),
    ("support_email", "Support Email")
]

# Helper function to collect inputs
def collect_inputs(is_update=False):
    data = {}
    print("\n--- Please fill out the following fields ---")
    print("(Press Enter to skip a field)")

    for field_key, prompt in MANUFACTURER_FIELDS:
        # For simplicity, ask for everything.
        user_input = input(f"{prompt}: ").strip()
        # Only add to the payload if the user typed something
        if user_input:
            data[field_key] = user_input
    return data

def main():
    mgr = ManufacturerManager(URL, snipeit_api_token)

    #need to sync first for accurate
    print(">> Syncing Manufacturer IDs...")
    mgr.sync_cache()

    while True:
        print("\n=== MANUFACTURER TOOL ===")
        print("1. Search")
        print("2. Create")
        print("3. Update")
        print("q. Quit")

        choice = input("Select: ")

        if choice == '1':
            term = input("Search Name: ")
            results = mgr.search(term)
            for r in results:
                print(f"ID: {r['id']} | {r['name']}")

        elif choice == '2':
            name = input("Name: ")
            url = input("URL (optional): ")
            payload = {
                "name": name,
                "url": url
            }

            res = mgr.create(payload)
            if res.status_code == 200:
                print("Created successfully!")
                mgr.sync_cache() # Refresh list so we can find it immediately
            else:
                print(f"Error: {res.text}")

        elif choice == '3':
            # Search first to get ID
            term = input("Search Name to update: ")
            results = mgr.search(term)
            if not results:
                print("Not found.")
                continue

            for r in results:
                print(f"ID: {r['id']} | {r['name']}")

            target_id = input("Enter ID to update: ")
            new_url = input("New URL (enter to skip): ")

            # Build update data dynamically
            updates = {}
            if new_url: updates['url'] = new_url

            if updates:
                res = mgr.update(target_id, payload=updates)
                if res.status_code == 200:
                    print("Updated!")
                else:
                    print(f"Error: {res.text}")
            else:
                print("No changes made.")

        elif choice.lower() == 'q':
            break

if __name__ == "__main__":
    main()