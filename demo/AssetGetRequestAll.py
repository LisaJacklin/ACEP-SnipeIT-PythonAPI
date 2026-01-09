#!/usr/bin/env python

#AssetGetRequestAll.py
# - Pulls all assets into a .json file
# - outputs all assets into a easy read table
#Using AssetGetRequestExample.py from SnipeITPythonAPI

import json
from snipeit import Assets
from pathlib import Path
from tabulate import tabulate

server='http://10.8.0.197:8000'
token = Path('../creds/snipeitkey.cred').read_text().strip()

A = Assets()
#r = A.get(server, token, 5) # With a limit of results
r = A.get(server, token) # Using default limit of 50 for results

#decode output for tabulate to process
if isinstance(r, bytes):
    r = r.decode("utf-8")
if isinstance(r, str):
    r = json.loads(r)

# writes to assets.json file all assets w/tags
with open("assets.json", "w") as file:
    print(json.dump(r,file, indent=4))

# Tabulated output
print("\n=== Asset Table ===")
rows = r.get("rows", [])

# Detect custom field names
custom_keys = []
if rows:
    first = rows[0].get("custom_fields", {})
    custom_keys = list(first.keys())   # e.g. ["CPU","GPU","Model Number","Storage","Hostname"]


table = []
for asset in rows:
    base = [
        asset.get("id"),
    #    asset.get("name"),
     #   asset.get("serial"),
        asset.get("asset_tag"),
        asset.get("status_label", {}).get("name"),
        asset.get("model", {}).get("name"),
    ]
      # Add custom field values in same order as headers
    for key in custom_keys:
        value = asset.get("custom_fields", {}).get(key, {}).get("value", "")
        base.append(value)

    table.append(base)

#include in header the specs!
headers = ["ID", "Tag", "Status", "Model"] + custom_keys
print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

