import nltk
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

mustbestr = "Input must be a string"

Stemmer = PorterStemmer()
Lemmatizer = WordNetLemmatizer()

class nlp: 

    @staticmethod
    def tokenize(query):
        if not isinstance(query, str):
            raise Exception(mustbestr)

        return nltk.word_tokenize(query)

    @staticmethod
    def stem(query):
        if not isinstance(query, str):
            raise Exception(mustbestr)

        return Stemmer.stem(query.lower())

    @staticmethod
    def bag_of_words(query, vocabulary):
        tokens = nlp.clean_text(query)
        bow = [0] * len(vocabulary)
        for token in tokens:
            for i, word in enumerate(vocabulary):
                if word == token:
                    bow[i] = 1
        
        return np.array(bow)

    @staticmethod
    def word_embedding(query, vocabulary):
        embedded = [[one_hot(query, len(vocabulary))]]
        return pad_sequences(embedded, maxlen=len(vocabulary), padding='post')

    @staticmethod
    def clean_text(text):
        if not isinstance(text, list):
            text = nlp.tokenize(text)

        return [Lemmatizer.lemmatize(token.lower()) for token in text]

    @staticmethod
    def lemmatize(text):
        return Lemmatizer.lemmatize(text)
        