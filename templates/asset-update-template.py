
import requests
from pathlib import Path

#put rule -> updates an existing thing
url= "http://10.8.0.197:8000/ap/v1/hardware/10"
snipeit_api_token = Path('snipeitkey.cred').read_text().strip()

#information for new asset:
payload = {
        "location_id": None,
        "asset_tag":"null", #
        "notes":"null", #
        "requestable": False,
        #"serial": "null",
        # custom field tags
        "_snipeit_mac_address_1":"null",
        "_snipeit_ram_2":"null",
        "_snipeit_cpu_3":"null",
        "_snipeit_gpu_4":"null",
        "_snipeit_model_number_5":"null",
        "_snipeit_storage_6":"null",
        "_snipeit_hostname_7":"null"
        #other
        #"last_checkout": "null",
        #"assigned_user": None,
        #"assigned_location": None,
        #"assigned_asset": None,
        #"company_id": None,
        #"warranty_months": None,
        #"purchase_cost": None,
        #"purchase_date":"null",
        #"archived": False,
        #"image":"null",
        #"rtd_location_id": None,
        #"name:":"null",

        }

headers = {

        "accept": "application/json",
        "Authorization": snipeit_api_token,
        "Accept": "application/json",
        "content-type": "application/json"
        }

response = requests.put(url, json=payload, headers=headers)

print(response.text)
