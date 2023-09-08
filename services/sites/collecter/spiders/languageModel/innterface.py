import os
import re

import statistics
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from loguru import logger
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer, util

nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('punkt') # if necessary...
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
model = SentenceTransformer('blinoff/roberta-base-russian-v0')

def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and   characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()    
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text

def loadCosine():
    file_ = os.path.join(Path.cwd().joinpath('collecter').joinpath('spiders').joinpath('languageModel'), 'searchQuery.txt')
    with open( file_, 'r', encoding='utf-8') as f:
        list_ = f.read()
        return list_
        # Раскоммитить при использовании статистики 
        # stringer=list_.split('')
        # perem_list=[]
        # for i in range(len(stringer)):
        #     perem=utils_preprocess_text(stringer[i])
        #     perem_list.append(perem)
        # return perem_list


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

# Быстрее, но с аномалиями
def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words=stopwords.words('russian'))
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

# Дольше, но точнее
def stats_method(perem_list, text):
    metr=[]
    for item in perem_list:
        tzs=cosine_sim(item, text)
        metr.append(tzs)
    return statistics.mean(metr)

def model_method(shablon, text):
    encoded_text = model.encode(text)
    encoded_shablon = model.encode(shablon)
    result = util.pytorch_cos_sim(encoded_text, encoded_shablon)
    return result.item()
