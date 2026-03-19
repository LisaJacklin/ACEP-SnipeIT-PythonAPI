# File: visuals.py
#2026-03-19
#
# Description:
#

import matplotlib.pyplot as plt
import numpy as np

#pi chart: main focus current is assets
def create_pie_chart(data_dict, title, filepath):
  labels = data_dict.keys()
  sizes = data_dict.values()
  plt.figure(figsize=(8, 8))
  plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
  plt.title(title)
  plt.axis('equal')
  plt.show()

  plt.savefig(filepath, bbox_inches='tight')
  plt.close()
  print(f"Pie chart saved to: {filepath}")


#nested pie chart option
# may be easier to read the locations from this rather than two separate charts
def create_nested_pie_chart(data_dict, title, filepath):

  fig, ax = plt.subplots(figsize=(8, 8))
  size = 0.3

  inner_labels = list(data_dict.keys())
  inner_size = [sum(sub.values()) for sub in data_dict.values()]

  outer_labels = []
  outer_size = []

  for sub_dict in data_dict.values():
    for key, count in sub_dict.items():
      outer_labels.append(key)
      outer_size.append(count)

  ring_width = 0.3

  ax.pie(inner_size, radius=1-ring_width, labels=inner_labels, labeldistance=0.5, wedgeprops=dict(width=ring_width, edgecolor='w'))

  outer_wedge, _ = ax.pie(outer_size, radius=1, labels=outer_labels, wedgeprops=dict(width=ring_width, edgecolor='w'))

  legend_labels = [f"{label} ({size})" for label, size in zip(outer_labels, outer_size)]
  ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1,0.5))

  plt.title(title)
  plt.savefig(filepath, bbox_inches='tight')
  plt.close()
  print(f"Nested pie chart saved to: {filepath}")


## Changes to make for reading the pie chart:
# values not percentagse
# side key or include inside chart
