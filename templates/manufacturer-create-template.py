import requests
from pathlib import Path

#put rule -> updates an existing thing
url= "https://snipeit.camio.acep.uaf.edu/api/v1/manufacturers"
snipeit_api_token = Path('../prod.cred').read_text().strip()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {snipeit_api_token}"
}

payload = {
    # required fields
    "name": "Acer",
    # additional fields:
    "url": "https://www.acer.com/us-en/",
    #"support_url": "null",
    #"support_phone": "null",
    #"support_email": "null",
    #"notes": "null"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)