from transformers import AutoTokenizer
import pandas as pd

# Load CSV
df = pd.read_csv('train_cleaned.csv')

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Combine all text into one string (or per row/column if needed)
text = df.astype(str).apply(' '.join, axis=1).tolist()

# Count total tokens
total_tokens = sum(len(tokenizer.encode(row)) for row in text)

print(f"Total tokens: {total_tokens}")
