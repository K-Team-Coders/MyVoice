import uvicorn
from typing import Any, List
from fastapi import FastAPI, Query
from sklearn.cluster import KMeans,MeanShift,DBSCAN,MiniBatchKMeans,AgglomerativeClustering
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
from services import get_text,get_bert_embeddings
from loguru import logger
from metrics import  mbkmeans_clusters, censor_text

with open("words.txt", "r", encoding="utf-8") as file:
    censored_words = [line.strip() for line in file]

app = FastAPI()

model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# clusterer = AgglomerativeClustering()

@app.post("/api/clusters")
def get_s_text(text: List[str] = Query(None)):

    res=[]
    # bac_req={}
    for i in range(0,len(text)):
        res.append(censor_text(get_text(text[i]),censored_words))
    logger.debug(res)
    text_embeddings = get_bert_embeddings(res)

    # Вычисление матрицы попарных косинусных сходств
    cosine_matrix = cosine_similarity(text_embeddings)
    #вычисление оптима кластеров
    wcss = {}
    limit = int((len(text)//2)**0.9)

    for k in range(2,limit+1):
        model = KMeans(n_clusters=k)
        model.fit(1-cosine_matrix)
        wcss[k] = model.inertia_
    # Рассчитываем дифференциал значений
    differences = {k: abs(v - wcss[k - 1]) if k > 2 else 0 for k, v in wcss.items()}

    # Находим ключ с максимальным дифференциалом
    max_key = max(differences, key=differences.get)

    # Кластеризация с использованием HDBSCAN
    clusterer = KMeans(max_key)
    cluster_labels = clusterer.fit_predict(1 - cosine_matrix)
    logger.debug(int((len(text)//2)**0.8))
    logger.debug(cluster_labels)

    # Группировка текстов по кластерам
    clusters = {}
    for cluster_id in np.unique(cluster_labels):
        cluster_docs = np.array(res)[cluster_labels == cluster_id]
        clusters[f"Кластер {cluster_id}"] = cluster_docs.tolist()


    logger.debug(mbkmeans_clusters(1-cosine_matrix,max_key))




    return clusters
    

if __name__ == "__main__":
    # run app on the host and port
    # init_db()
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
     uvicorn.run("main:app", host="localhost", port=8000, reload=True)