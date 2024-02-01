import pandas as pd
df = pd.read_csv('data_for_measures.csv')
del df['description']
del df['cleaned_title']
del df['cleaned_description']
output_file_path = 'data_for_measures.csv'
df.to_csv(output_file_path, index=False)