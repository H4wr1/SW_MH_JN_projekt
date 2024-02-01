import pandas as pd

file1 = 'scraped_data.csv'
file2 = 'scraped_data_part2.csv'


df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)


combined_df = pd.concat([df1, df2], ignore_index=True)

combined_df = combined_df.dropna(subset=['page_count'])

combined_df = combined_df[~combined_df['description'].str.contains('Ta książka nie posiada jeszcze opisu.')]

combined_df.to_csv('combined_data.csv', index=False)

print("Combined data saved to combined_data.csv")

combined_file = 'combined_data.csv'
combined_df = pd.read_csv(combined_file)


cmu_file = 'cmu_cleaned.csv'
cmu_df = pd.read_csv(cmu_file)
#combined_df['book_title'] = combined_df['book_title'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
#combined_df['book_title'] = combined_df['book_title'].str.replace('"', '')

##cmu_df['book_title'] = cmu_df['book_title'].apply(lambda x: ''.join(e for e in x.strip() if e.isalnum() or e.isspace()))

combined_df = pd.concat([combined_df, cmu_df[~cmu_df['book_title'].isin(combined_df['book_title'])]])

combined_df.to_csv('final_combined_data.csv', index=False)

print("Final combined data saved to final_combined_data.csv")