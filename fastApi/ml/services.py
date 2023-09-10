import pandas as pd

import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

import pandas as pd
import numpy as np
import spacy


from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
lst_stopwords = nltk.corpus.stopwords.words('russian')
lst_stopwords.extend(['…', '«', '»', '...','-','—'])
lst_stopwords = lst_stopwords[:29]
nlp = spacy.load('ru_core_news_sm')

from sklearn.cluster import HDBSCAN,AgglomerativeClustering,KMeans
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def clean_text(text):
    # приводим текст к нижнему регистру
    text = text.lower()
    # создаем регулярное выражение для удаления лишних символов
    regular = r'[\*+\#+\№\"\-+\+\=+\?+\&\^\.+\;\,+\>+\(\)\/+\:\\+]'
    # регулярное выражение для замены ссылки на "URL"
    regular_url = r'(http\S+)|(www\S+)|([\w\d]+www\S+)|([\w\d]+http\S+)'
    # удаляем лишние символы
    text = re.sub(regular, '', text)
    # заменяем ссылки на "URL"
    text = re.sub(regular_url, r'URL', text)
    # заменяем числа и цифры на ' NUM '
    #text = re.sub(r'(\d+\s\d+)|(\d+)',' NUM ', text)
    # удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    # возвращаем очищенные данные
    return text
 
# создаем список для хранения преобразованных данных 
# загружаем стоп-слова для английского языка
# инициализируем лемматайзер 
lemmatizer = WordNetLemmatizer()
snowball = PorterStemmer()
# для каждого сообщения text из столбца data['Message']
def restore_word(stemmed_word):
    synonyms = wordnet.synsets(stemmed_word)
    if synonyms:
        return synonyms[0].lemmas()[0].name()
    else:
        return stemmed_word

#for text in dataframe['responsibilities(Должностные обязанности)']:
def get_text(text):
    
    # cleaning 
    text = clean_text(text) 
    # tokenization
    text = word_tokenize(text)       
    # удаление стоп-слов
    text = [word for word in text if word not in lst_stopwords]     
    # лемматизация
    text=  [snowball.stem(w) for w in text]
    text = [lemmatizer.lemmatize(w) for w in text]
    # добавляем преобразованный текст в список processed_text
    
    return ' '.join(text)

def get_bert_embeddings(texts):
    embeddings = []
    for text in texts:
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            output = model(**tokens)
        embeddings.append(output.last_hidden_state.mean(dim=1).squeeze().numpy())
    return np.vstack(embeddings)