import pandas as pd

df = pd.read_csv('train.csv')
df.drop(df.columns[[3, 4, 5, 6, 9, 10, 11, 12]], axis=1, inplace=True)
df.to_csv('train_cleaned.csv', index=False)