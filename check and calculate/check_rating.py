import pandas as pd

# Load CSV
df = pd.read_csv("train.csv")

# Get column 6 (index 5)
col6 = df.iloc[:, 5]

# Count unique values
unique_count = col6.nunique(dropna=True)
value_counts = col6.value_counts()

# Print results
print("Number of unique values in column 6:", unique_count)
print("\nCounts of each value:\n", value_counts)
