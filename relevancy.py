import pandas as pd
import simplemma
import stopwordsiso as stopwords
import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')
print(stopwords.fileids())
# Load the CSV file into a DataFrame
file_path = 'final_combined_data copy.csv'
df2 = pd.read_csv('unique_rows_file2.csv')
df = pd.read_csv(file_path)
num_rows = df.shape[0]
print("Number of rows:", num_rows)
df = df[~df['language'].isin(['kaszubski', 'esperanto','białoruski', 'japoński', 'łaciński', 'ukraiński'])]

indices_to_exclude = [11347, 10423, 15063, 15246, 15112, 14504, 11995, 10911, 2974, 988, 1074, 15313, 14107, 8947, 16783, 16742, 15471, 15332, 14678, 14370, 14247, 13873, 8504, 7036, 6609, 6407, 5967, 5358, 5581, 5719, 5847, 4953, 4944, 4573, 4565, 3818, 3679, 2310, 2868, 6051, 6358, 6536, 7450, 7625, 8149, 13853, 13860, 589, 784, 918, 1252, 1356, 1725, 1954, 2290, 2518, 2848, 2994, 3329, 3667, 3913, 4259, 4668, 5107, 5109, 5566, 5582, 6945, 6946, 6958, 7049, 8128, 8136, 8142, 8147, 6995]  # Replace with the indices you want to exclude
num_rows = df.shape[0]
print("Number of rows:", num_rows)
# Use drop method to exclude rows by index
df = df.drop(indices_to_exclude)
num_rows = df.shape[0]
print("Number of rows:", num_rows)
#df['book_link'] = df['book_link'].str.strip()
# Delete rows with links in the exclusion list
#df = df[~df['book_title'].isin(links_to_exclude)]
# Define a mapping of translations
df = pd.concat([df, df2], ignore_index=True)
num_rows = df.shape[0]
print("Number of rows:", num_rows)
language_mapping = {
    'polski': 'polish', 
    'angielski': 'english',
    'niemiecki': 'german',
    'rosyjski': 'russian',
    'francuski': 'french',
    'szwedzki': 'swedish',
    'hiszpański': 'spanish', 
    'norweski': 'norwegian', 
    'włoski': 'italian', 
    'czeski': 'czech', 
    'chorwacki': 'croatian', 
    'słowacki': 'slovak', 
    'niderlandzki': 'dutch' 
}

# Replace values in the 'language' column
df['language'] = df['language'].map(language_mapping)
# Drop rows with any missing values
df = df.dropna()
print(df)
# Display the number of rows after dropping NaN values
num_rows = df.shape[0]
print("Number of rows after dropping NaN values:", num_rows)

# Text data preprocessing for 'book_title' and 'description'
def clean_and_tokenize(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Tokenize the words
    tokens = word_tokenize(text)
    
    return tokens

# Clean and tokenize the 'book_title' column
df['cleaned_title'] = df['book_title'].apply(clean_and_tokenize)

# Clean and tokenize the 'description' column
df['cleaned_description'] = df['description'].apply(clean_and_tokenize)

# Display the cleaned and tokenized columns
print("\nCleaned and tokenized 'book_title' column:")
print(df['cleaned_title'])

print("\nCleaned and tokenized 'description' column:")
print(df['cleaned_description'])
num_rows = df.shape[0]
print("Number of rows:", num_rows)