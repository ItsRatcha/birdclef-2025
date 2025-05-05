import pandas as pd

# Load the CSV
df = pd.read_csv("train.csv", header=None)  # remove header=None if your CSV has headers

# Group by first column (primary label)
grouped = df.groupby(0)
i=0
# Check for any group where all values in the third column are '-'
for label, group in grouped:
    if all(group[2] == "['']"):
        print(f"Label '{label}' has all '-' in third column.")
        i+=1
print(f"Total labels with all '-' in third column: {i}")
