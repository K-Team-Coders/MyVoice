import os
import time

import psycopg2
import numpy as np
from loguru import logger
from fastapi import FastAPI, Response, File, UploadFile, Query
from fastapi.responses import JSONResponse  
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import Any, List
from transformers import AutoTokenizer, AutoModel
from sklearn.cluster import KMeans,MeanShift,DBSCAN,MiniBatchKMeans,AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity


# ml features
from ml.tone import tone
from ml.t9 import t9
from ml.services import get_text, get_bert_embeddings

# Initial code
# Database connection setup

conn = 0
cur = 0

logger.debug("Waiting for DB service Up...")
time.sleep(20)

try:     
    HOST=os.environ.get("DB_HOST")
    PORT=os.environ.get("PORT")
    DBNAME=os.environ.get("POSTGRES_DB")
    USER=os.environ.get("POSTGRES_USER")
    PASSWORD=os.environ.get("POSTGRES_PASSWORD")

    logger.success(('Docker DB connection started \n', HOST, PORT, DBNAME, USER, PASSWORD, ' - env variables!'))

    conn = psycopg2.connect(
        dbname=DBNAME, 
        host=HOST, 
        user=USER, 
        password=PASSWORD, 
        port=PORT)

    cur = conn.cursor()

    logger.success('Docker DB connected!')

except Exception as e:
    logger.error(f'Docker DB connect failed \n {e}!')

# Clusterisation models preset
model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Tables list output with question for FRONTEND COMBOBOX
@app.get("/tableslist")
def tableslist():
    cur.execute("""SELECT * FROM tables_list""")
    data = cur.fetchall()
    result = []
    for index, subdata in enumerate(data):
        table_id = data[0]
        table_head_question = data[1]

        result.append({
            'table_id': table_id,
            'table_head_question': table_head_question
        })

    return result

# Answer model for POST
class Answer(BaseModel):
    usertext: str

# Single answer processing (tone (+), censor (-), t9 (-), cluster! (-))
@app.post("/answer")
def answerProcessing(item: Answer):
    logger.debug(f"Answer is --- {item.usertext}")

    scores = tone(item.usertext)
    t9_correction = t9(item.usertext)

    result = {
        "positive": scores['pos'],
        "neutral": scores['neu'],
        "negative": scores['neg'],
        "t9": t9_correction["t9_corretion"]
    }

    logger.success(result)

    return JSONResponse(content=result)

# JSON files processing (filtering --> database)
@app.post("/files")
def filesProcessing(file: UploadFile):
    logger.debug(file.filename)
    data = file.file.read()
    logger.debug(data)
    return Response(status_code=201)

@app.post("/clusters")
def get_s_text(text: List[str] = Query(None)):

    res=[]
    # bac_req={}
    for i in range(0,len(text)):
        res.append(get_text(text[i]))
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

    return clusters
