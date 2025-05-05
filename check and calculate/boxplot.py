import matplotlib.pyplot as plt

# Data for the boxplots
original_data = {
    "Mean": 35.35,
    "Median": 20.98,
    "Variance": 2560.70,
    "Std_dev": 50.60,
    "Min": 0.54,
    "Max": 1774.39,
    "25_percentile": 10.58,
    "75_percentile": 41.30,
    "Iqr": 30.72
}

filtered_data = {
    "Mean": 24.83,
    "Median": 19.12,
    "Variance": 375.85,
    "Std_dev": 19.39,
    "Min": 0.54,
    "Max": 87.38,
    "25_percentile": 10.00,
    "75_percentile": 34.43,
    "Iqr": 24.43
}

# Boxplot values
original_box = [original_data["Min"], original_data["25_percentile"], original_data["Median"], original_data["75_percentile"], original_data["Max"]]
filtered_box = [filtered_data["Min"], filtered_data["25_percentile"], filtered_data["Median"], filtered_data["75_percentile"], filtered_data["Max"]]

# Create the boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([original_box, filtered_box], labels=["Original", "Filtered"], showmeans=True)

# Add titles and labels
plt.title("Boxplot of File Lengths (Original vs Filtered)")
plt.ylabel("Length (seconds)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.show()