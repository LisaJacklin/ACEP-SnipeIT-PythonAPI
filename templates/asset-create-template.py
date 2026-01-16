import requests
from pathlib import Path

#put rule -> updates an existing thing
url= "http://10.8.0.197:8000/api/v1/hardware"
snipeit_api_token = Path('snipeitkey.cred').read_text().strip()

payload = {
 "asset_tag": "Null",
 "status_id": None, #int32
 "model_id": None, #int32
 "requestable": False, #boolean
 #additional statistics
 "_snipeit_mac_address_1":"null",
 "_snipeit_ram_2":"null",
 "_snipeit_cpu_3":"null",
 "_snipeit_gpu_4":"null",
 "_snipeit_model_number_5":"null",
 "_snipeit_storage_6":"null",
 "_snipeit_hostname_7":"null",
 #additional stats -standard w/SnipeIT
 "archived": False,
 "warranty_months": None,
 "depreciate": False,
 "supplier_id": None,
 "rtd_location_id": None,
 "location_id": None

}

header = {
  "accept": "application/json",
  "Authorization": f"Bearer {snipeit_api_token}",
  "Accept": "application/json",
  "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=header)

print(response.text)
