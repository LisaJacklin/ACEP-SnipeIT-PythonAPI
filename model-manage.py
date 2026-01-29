#Name: model-manage.py
# Last Updated: 2026-01-22
#
# Description: Model Management Tool for Snipe-IT
# Usage: python3 model-manage.py
#

import requests
import json
import os
from pathlib import Path

from models import ModelManager

## Standard Configuration ---
URL = "https://snipeit.camio.acep.uaf.edu/api/v1"
snipeit_api_token = Path('prod.cred').read_text().strip()
header = {
    "Authorization": f"Bearer {snipeit_api_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
## End Standard Configuration ---

REF_FILE = "snipeit_reference_ids.json"

def load_references():
    if not os.path.exists(REF_FILE):
        print(f"CRITICAL ERROR: {REF_FILE} not found!")
        print("Please run your 'get_ids.py' or Manufacturer script first to generate it.")
        return None

    with open(REF_FILE, 'r') as f:
        return json.load(f)

def select_from_list(prompt_name, data_list):
    while True:
        search = input(f"\nSearch for {prompt_name} (or 'enter' to see all): ").lower().strip()
        matches = [item for item in data_list if search in item['name'].lower()]

        if not matches:
            print("No matches found. Try again.")
            continue

        print(f"--- Select {prompt_name} ---")
        for i, item in enumerate(matches):
            print(f"{i + 1}. {item['name']} (ID: {item['id']})")

        selection = input("Enter number to select (or 'r' to retry): ")
        if selection.lower() == 'r':
            continue
        try:
            index = int(selection) - 1
            if 0 <= index < len(matches):
                return matches[index]['id'] # Return the actual ID (e.g., 3)
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")

def select_model_from_results(results):
    """ Helper to pick a specific model from a search result list """
    if not results:
        print("No models found.")
        return None

    print("\n--- Matching Models ---")
    for i, r in enumerate(results):
        # Note: 'manufacturer' is a string in the cache, not a dict
        man_name = r.get('manufacturer', 'Unknown')
        print(f"{i + 1}. {r['name']} (ID: {r['id']}) - Manuf: {man_name}")

    choice = input("\nSelect Model # to Update (or 'c' to cancel): ")
    if choice.lower() == 'c':
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(results):
            return results[idx]
    except ValueError:
        pass

    print("Invalid selection.")
    return None

def main():
    mgr = ModelManager(URL, snipeit_api_token)
    refs = load_references()

    if not refs:
        return # Stop if we don't have the reference file

    #formatted just like manufacture-manage.py to keep things consistent
    while True:
        print("\n=== MODEL MASTER TOOL ===")
        print("1. Search Models")
        print("2. Create New Model")
        print("3. Update Model")
        print("q. Quit")

        choice = input("Select: ")

        if choice == '1':
            term = input("Search Model Name: ")
            results = mgr.search(term)
            print(f"\nFound {len(results)} models:")
            for r in results:
                # Models have nested data, so we access r['manufacturer']['name']
                man_name = r.get('manufacturer', {}).get('name', 'Unknown')
                print(f"ID: {r['id']} | {r['name']} ({man_name})")

        elif choice == '2':
            print("\n--- New Model Wizard ---")

            name = input("Model Name (e.g. MacBook Pro 14): ")
            model_number = input("Model Number (Optional): ")
            # This loops until the user picks a valid ID from your JSON list
            man_id = select_from_list("Manufacturer", refs.get('manufacturers', []))
            cat_id = select_from_list("Category", refs.get('categories', []))
            payload = {
                "name": name,
                "manufacturer_id": man_id,
                "category_id": cat_id,
                "model_number": model_number
            }
            res = mgr.create(payload)
            if res.status_code == 200:
                print("SUCCESS! Model created.")
            else:
                print(f"FAILED: {res.text}")
        #update model set
        # todo edit this!
        elif choice == '3':
            term = input("Search Model to Update: ")
            results = mgr.search(term)
            target = select_model_from_results(results)

            if not target:
                continue

            print(f"\nUpdating: {target['name']} (ID: {target['id']})")
            print("Leave fields blank to keep current value.")

            new_name = input(f"New Name [{target['name']}]: ").strip()
            new_mod_num = input(f"New Model # [{target.get('model_number', '')}]: ").strip()

            change_man = input("Change Manufacturer? (y/N): ").lower()
            new_man_id = None
            if change_man == 'y':
                new_man_id = select_from_list("Manufacturer", refs.get('manufacturers', []))

            change_cat = input("Change Category? (y/N): ").lower()
            new_cat_id = None
            if change_cat == 'y':
                new_cat_id = select_from_list("Category", refs.get('categories', []))

            # Build Payload
            payload = {}
            if new_name: payload['name'] = new_name
            if new_mod_num: payload['model_number'] = new_mod_num
            if new_man_id: payload['manufacturer_id'] = new_man_id
            if new_cat_id: payload['category_id'] = new_cat_id

            if not payload:
                print("No changes entered.")
                continue

            res = mgr.update(target['id'], payload)
            if res.status_code == 200:
                print("SUCCESS! Model updated.")
                print("Note: Run 'Force Sync' to see changes in local search.")
            else:
                print(f"FAILED: {res.text}")


        elif choice.lower() == 'q':
            break

if __name__ == "__main__":
    main()