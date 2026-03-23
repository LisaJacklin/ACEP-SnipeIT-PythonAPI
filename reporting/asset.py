#File: asset.py
# 2026-03-18
#
#Description:
#

from collections import Counter

# count of assets based on their status label
def get_status_counts(assets):
	status_counts = Counter()

	for a in assets:
		status_label = a.get('status_label')

		if status_label and isinstance(status_label, dict):
			status_name = status_label.get('name', 'Unknown Status')
			status_counts[status_name] += 1
		else:
			status_counts['No Status Assigned'] += 1

	return dict(status_counts)

# Now to get a count based on location and ready systems
def get_ready_location(assets, ready_status_name="Ready to Deploy"):
	location_counts = Counter()

	for a in assets:
		status_label = a.get('status_label', {})
		if status_label and status_label.get('name') == ready_status_name:

			#note that snipeit Tracks location (location) and default location (rtd)
			location_obj = a.get('location') or a.get('rtd_location') or {}
			location_name = location_obj.get('name', 'Unknown Location')

			location_counts[location_name] += 1

	return dict(location_counts)
