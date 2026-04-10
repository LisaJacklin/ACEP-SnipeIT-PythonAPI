#File: SnipeIT_APIclient.py
#Created: 2026-03-17
#Last edit: 2026-04-07
#
# Description:
#

import requests

class SnipeITClient:
	def __init__ (self, base_url, api_key):
		self.base_url = base_url.rstrip('/')
		self.headers = {
			"Accept": "application/json",
			"Content-Type": "application/json", #added for POST ability
			"Authorization": f"Bearer {api_key}"
		}

	# Used by: SnipeitReport.py
	# pull all the data from the category (assets, license, hardware, etc)
	def get_all(self, endpoint):
		url = f"{self.base_url}/{endpoint}"
		all_records = []
		offset = 0 #default
		limit = 500 #default max per page

		while True:
			params = {"limit": limit, "offset": offset}
			response = requests.get(url, headers=self.headers, params=params)

			if response.status_code !=200:
				print(f"Error {response.status_code}: {response.text}")
				break

			data = response.json()
			rows = data.get("rows", [])
			all_records.extend(rows)

			if len(rows) <limit:
				break

			offset+= limit
		return all_records

	#Used by: asset-automate.py
	# create a single asset
	#todo: test that it can create more than one!
	def create_asset(self, payload):
		url = f"{self.base_url}/hardware"
		response = requests.post(url, headers=self.headers, json=payload)

		#for debugging:
		response.raise_for_status()
		return response.json()

	# Used by: 
	# create a new model
	def create_model(self, payload):
		url = f"{self.base_url}/models"
		response = requests.post(url, headers=self.headers, json=payload)
		response.raise_for_status()
		return response.json()




