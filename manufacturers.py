# Name: manufacturers.py
# Last Updated: 2025-01-22
#
# Description:
# Usage:
#
# Notes:
# - may need to shift base_url to include /api/v1/ depending on usage context...

import requests
import json
import os

class ManufacturerManager:
    def __init__(self, url, api_key, cache_file="snipeit_reference_ids.json"):
        self.base_url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.cache_file = cache_file

    # updates the reference IDs related to manufacturers
    def sync_cache(self):
        try:
            response = requests.get(f"{self.base_url}/manufacturers", headers=self.headers, params={"limit": 500, "sort": "name", "order": "asc"})
            if response.status_code == 200:
                # Load existing cache if it exists to preserve other keys (like categories)
                if os.path.exists(self.cache_file):
                    with open(self.cache_file, 'r') as f:
                        full_cache = json.load(f)
                else:
                    full_cache = {}

                # Update only manufacturers section
                rows = response.json().get('rows', [])
                full_cache['manufacturers'] = [{"id": r['id'], "name": r['name']} for r in rows]

                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(full_cache, f, indent=4)
                return True
            return False
        except Exception as e:
            print(f"Sync Error: {e}")
            return False

    # Search the updated reference IDs for manufacturers by Name
    def search(self, query):
        if not os.path.exists(self.cache_file):
            self.sync_cache()

        with open(self.cache_file, 'r') as f:
            data = json.load(f)
            manufacturers = data.get('manufacturers', [])

        return [m for m in manufacturers if query.lower() in m['name'].lower()]

    # create/post a new manufacturer
    def create(self, payload):
    # json=payload means "send this whole dictionary"
      return requests.post(f"{self.base_url}/manufacturers", headers=self.headers, json=payload)

      # update/patch an existing manufacturer
    def update(self, manufacturer_id, payload):
          return requests.patch(f"{self.base_url}/manufacturers/{manufacturer_id}", headers=self.headers, json=payload)