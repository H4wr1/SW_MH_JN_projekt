import pandas as pd

# Read the second CSV file into a pandas DataFrame
df = pd.read_csv("data_for_measures.csv")

# Drop duplicate rows based on all columns
df_unique = df.drop_duplicates()

# Optionally, reset the index
df_unique.reset_index(drop=True, inplace=True)

# Save the resulting DataFrame back to a CSV file
df_unique.to_csv("second_file_unique.csv", index=False)
