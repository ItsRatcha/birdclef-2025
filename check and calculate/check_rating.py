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

# Load the CSV
df = pd.read_csv("train.csv", header=None)  # remove header=None if CSV has headers

# Group by primary label (column 0)
grouped = df.groupby(0)

count=0
# Check for any group where all values in column 6 are 0.0
for label, group in grouped:
    if all(group[5] == "0"):
        print(f"Label '{label}' has all 0 in column 6.")
        count+=1
print(f"Total labels with all 0 in column 6: {count}")
