import pandas as pd
import ast

# Load CSV
df = pd.read_csv('train.csv', header=None)

# Set of banned keywords
banned = {'call', 'song', 'flight call'}

def is_valid(label_str):
    try:
        labels = ast.literal_eval(label_str)  # Convert string to list
        if not labels or labels == ['']: return False
        for label in labels:
            if any(bad in label.lower() for bad in banned):
                return False
        return True
    except:
        return False  # In case of malformed data

# Apply filter
count = df[2].apply(is_valid).sum()

print("Valid label count (not empty, not containing song/call/flight call):", count)
