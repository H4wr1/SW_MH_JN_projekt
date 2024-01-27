import pandas as pd



# Read the previously combined data
combined_file = 'combined_data.csv'
combined_df = pd.read_csv(combined_file)

# Read the cmu_cleaned.csv
cmu_file = 'cmu_cleaned.csv'
cmu_df = pd.read_csv(cmu_file)
#combined_df['book_title'] = combined_df['book_title'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
#combined_df['book_title'] = combined_df['book_title'].str.replace('"', '')
# Remove double quotes from the book_title column
combined_df['book_title'] = combined_df['book_title'].apply(lambda x: ''.join(e for e in x.strip() if e.isalnum() or e.isspace()))
cmu_df['book_title'] = cmu_df['book_title'].apply(lambda x: ''.join(e for e in x.strip() if e.isalnum() or e.isspace()))

# Identify duplicates in the cmu_cleaned.csv and add only non-duplicates to the combined dataframe
combined_df = pd.concat([combined_df, cmu_df[~cmu_df['book_title'].isin(combined_df['book_title'])]])

# Save the updated combined dataframe to a new CSV file
combined_df.to_csv('final_combined_data.csv', index=False)

print("Final combined data saved to final_combined_data.csv")