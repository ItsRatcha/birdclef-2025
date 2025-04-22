import pandas as pd
import os
import plotly.express as px

# Folder with CSVs
folder = "type_of_call"

# Count rows in each CSV
data = []
for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        path = os.path.join(folder, filename)
        count = len(pd.read_csv(path))
        data.append({"call_type": filename.replace(".csv", ""), "count": count})

# Create DataFrame and sort
df = pd.DataFrame(data)
df = df.sort_values(by="count", ascending=False)

# Generate bar chart
fig = px.bar(df, x="call_type", y="count", title="Call Type Counts (Sorted)", text_auto=True)
fig.update_layout(xaxis_title="Call Type", yaxis_title="Number of Samples")

# Save to HTML
fig.write_html("call_type_chart.html")
