# pull-ids.py
# Last updated: 2026-01-21
#
# Script to gather API reference IDs for use in other Snipe-IT API interactions.
## Usage:
#   python pull-ids.py

import requests
import json
from pathlib import Path

URL = "https://snipeit.camio.acep.uaf.edu"
snipeit_api_token = Path('prod.cred').read_text().strip()

header = {
 # "accept": "application/json",
  "Authorization": f"Bearer {snipeit_api_token}",
  "Accept": "application/json",
  "Content-Type": "application/json"
}

#get end point references
def get_reference_list(endpoint):
    response = requests.get(f"{URL}/api/v1/{endpoint}", headers=header, params={"limit":500})

    if response.status_code == 200:
        data = response.json()
        print(f"\n --- {endpoint.upper()} LIST --- \n")
        for item in data['rows']:
            print(f"{item['id']}: {item['name']}")
    else:
        print(f"Error: Unable to fetch data from {endpoint}. Status code: {response.status_code}")

if __name__ == "__main__":
   get_reference_list("manufacturers")
   get_reference_list("categories")
   get_reference_list("models")
   get_reference_list("statuslabels")

   # what other tags might be good for me to keep an eye on and store.....?
   # note: what is protected and something I don't want ie: should I ignore this information and push it to .gitignore?