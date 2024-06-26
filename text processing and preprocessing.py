# -*- coding: utf-8 -*-
"""Text Processing and Preprocessing (NLP).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fXmjD5pmG5VoqmZUZPUfRjR49ggrzZwT
"""

# mount the drive
from google.colab import drive
drive.mount('/content/drive')

#Investigate the directory
import os.path
import os

os.chdir('/content/drive/My Drive/Colab Notebooks')

print("Current Working Directory " , os.getcwd())

#suppress warnings for a clean notebook
import warnings
warnings.filterwarnings('ignore')

#i select libraries
# Download NLTK data if not already downloaded
import nltk
import pandas as pd
import string
import collections
import matplotlib.cm as cm
import matplotlib.pyplot as pt

"""Task 1. Loading of the data into a Pandas dataframe

Data Source: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
"""

#Load
#df = pd.read_csv('spham.csv') error: UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 606-607: invalid continuation byte
try:
    df = pd.read_csv('spham.csv', encoding='latin1')
except UnicodeDecodeError:
    try:
        df = pd.read_csv('spham.csv', encoding='iso-8859-1')
    except UnicodeDecodeError:
        df = pd.read_csv('spham.csv', encoding='cp1252')

# Display the dataframe
print(df.head())

#Invesigate data
# Find out how many rows are in the dataframe
num_rows = df.shape[0]
print(f'The number of rows in the dataframe is: {num_rows}')

# Find out how many rows are labeled as 'spam' and 'not spam'
spam_count = df[df['v1'] == 'spam'].shape[0]
not_spam_count = df[df['v1'] == 'ham'].shape[0]

print(f'The number of rows labeled as spam is: {spam_count}')
print(f'The number of rows labeled as not spam is: {not_spam_count }')

# Count the number of NaN values in each column
nan_counts = df.isna().sum()

print('Number of NaN values in each column:')
print(nan_counts)

"""Task 2.Tokenization into words OR AND
sentence
"""

nltk.download('punkt')

#import nltk, word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize # this line is iport it initializes stuff
data = df

#word Tokenization

if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(word_tokenize)

    # Display the tokenized words
    print(df[['v2', 'tokenized_v2']].head())
else:
    print("The 'v2' column does not exist in the dataframe.")

from nltk.tokenize import sent_tokenize, word_tokenize
#Sentence Tokenization

if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(sent_tokenize)

    # Display the tokenized words
    print(df[['v2', 'tokenized_v2']].head())
else:
    print("The 'v2' column does not exist in the dataframe.")

"""3.  Normalization using stemming and lemmatization

a. stemming
*   removes prefixes and suffixes on a word to remain with only a stem, this increases accuracy



"""

from nltk.stem import PorterStemmer
# use lib creates stemming obj
ps = PorterStemmer()
# data is in a column named 'v2'
if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(word_tokenize)

    # Initialize the PorterStemmer
    ps = PorterStemmer()

    # Define a function to apply stemming to a list of words
    def stem_words(words):
        return [ps.stem(w) for w in words]

    # Apply the stemming function to the tokenized text
    df['stemmed_v2'] = df['tokenized_v2'].apply(stem_words)

    # Display the original, tokenized, and stemmed text
    print(df[['v2', 'tokenized_v2', 'stemmed_v2']].head())
else:
    print("The 'v2' column does not exist in the dataframe.")

"""b. lemmatization
*   It extracts a word as it would appear in the dictionary from a conjugated word .. etc
"""

nltk.download('omw-1.4')

nltk.download('wordnet')

# libraries
from nltk.stem import WordNetLemmatizer # installed wordnet above

# define obj
wl = WordNetLemmatizer()

# text data is in a column named 'text'
if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v'] = df['v2'].apply(word_tokenize)

    # Initialize the WordNetLemmatizer
    wl = WordNetLemmatizer()

    # Define a function to apply lemmatization to a list of words
    def lemmatize_words(words):
        return [wl.lemmatize(w) for w in words]

    # Apply the lemmatization function to the tokenized text
    df['lemmatized_v2'] = df['tokenized_v2'].apply(lemmatize_words)

    # Display the original, tokenized, and lemmatized text
    print(df[['v2', 'tokenized_v2', 'lemmatized_v2']].head())
