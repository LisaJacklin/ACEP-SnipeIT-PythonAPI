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

#attempt to pull in the custom fields created
def get_fieldset_mapping(fieldset_name, api_url, header):
    field_map = {}

    try: 
        response = requests.get(f"{api_url}/fieldsets/", headers=header)
        if response.status_code != 200:
            print("Failed to pull custom fieldsets")
            return {}

        target_id = None
        for fs in response.json().get('rows', []):
            if fs.get('name') == fieldset_name:
                target_id = fs.get('id')
                break

        if not target_id:
            print(f"Could not find a fieldset named '{filedset_name}")
            return {}

        # get fields assigned to the fieldset
        fields_resp = requests.get(f"{api_url}/fildsets/{target_id}/fields", headers=header)
        if response.status_code == 200:
            for field in fields_resp.json().get('rows', []): 
                label = field.get('name')
                db_name = field.get('db_column')

                if label and db_name:
                    mapping[label] = db_name

        return field_map

    except Exception as e:
        print(f"Error occured while mapping: {e}")
        return {}

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
    
    # hardcoded custom fields db_name...
    #haven't had luck yet with being able to query them without getting Null
    system_specs = {
        "RAM_GB":"_snipeit_ram_gb_2",
        "Storage_GB":"_snipeit_storage_gb_3",
        "Hostname":"_snipeit_hostname_4", 
        "Operating System":"_snipeit_operating_system_5", 
        "CPU":"_snipeit_cpu_10", 
        "GPU":"_snipeit_gpu_11", 
        "Model Number":"_snipeit_model_number_30",
        "UUID":"_snipeit_uuid_31"

        #other fields not needed off the bat...
        # "MAC Address":"_snipeit_mac_address_1", 
        # "UA Domain":"_snipeit_ua_domain_6", 
        # "ACEP OU":"_snipeit_acep_ou_7", 
        # "Login":"_snipeit_login_8"
    }

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
        "depreciations": get_reference_list("depreciations", api_url, header),
        "system_specs": system_specs
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
