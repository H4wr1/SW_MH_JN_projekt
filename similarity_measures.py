from collections import defaultdict, Counter
import math
import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
#import simplemma
#from datetime import datetime
def calculate_tf(document):
    word_counts = Counter(document)
    max_frequency = max(word_counts.values())

    tf_values = {word: count / max_frequency for word, count in word_counts.items()}
    return tf_values

def calculate_idf(documents):
    word_count = defaultdict(int)
    num_documents = len(documents)
    idf_values = {}

    for doc in documents:
        unique_words = set(doc)  
        for word in unique_words:
            word_count[word] += 1

    for word, count in word_count.items():
        idf = math.log10(num_documents / count)
        idf_values[word] = idf

    return idf_values

def calculate_tf_idf(documents, idf_values):
    tf_idf_values = []

    for doc in documents:
        tf = calculate_tf(doc)
        tf_idf = {word: tf_value * idf_values[word] for word, tf_value in tf.items()}
        tf_idf_values.append(tf_idf)

    return tf_idf_values

def calculate_measures(query_text, page_count_min, page_count_max, release_date_min, release_date_max):
    df = pd.read_csv('data_for_measures9.csv')
    if page_count_min != "":
        df = df[df['page_count'] >= int(page_count_min)]

    if page_count_max != "":
        df = df[df['page_count'] <= int(page_count_max)]
   
    if release_date_min !="":
        df = df[df['release_date'] >= release_date_min]

    if release_date_max !="":
        df = df[df['release_date'] <= release_date_max]

    tokenizer = RegexpTokenizer(r'\w+')

    documents = df['combined_text'].apply(lambda x: tokenizer.tokenize(str(x).lower())).tolist()

    idf_values = calculate_idf(documents)
    tf_idf_values = calculate_tf_idf(documents, idf_values)

    tokenizer = RegexpTokenizer(r'\w+')
    query_tf = tokenizer.tokenize(str(query_text).lower())
    
    query_tf_idf = {word: query_tf.count(word) / len(query_tf) * idf_values.get(word, 0) for word in query_tf}
    results = []
    for count,doc_tf_idf in enumerate(tf_idf_values):

        result = []       
        sum_squared_tf_idf = sum(value ** 2 for word, value in doc_tf_idf.items() if word in query_tf) 

        if sum_squared_tf_idf != 0:
            iloczyn = sum(doc_tf_idf.get(word, 0) for word in query_tf if word in doc_tf_idf)
            result.append(round(iloczyn, 3))
            dice = (2 * iloczyn) / (4 * sum_squared_tf_idf)
            result.append(round(dice, 3))
            jaccard = iloczyn / (4 + sum_squared_tf_idf - iloczyn)
            result.append(round(jaccard, 3))
            cosinus = iloczyn / (math.sqrt(4) * math.sqrt(sum_squared_tf_idf))
            result.append(round(cosinus, 3))
            result.append(count)
            results.append(result) 

    sorted_books = sorted(results, key=lambda x: (x[3], x[2], x[1], x[0]), reverse=True)

    top_3_books = sorted_books[:5]
    for book in top_3_books:
        id_of_book = book[4]
        book.pop(4)
        book_info = df.iloc[id_of_book]
        book.append(book_info['book_title'])
        book.append(book_info['author_name'])
        book.append(book_info['release_date'])
        book.append(book_info['page_count'])
        book.append(book_info['book_link'])
        #book.pop(4)

        
    print(top_3_books)

        
    return top_3_books