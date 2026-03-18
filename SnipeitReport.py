# File: SnipeitAssetReport.py
# Date: 2026-03-17
#
# Run:
# Description:
#

import os
from pathlib import Path

#module scripts for api and assets
from reporting import asset
from reporting.api_client import SnipeITClient

# Configuration for API
api_key = Path('prod.cred').read_text().strip()
base_url = "https://snipeit.camio.acep.uaf.edu/api/v1/"

report_dir = "reports"
# creates a directory for reports if it doesn't exist.
def setup_directories():
	if not os.path.exists(report_dir):
		os.makedirs(report_dir)


def main():
	setup_directories()
	client = SnipeITClient(base_url, api_key)

	print("Fetching hardware from Snipe-IT...")
			# Asset == hardware in snipeit api land
	assets = client.get_all("hardware")
	print(f"Successfully retrieved {len(assets)} assets.\n")


if __name__ == "__main__":
			main()