else:
    print("The 'v2' column does not exist in the dataframe.")

#if 'v2' in df.columns:
  # Save the dataframe to a new CSV file
   # df.to_csv('lemmatized_spham.csv', index=False)
   # print("The DataFrame has been saved to 'lemmatized_spham.csv'.")
#else:
 #   print("The 'text' column does not exist in the dataframe.")

"""4. Stopword removal of common English words"""

nltk.download('stopwords')

from nltk.corpus import stopwords
#text data in v2
if 'v2' in df.columns:
        # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(word_tokenize)

    # Define the stopwords list
    stop_words = set(stopwords.words('english'))
    # Define a function to remove stopwords from a list of words
    def remove_stopwords(words):
        return [w for w in words if w.lower() not in stop_words]

    # Apply the remove_stopwords function to the lemmatized text
    df['cleaned_v2']= df['tokenized_v2'] .apply(remove_stopwords)

    # Display the original and cleaned text
    print(df[['v2', 'tokenized_v2', 'cleaned_v2']].head())

"""5. Part-of-Speech tagging on the tokenized text
*   defines the meaning of a sentence based on the context, extracts relations between words
"""

nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag
import nltk

# text data in v2
if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(word_tokenize)

       # Define the stopwords list
    stop_words = set(stopwords.words('english'))

    # Define a function to remove stopwords from a list of words in v2
    def remove_stopwords(words):
        return [w for w in words if w.lower() not in stop_words]

    # Apply the remove_stopwords function to the lemmatized text
    df['cleaned_v2'] = df['lemmatized_v2'].apply(remove_stopwords)

      # Define a function to apply POS tagging to a list of words
    def pos_tagging(words):
        return pos_tag(words)

    # Apply the POS tagging function to the cleaned text
    df['pos_tagged_v2'] = df['cleaned_v2'].apply(pos_tagging)

    # Display the original, tokenized, lemmatized, cleaned, and POS-tagged text
    print(df[['v2', 'cleaned_v2', 'pos_tagged_v2']].head())

"""6. Output the processed text, by combining processed text into a single string for each message
and saving the text in a new column in the dataframe.
"""

# Text data is in a column named 'V2'
if 'v2' in df.columns:
    # Tokenize the text data in each row
    df['tokenized_v2'] = df['v2'].apply(word_tokenize)

    # Initialize the WordNetLemmatizer
    wl = WordNetLemmatizer()

    # Define a function to apply lemmatization to a list of words
    def lemmatize_words(words):
        return [wl.lemmatize(w) for w in words]

    # Apply the lemmatization function to the tokenized text
    df['lemmatized_v2'] = df['tokenized_v2'].apply(lemmatize_words)

    # Define the stopwords list
    stop_words = set(stopwords.words('english'))

    # Define a function to remove stopwords from a list of words
    def remove_stopwords(words):
        return [w for w in words if w.lower() not in stop_words]

    # Apply the remove_stopwords function to the lemmatized text
    df['cleaned_v2'] = df['lemmatized_v2'].apply(remove_stopwords)

    # Define a function to apply POS tagging to a list of words
    def pos_tagging(words):
        return pos_tag(words)

    # Apply the POS tagging function to the cleaned text
    df['pos_tagged_v2'] = df['cleaned_v2'].apply(pos_tagging)

    # Combine the processed text into a single string for each message
    df['processed_v2'] = df['cleaned_v2'].apply(lambda words: ' '.join(words))

    # Display the original, tokenized, lemmatized, cleaned, and processed text
    print(df[['v2', 'tokenized_v2', 'lemmatized_v2', 'cleaned_v2', 'processed_v2']].head())

    # Save the dataframe to a new CSV file
    df.to_csv('processed_spham.csv', index=False)
    print("The DataFrame has been saved to 'processed_spham.csv'.")
else:
    print("The 'text' column does not exist in the dataframe.")

print("The END")
print("Created by Samwel Kibe")