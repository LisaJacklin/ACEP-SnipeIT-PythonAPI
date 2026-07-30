# File: trend-plot.py
# Date: 2026-07-14
#
# Run: python3 trend-plot.py
# Description:
#

import pandas as pd
import plotly.graph_objects as go

# 1. Load your Snipe-IT CSV file
# Replace 'snipeit_log.csv' with your actual file path
csv_file = "activity-report-2026-07-16-072022.csv"
df = pd.read_csv(csv_file, on_bad_lines='skip')

# 2. Map your columns (Adjust these strings to match your CSV headers)
# Typical Snipe-IT headers might be "Date", "Created At", "Action", "Activity", etc.
DATE_COL = "Date"      
ACTION_COL = "Action"  

# Convert the date column to a standard datetime format
df[DATE_COL] = pd.to_datetime(df[DATE_COL])


# 3. Filter for each specific action
adds_df = df[df[ACTION_COL].str.lower().str.contains("create new|add", na=False)]
updates_df = df[df[ACTION_COL].str.lower().str.contains("update|edit", na=False)]
checkouts_df = df[df[ACTION_COL].str.lower().str.contains("checkout|checked out", na=False)]
checkins_df = df[df[ACTION_COL].str.lower().str.contains("checkin|checked in", na=False)]

maintenance_df = df[df[ACTION_COL].str.lower().str.contains("maintenance|repair|service", na=False)]

# 4. Group by Date to get daily counts
adds_daily = adds_df.groupby(df[DATE_COL].dt.date).size().reset_index(name="Count")
updates_daily = updates_df.groupby(df[DATE_COL].dt.date).size().reset_index(name="Count")
checkouts_daily = checkouts_df.groupby(df[DATE_COL].dt.date).size().reset_index(name="Count")
checkins_daily = checkins_df.groupby(df[DATE_COL].dt.date).size().reset_index(name="Count")

maintenance_daily = maintenance_df.groupby(df[DATE_COL].dt.date).size().reset_index(name="Count")

# 5. Create the Interactive Plotly Figure
fig = go.Figure()

# Add line for Assets Updated
fig.add_trace(go.Scatter(
    x=adds_daily[DATE_COL], 
    y=adds_daily["Count"],
    mode="lines+markers",
    name="New Assets",
    line=dict(color="#0fd0aa", width=2) # Blue 
))

# --- Line 3: Checkouts ---
fig.add_trace(go.Scatter(
    x=checkouts_daily[DATE_COL], 
    y=checkouts_daily["Count"],
    mode="lines+markers",
    name="Checkouts",
    line=dict(color="#ff0000", width=2) # Red
))

# --- Line 4: Checkins ---
fig.add_trace(go.Scatter(
    x=checkins_daily[DATE_COL], 
    y=checkins_daily["Count"],
    mode="lines+markers",
    name="Checkins",
    line=dict(color="#90ee90", width=2) # Purple
))



# 6. Add Range Selector Buttons and Slider for Date Ranges
fig.update_layout(
    title="Snipe-IT Asset Activity Over Time",
    xaxis_title="Date",
    yaxis_title="Number of Actions",
    hovermode="x unified",
    yaxis=dict(
       # range=[0,15],
        fixedrange=False
    ),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True), # Adds the slider at the bottom
        type="date"
    ),
    template="plotly_white"
)

# Show the interactive plot in your browser
fig.show()
