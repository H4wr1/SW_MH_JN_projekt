import pandas as pd
df = pd.read_csv('data_for_measures.csv')
counts = df['language'].value_counts()
print(counts)
