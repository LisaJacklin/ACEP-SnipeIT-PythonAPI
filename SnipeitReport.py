# File: SnipeitAssetReport.py
# Date: 2026-03-17
#
# Run:
# Description:
#

import os
from pathlib import Path
from datetime import datetime

#module scripts for api and assets
from reporting import asset
from reporting.api_client import SnipeITClient
from reporting import formatter

# Configuration for API
api_key = Path('prod.cred').read_text().strip()
base_url = "https://snipeit.camio.acep.uaf.edu/api/v1/"

report_dir = "reports"
date_str = datetime.now().strftime("%Y-%m-%d")

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
	#print(f"Successfully retrieved {len(assets)} assets.\n")

	# Run Metric 1: Asset Count by Status
	print("--- Asset Counts by Status Label ---")
	status_counts = asset.get_status_counts(assets)
	for status, count in sorted(status_counts.items()):
			print(f"{status}: {count}")

	total_assets = sum(status_counts.values())
	print(f"\nTotal Assets: {total_assets}")

	print("\n--- 'Ready to Deploy' Assets by Location ---")
			# Run Metric 2: Ready to Deploy by Location
	location_counts = asset.get_ready_location(assets)
	for location, count in sorted(location_counts.items()):
					print(f"{location}: {count}")

	print("\n--- Generating Report ---")
	# Generate Markdown report

	status_md = formatter.create_md_table(
		"Asset Counts by Status", status_counts, add_total=True)
	location_md = formatter.create_md_table(
		"'Ready to Deploy' Assets by Location", location_counts, add_total=True)

  # Save the report as a .md file
	md_filepath = os.path.join(report_dir, f"snipeit_report_{date_str}.md")
	formatter.save_md_file(status_md + "\n\n" + location_md, md_filepath)


if __name__ == "__main__":
			main()