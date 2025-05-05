import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("train.csv")

# Define target location and range
target_lat = 6.76
target_lon = -74.21
tol = 0.5

# Filter data within range
filtered = df[
    (df.iloc[:, 7] >= target_lat - tol) & (df.iloc[:, 7] <= target_lat + tol) &
    (df.iloc[:, 8] >= target_lon - tol) & (df.iloc[:, 8] <= target_lon + tol)
]

# Count unique species
unique_species_count = filtered.iloc[:, 10].nunique()
print(f"Unique species in area: {unique_species_count}")

# Rename columns for clarity
filtered = filtered.rename(columns={
    filtered.columns[7]: "latitude",
    filtered.columns[8]: "longitude",
    filtered.columns[10]: "common_name"
})

# Set up plot
plt.figure(figsize=(12, 10))
scatter = sns.scatterplot(
    data=filtered,
    x="longitude", y="latitude",
    hue="common_name",
    palette="tab20",  # change if more than 20 species
    s=60,
    edgecolor='black',
    linewidth=0.5
)

# Add target lines
plt.axhline(target_lat, color='red', linestyle='--', linewidth=2, label='Target Latitude')
plt.axvline(target_lon, color='blue', linestyle='--', linewidth=2, label='Target Longitude')

# Titles and labels
plt.title(f"Species near (6.76, -74.21)\n±0.2 Lat/Lon — {unique_species_count} Unique Species", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)

# Legend handling
handles, labels = scatter.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

# Save figure
plt.tight_layout()
plt.savefig("species_map.png", dpi=300)
plt.close()

print("Map saved as species_map.png with labeled species and target lines.")
