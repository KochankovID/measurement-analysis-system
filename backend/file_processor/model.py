import numpy as np
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder

from sklearn.ensemble import RandomForestClassifier
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
import re
import pickle


def clean_comment(text, vocab):
    regex = re.compile('[^а-яА-Я]')
    stemmer = SnowballStemmer("russian")
    text = [stemmer.stem(i) for i in regex.sub(' ', text.lower()).split()]
    check_vocab = lambda x: x if x in vocab else '[UNK]'
    text = ' '.join(list(map(check_vocab, text)))
    return text


def save_model(model, filename):
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename):
    return pickle.load(open(filename, 'rb'))


def predict(text):
    vocab = pickle.load(open('for_model/vocab', 'rb'))
    vectorizer = pickle.load(open('for_model/vectorizer', 'rb'))
    clf = pickle.load(open('for_model/clf', 'rb'))
    enc = pickle.load(open('for_model/enc', 'rb'))

    text = clean_comment(text, vocab)
    text = vectorizer.transform([text]).toarray()

    return enc.inverse_transform(clf.predict(text)[:, np.newaxis])[0, 0]