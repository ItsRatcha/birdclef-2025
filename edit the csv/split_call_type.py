import pandas as pd
import os
import ast
import re

# Load CSV
df = pd.read_csv("train.csv")

# Parse call types from third column
df['call_types'] = df.iloc[:, 2].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

# Create output directory
os.makedirs("type_of_call", exist_ok=True)

# Get all unique types
all_types = set(t for sublist in df['call_types'] for t in sublist)
all_types.add('no_type')

# Sanitize function for filenames
def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Prepare and save CSVs
for call_type in all_types:
    if call_type == 'no_type':
        filtered = df[df['call_types'].apply(lambda x: len(x) == 0)]
    else:
        filtered = df[df['call_types'].apply(lambda x: call_type in x)]
    safe_name = safe_filename(call_type)
    filtered.drop(columns=['call_types']).to_csv(f"type_of_call/{safe_name}.csv", index=False)
