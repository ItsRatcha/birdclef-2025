import pandas as pd

# Load CSV
df = pd.read_csv("train.csv")

# Get the second column (index 1)
second_col = df.iloc[:, 1]

# Count empty values (NaN or empty string)
empty_count = second_col.isna().sum() + (second_col == '').sum()

# Count occurrences of each unique non-empty value
value_counts = second_col.value_counts()

# Print results
print("Empty:", empty_count)
print("\nValue Counts:\n", value_counts)
