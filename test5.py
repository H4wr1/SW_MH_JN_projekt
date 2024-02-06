
import pandas as pd
df = pd.read_csv('data_for_measures.csv')

indices_to_exclude = [1154,1428,2755,8338]  # Replace with the indices you want to exclude


df = df.drop(indices_to_exclude)
filtered_df = df[df['language'] == 'ru']
print(filtered_df)
output_file_path = 'data_for_measures.csv'
df.to_csv(output_file_path, index=False)
    