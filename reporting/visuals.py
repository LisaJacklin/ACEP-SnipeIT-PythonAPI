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

# New Line Graph function for Activity Tracking
def create_activity_line_graph(plot_data, title, filepath):
    """Expects a Pandas DataFrame indexed by Date, with columns matching the action trends to plot."""
    plt.figure(figsize=(12, 6))

    # Dynamically plot whatever trend columns are passed in the DataFrame
    colors = ["#007bff", "#28a745", "#dc3545", "#ffc107"]
    markers = ["o", "s", "^", "D"]

    for i, column in enumerate(plot_data.columns):
        plt.plot(
            plot_data.index,
            plot_data[column],
            label=column,
            color=colors[i % len(colors)],
            linewidth=2,
            marker=markers[i % len(markers)],
        )

    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Number of Actions", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Line graph saved to: {filepath}")


## Changes to make for reading the pie chart:
# values not percentagse
# side key or include inside chart