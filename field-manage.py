#Name: field-manage.py
# Last Updated: 2026-01-23
#
# Description:
# Useage:
#

import requests
import json
import os
from pathlib import Path

## Standard Configurations ---
url = "https://snipeit.camio.acep.uaf.edu/api/v1"
snipeit_api_token = Path('prod.cred').read_text().strip()
header = {
    "Authorization": f"Bearer {snipeit_api_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
## End Standard Configurations ---

from fields.py import FieldManager

def main():
    snipe = FieldManager(URL, TOKEN)

    print("--- 1. Listing current Fieldsets ---")
    fieldsets = snipe.list_fieldsets()
    if fieldsets and 'rows' in fieldsets:
        for fs in fieldsets['rows']:
            print(f"ID: {fs['id']} | Name: {fs['name']}")

if __name__ == "__main__":
    main()