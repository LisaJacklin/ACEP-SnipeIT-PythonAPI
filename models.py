#Name: models.py
# Last Updated: 2026-01-22
#
# Description: Model management class for Snipe-IT API interactions.
#

import requests
import json
import os

class ModelManager:
    def __init__(self, url, api_key, cache_file="snipeit_reference_ids.json"):
        self.base_url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.cache_file = cache_file

    #update the reference IDs
    def sync_cache(self):
     print(" [Syncing Models with Snipe-IT...]")
     try:
            # Added limit=2000 to ensure we get everything
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                params={"limit": 2000, "sort": "name", "order": "asc"}
            )

            if response.status_code == 200:
                # Load existing cache to preserve manufacturers/categories if they exist
                full_cache = {}
                if os.path.exists(self.cache_file):
                    with open(self.cache_file, 'r') as f:
                        try:
                            full_cache = json.load(f)
                        except json.JSONDecodeError:
                            full_cache = {}

                rows = response.json().get('rows', [])

                # Save flat structure for easy display
                full_cache['models'] = [{
                    "id": r['id'],
                    "name": r['name'],
                    "model_number": r.get('model_number'),
                    # We store the manufacturer NAME as a string here for display
                    "manufacturer": r.get('manufacturer', {}).get('name', 'Unknown')
                } for r in rows]

                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(full_cache, f, indent=4)

                print(f" [Cache] Synced {len(rows)} models to {self.cache_file}")
                return True
            else:
                print(f"Sync Failed: {response.status_code}")
                return False

     except Exception as e:
            print(f"Sync Error: {e}")
            return False
  # Search, create and update methods similar to ManufacturerManager:
    def search(self, query):
        if not os.path.exists(self.cache_file):
            print("Cache not found. Syncing now...")
            self.sync_cache()

        with open(self.cache_file, 'r') as f:
            data = json.load(f)
            models = data.get('models', [])

        return [m for m in models if query.lower() in m['name'].lower()]

    def create(self, payload):
        return requests.post(f"{self.base_url}/models", headers=self.headers, json=payload)

    def update(self, model_id, payload):
        return requests.patch(f"{self.base_url}/models/{model_id}", headers=self.headers, json=payload)