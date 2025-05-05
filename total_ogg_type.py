import pandas as pd
import matplotlib.pyplot as plt
import re

# --- Load durations from your text file ---
def parse_duration(duration_str):
    h, m, s = map(int, re.findall(r'\d+', duration_str))
    return h * 3600 + m * 60 + s

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"

durations = {}
with open("ogg_length.txt", "r") as f:
    for line in f:
        if ":" in line:
            parts = line.strip().split(":")
            if len(parts) < 2: continue
            id_ = parts[0].strip()
            time_str = ":".join(parts[1:]).strip()
            durations[id_] = parse_duration(time_str)

# --- Load taxonomy.csv ---
taxonomy = pd.read_csv("taxonomy.csv")

# --- Build a DataFrame from durations ---
df = pd.DataFrame(list(durations.items()), columns=["primary_label", "total_seconds"])

# --- Merge with taxonomy on primary_label ---
merged = pd.merge(df, taxonomy, on="primary_label", how="left")

# --- Debug check: what's missing ---
print("Null values per column:\n", merged.isnull().sum())
print("Unique class_name:\n", merged["class_name"].unique())

# --- Group by class_name and sum durations ---
grouped = merged.groupby("class_name")["total_seconds"].sum().sort_values(ascending=False)

# --- Convert durations to hours and minutes ---
grouped_formatted = grouped.apply(format_duration)

# --- Print durations for each class ---
print("Total duration by class (hours and minutes):")
print(grouped_formatted)

# --- Plot ---
plt.figure(figsize=(10, 6))
grouped.plot(kind="bar", color="skyblue")
plt.title("Total OGG Duration by Class")
plt.xlabel("Class Name")
plt.ylabel("Total Duration (seconds)")
plt.xticks(rotation=45)

# Add formatted durations as text labels on the bars
for i, (class_name, total_seconds) in enumerate(grouped.items()):
    plt.text(i, total_seconds, format_duration(total_seconds), ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
