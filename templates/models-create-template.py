import requests
from pathlib import Path

url= "https://snipeit.camio.acep.uaf.edu/api/v1/models"
snipeit_api_token=Path('prod.cred').read_text().strip()

payload = {
	#required: 
	"category_id": 1, 
	"name": "string"
	# Additional: 
	# "model_number": "string"
	# "manufacturer_id: 1,
	# "eol": 1
	# filedset_id: 1; #note this is the ID of an EXISTING fieldset
}

header = {
	"accept": "application/json", 
	"Authorization": f"Bearer {snipeit_api_token}", 
	"Accept": "application/json", 
	"content-type": "application/json"
}

response = requests.post(url, json=payload, headers=header)

print(response.text)
