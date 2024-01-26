import pandas as pd

# Read the two CSV files
file1 = 'scraped_data.csv'
file2 = 'scraped_data_part2.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Combine the two dataframes
combined_df = pd.concat([df1, df2], ignore_index=True)

# Remove records with None (empty) value in the page_count column
combined_df = combined_df.dropna(subset=['page_count'])

# Remove records where the description contains the specified text
combined_df = combined_df[~combined_df['description'].str.contains('Ta książka nie posiada jeszcze opisu.')]

# Save the combined and cleaned dataframe to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)

print("Combined data saved to combined_data.csv")

