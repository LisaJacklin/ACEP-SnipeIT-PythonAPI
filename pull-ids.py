# Name: pull-ids.py
# Last updated: 2026-01-22
#
# Description: Script to gather API reference IDs for use in other Snipe-IT API interactions.
# Usage: python pull-ids.py
#

import requests
import json
import os
from pathlib import Path

## Standard Configuration ---
URL = "https://snipeit.camio.acep.uaf.edu"
snipeit_api_token = Path('prod.cred').read_text().strip()

header = {
  "Authorization": f"Bearer {snipeit_api_token}",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
## End Standard Configuration ---
output_file = "snipeit_reference_ids.json"

#get end point references
def get_reference_list(endpoint):
    try:
        response = requests.get(f"{URL}/api/v1/{endpoint}", headers=header, params={"limit":500})

        if response.status_code == 200:
            data = response.json()
            clean_list = []
            # Extract only 'id' and 'name' from each item
            for item in data.get('rows', []):
                clean_list.append({
                    "id": item["id"],
                    "name": item["name"]
                })
            return clean_list
        else:
            print(f"Failed to retrieve {endpoint}. Status code: {response.status_code}")
            return []

    except Exception as e:
            print(f"An error occurred: {e}")
            return []

# simplify main
def main():
    data_to_store = {
        #add/remove components as determined they are needed
        "manufacturers": get_reference_list("manufacturers"),
        "categories": get_reference_list("categories"),
        "models": get_reference_list("models"),
        "statuslabels": get_reference_list("statuslabels"),
        "fieldsets": get_reference_list("fieldsets"),
        "fields": get_reference_list("fields")
    }

    #store output to json file
    try:
         with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_store, f, indent=4)
            print(f"Reference IDs saved to {output_file}")

    except Exception as e:
        print(f"An error occurred while writing to file: {e}")

if __name__ == "__main__":
    main()

   # note: what is protected and something I don't want ie: should I ignore this information and push it to .gitignore?