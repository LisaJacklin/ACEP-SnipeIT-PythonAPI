# Name: pull-ids.py
# Last updated: 2026-01-22
#
# Description: Script to gather API reference IDs for use in other Snipe-IT API interactions.
# Usage: python pull-ids.py
#

import requests
import json
import os
import yaml
from pathlib import Path

output_file = "snipeit_reference_ids.json"

#get end point references
def get_reference_list(endpoint, api_url, header):
    print(f"Pulling {endpoint}...")
    clean_list = []
    limit = 500
    offset = 0

    try:
        while True: 
            response = requests.get(f"{api_url}/{endpoint}", headers=header, params={"limit": limit, "offset": offset})

            if response.status_code == 200:
                data = response.json()
                rows = data.get('rows', [])

                #now to gather info for items: 
                for item in rows: 
                    clean_list.append({
                        "id": item.get("id"), 
                        "name": item.get("name", "Unknown Name"),
                        "db_column": item.get("db_column")
                    })

                if len(rows) < limit:
                    break
                offset += limit
            else:
                print(f" Failed to retried {endpoint}. Status: {response.status_code}")
                break
        return clean_list

    except Exception as e:
        print(f"An error occured: {e}")
        return []

# simplify main
def main():
    #load in the config file
    try: 
        with open('sample-config.yaml', 'r') as file:
            full_config = yaml.safe_load(file)
        
        config = full_config[full_config['active_env']]
        api_url = config['domain']

        api_token = Path(config['cred_file']).read_text().strip()

        #api header setup
        header = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json", 
            "Content-Type": "application/json"
        }

    except FileNotFoundError as e: 
        print(f"Could not find config or cred file: {e}")
        return
    
    data_to_store = {
        "manufacturers": get_reference_list("manufacturers", api_url, header),
        "categories": get_reference_list("categories", api_url, header),
        "models": get_reference_list("models", api_url, header),
        "statuslabels": get_reference_list("statuslabels", api_url, header),
        "fieldsets": get_reference_list("fieldsets", api_url, header),
        "fields": get_reference_list("fields", api_url, header),
        
        #additional items for later maybe...
        "locations": get_reference_list("locations", api_url, header),
        "companies": get_reference_list("companies", api_url, header),
        "departments": get_reference_list("departments", api_url, header),
        "suppliers": get_reference_list("suppliers", api_url, header),
        "depreciations": get_reference_list("depreciations", api_url, header)
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
