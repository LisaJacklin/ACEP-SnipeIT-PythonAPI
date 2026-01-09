#!/usr/bin/env python

import requests
from pathlib import Path

server='http://10.8.0.197:8000/api/v1/hardware/6' #6 needs to match the system ID
token = Path('../creds/snipeitkey.cred').read_text().strip()


payload = {
    "asset_tag":"ACEP-BLS-23-01",
    "status_id": 2, 
    "model_id": 2, 
    "_snipeit_ram_2":"32 GB" #change me back to 32GB!
    }

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "content-type": "application/json"
}

response = requests.put(server, json=payload, headers=headers)

print(response.text)
