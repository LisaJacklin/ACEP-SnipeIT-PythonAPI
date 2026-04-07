#File: api_client.py
# 2026-03-17
#
# Description:
#

import requests

class SnipeITClient:
	def __init__ (self, base_url, api_key):
		self.base_url = base_url.rstrip('/')
		self.headers = {
			"Accept": "application/json",
			"Authorization": f"Bearer {api_key}"
		}

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

