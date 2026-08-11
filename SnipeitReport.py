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
from reporting import asset, formatter, visuals
from reporting.api_client import SnipeITClient

#import pandas to tackle activities
import pandas as pd

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

	# 0: Need to get all data from the api and other tools
	print("Fetching hardware from Snipe-IT...")
	# Asset == hardware in snipeit api land
	assets = client.get_all("hardware")
	#print(f"Successfully retrieved {len(assets)} assets.\n")

	print("Gathering activity reports...")
	raw_json = os.path.join(
		report_dir, f"raw_activity_report_2026_07_07.json"
	)
	formatter.save_json_file(assets, raw_json)

	# 1: Asset Count by Status
	print("--- Asset Counts by Status Label ---")
	status_counts = asset.get_status_counts(assets)
	for status, count in sorted(status_counts.items()):
			print(f"{status}: {count}")

	total_assets = sum(status_counts.values())
	print(f"\nTotal Assets: {total_assets}")

	print("\n--- 'Ready to Deploy' Assets by Location ---")
			
			
	#2: Ready to Deploy by Location
	location_counts = asset.get_ready_location(assets)
	for location, count in sorted(location_counts.items()):
					print(f"{location}: {count}")

	#3: Activity Log Processes
	## TODO: update dates somewhere for reporting....create a config?
	print("--- Processing Activity Logs ---")
	start_date = "2026-04-01"
	end_date = "2026-07-01"

	timeline_data = formatter.process_activity_timeline(
		raw_json_path=raw_json,
		start_date_str=start_date,
		end_date_str=end_date
	)
# Convert dictionary to DataFrame for visuals mapping
	plot_df = pd.DataFrame.from_dict(timeline_data, orient="index")
	plot_df.index = pd.to_datetime(plot_df.index)

	print("\n--- Generating Report ---")
	# Generate Markdown report
	date_str = datetime.now().strftime("%Y-%m-%d")

  # building the markdown tables for the report
	status_md = formatter.create_md_table(
		"Asset Counts by Status", status_counts, add_total=True)
	location_md = formatter.create_md_table(
		"'Ready to Deploy' Assets by Location", location_counts, add_total=True)

  #dates and picharts for report
	status_pie_chart = report_dir + f"/status_pie_chart_{date_str}.png"
	visuals.create_pie_chart(status_counts, "Asset Counts by Status", status_pie_chart)

	location_pie_chart = report_dir + f"/location_pie_chart_{date_str}.png"
	visuals.create_pie_chart(location_counts, "'Ready to Deploy' Assets by Location", location_pie_chart)
	#include the visuals!
	#image_links = f"""
	#	![Asset Counts by Status]({status_pie_chart})
	#	![Ready to Deploy Assets by Location]({location_pie_chart})
	#"""
	# Generate Activity Line Graph
	trend_line_graph = os.path.join(
        report_dir, f"activity_trends_{date_str}.png"
    )

	visuals.create_activity_line_graph(
        plot_data=plot_df,
        title=f"Asset Allocation Trends ({start_date} to {end_date})",
        filepath=trend_line_graph,
    )


# 4. Put all your text blocks into a clean list
	report_sections = (
        "# Snipe-IT Hardware Report",
        status_md,
        location_md,
        #image_links
    )

    # 5. Automatically stitch them together with perfect double line-breaks
	full_markdown_report = "\n\n".join(report_sections)

	print("\n--- DEBUG: END OF MARKDOWN STRING ---")
	print(full_markdown_report)
	print("-------------------------------------\n")

  # Save the report as a .md file
	md_filepath = os.path.join(report_dir, f"snipeit_report_{date_str}.md")
	formatter.save_md_file(full_markdown_report, md_filepath)



if __name__ == "__main__":
			main()