import pandas as pd

df1 = pd.read_csv('final_combined_data copy.csv')
df2 = pd.read_csv('final_combined_data.csv')

unique_rows_in_file1 = df1[~df1['book_link'].isin(df2['book_link'])]

unique_rows_in_file2 = df2[~df2['book_link'].isin(df1['book_link'])]

#print("\nUnique rows in file 2:")
#print(unique_rows_in_file2.head())
unique_rows_in_file2.to_csv('unique_rows_file2.csv', index=False)