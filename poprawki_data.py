
import pandas as pd
df = pd.read_csv('data_for_measures9.csv')

indices_to_exclude = [1154,1428,2755,8338]  # Replace with the indices you want to exclude

#df.count
df = df.drop(indices_to_exclude)
filtered_df = df[df['language'] == 'ru']
print(df.count)
output_file_path = 'data_for_measures9.csv'
df.to_csv(output_file_path, index=False)
    