#File: formatter.py
# 2026-03-18
#
# Description:
#

import json
from datetime import datetime


def create_md_table(title, data_dict, key_header="Category", value_header="Count", add_total=False):
  md = f"## {title}\n\n"
  md += f"| {key_header} | {value_header} |\n"
  md += "| --- | ---: |\n"
  for key, value in sorted(data_dict.items()):
    md += f"| {key} | {value} |\n"
  if add_total:
    total = sum(data_dict.values())
    md += f"| **Total** | **{total}** |\n"
  return md

# default option: save as a .md file in .txt
def save_md_file(content, filepath):
  with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
    print(f"Report saved to: {filepath}")


# added option to save data as json for use in other reports
def save_json_file(data, filepath):
  with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    print(f"JSON data saved to: {filepath}")

