import pandas as pd
import simplemma
#import re
from nltk.tokenize import RegexpTokenizer
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
#import string

with open('stopwords-iso.json', 'r', encoding='utf-8') as file:
    stopword_dict = json.load(file)

nltk.download('punkt')
#nltk.download('stopwords')
#print(stopwords.fileids())

file_path = 'final_combined_data copy.csv'
df2 = pd.read_csv('unique_rows_file2.csv')
df = pd.read_csv(file_path)
#num_rows = df.shape[0]
#print("Number of rows:", num_rows)
df = df[~df['language'].isin(['kaszubski', 'esperanto','białoruski', 'japoński', 'łaciński', 'ukraiński'])]

indices_to_exclude = [11347, 10423, 15063, 15246, 15112, 14504, 11995, 10911, 2974, 988, 1074, 15313, 14107, 8947, 16783, 16742, 15471, 15332, 14678, 14370, 14247, 13873, 8504, 7036, 6609, 6407, 5967, 5358, 5581, 5719, 5847, 4953, 4944, 4573, 4565, 3818, 3679, 2310, 2868, 6051, 6358, 6536, 7450, 7625, 8149, 13853, 13860, 589, 784, 918, 1252, 1356, 1725, 1954, 2290, 2518, 2848, 2994, 3329, 3667, 3913, 4259, 4668, 5107, 5109, 5566, 5582, 6945, 6946, 6958, 7049, 8128, 8136, 8142, 8147, 6995]  # Replace with the indices you want to exclude
#num_rows = df.shape[0]
#print("Number of rows:", num_rows)

df = df.drop(indices_to_exclude)
#num_rows = df.shape[0]
#print("Number of rows:", num_rows)

df = pd.concat([df, df2], ignore_index=True)
#num_rows = df.shape[0]
#print("Number of rows:", num_rows)
language_mapping = {
    'polski': 'pl', 
    'angielski': 'en',
    'niemiecki': 'de',
    'rosyjski': 'ru',
    'francuski': 'fr',
    'szwedzki': 'sv',
    'hiszpański': 'es', 
    'norweski': 'no', 
    'włoski': 'it', 
    'czeski': 'cs', 
    'chorwacki': 'hr', 
    'słowacki': 'sk', 
    'niderlandzki': 'nl' 
}


df['language'] = df['language'].map(language_mapping)


num_rows = df.shape[0]
print("Number of rows after dropping NaN values:", num_rows)

def clean_and_tokenize(text, language):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(str(text).lower())
    stop_words = stopword_dict.get(language, [])
    tokens = [word for word in tokens if word not in stop_words]
    if language == 'eng':
        lemmatized_tokens = [simplemma.lemmatize(token, lang='en') for token in tokens]
        print(lemmatized_tokens)
    else:
        lemmatized_tokens = [simplemma.lemmatize(token, lang=(language,'en')) for token in tokens]
        print(lemmatized_tokens)
    return lemmatized_tokens

df['cleaned_title'] = df.apply(lambda row: clean_and_tokenize(row['book_title'], row['language']), axis=1)

df['cleaned_description'] = df.apply(lambda row: clean_and_tokenize(row['description'], row['language']), axis=1)

print("Cleaned and tokenized 'book_title' column:")
print(df['cleaned_title'])

print("\nCleaned and tokenized 'description' column:")
print(df['cleaned_description'])
df = df.dropna()

df['combined_text'] = (2 * df['cleaned_title'].apply(lambda x: ' '.join(x)) +
                       df['cleaned_description'].apply(lambda x: ' '.join(x)))

df['page_count'] = df['page_count'].astype(int)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

mask = df['release_date'].dt.year.apply(lambda x: pd.notnull(x) and pd.isna(df['release_date'].dt.month.iloc[0]))
df.loc[mask, 'release_date'] = df['release_date'][mask].apply(lambda x: pd.to_datetime(str(int(x)) + '-01-01'))


output_file_path = 'data_for_measures2.csv'
df.to_csv(output_file_path, index=False)


