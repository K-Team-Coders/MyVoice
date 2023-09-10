import os
import time
import json
import collections
from dotenv import load_dotenv
load_dotenv('../DB.env')

import psycopg2
import numpy as np
from loguru import logger
from fastapi import FastAPI, Response, File, UploadFile, Query
from fastapi.responses import JSONResponse  
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from pydantic import BaseModel

from typing import Any, List
from transformers import AutoTokenizer, AutoModel
from sklearn.cluster import KMeans,MeanShift,DBSCAN,MiniBatchKMeans,AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity


# ml features
from ml.emoji import remove_emoji 
from ml.tone import tone # Sentiment analysis
from ml.t9 import t9 # T9 classic
from ml.transform import translate_with_en # Keyboard errors
from ml.result import translate_with_en as pure_text
from ml.services import get_text, get_bert_embeddings, get_text
from ml.metrics import  mbkmeans_clusters, censor_text

# Initial code
# Database connection setup

conn = 0
cur = 0

logger.debug("Waiting for DB service Up...")
time.sleep(5)

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

censored_words = 0
with open("ml/words.txt", "r", encoding="utf-8") as file:
    censored_words = [line.strip() for line in file]


# Receive actual tables list
def getTables():
    cur.execute("""SELECT * FROM tables_list""")
    data = cur.fetchall()
    result = []
    for index, subdata in enumerate(data):
        table_id = subdata[0]
        table_head_question = subdata[1]

        result.append({
            'table_id': table_id,
            'table_head_question': table_head_question
        })

    return result


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/export/{id_}")
def export(id_ : str):
    tables = getTables()
    # Identity check
    question = 0
    logger.debug(tables)
    identity_checker = False
    for index, data in enumerate(tables):
        if data['table_id'] == id_ :
            identity_checker = True
            question = data['table_head_question']
        else:
            pass

    if not identity_checker:
        return Response(status_code=400)
    else:
        try:
            cur.execute(f""" SELECT * FROM "%s" """, (int(id_),))
            data = cur.fetchall()
        except:
            conn.rollback()
            return Response(status_code=404)
    
        countsData = []
        clustarisationData = []
        positiveData = []
        neutralData = []
        negativeData = []
        t9Data = []
        rawAnswers = []
        for index, subdata in enumerate(data):
            logger.debug(subdata[0]) # answer
            logger.debug(subdata[1]) # count
            logger.debug(subdata[2]) # positive
            logger.debug(subdata[3]) # neutral
            logger.debug(subdata[4]) # negative
            logger.debug(subdata[5]) # t9

            clustarisationData.append(get_text(subdata[0]))
            rawAnswers.append(subdata[0])
            countsData.append(subdata[1])
            positiveData.append(subdata[2])
            neutralData.append(subdata[3])
            negativeData.append(subdata[4])
            t9Data.append(subdata[5])
        
        clustersData, metrics = Clustarisation(clustarisationData)
        logger.debug(metrics)
        logger.debug(clustersData)

        answers = []
        clusters_names = []
        for clusterName in clustersData:
            wordsInCluster = clustersData[clusterName]
                        
            maximum = 0
            maximumName = 'none'

            for wordInCluster in wordsInCluster:
                commonIndex = clustarisationData.index(wordInCluster)

                # gaining common data
                wordInClusterRaw = rawAnswers[commonIndex]
                wordInClusterCount = countsData[commonIndex]

                # naming costyl 
                if maximum < wordInClusterCount:
                    maximum = wordInClusterCount
                    maximumName = wordInClusterRaw

            clusters_names.append(maximumName)

        clusterIndex = 0
        for clusterName in clustersData:
            wordsInCluster = clustersData[clusterName]

            for word in wordsInCluster:
                commonIndex = clustarisationData.index(wordInCluster)

                # gaining common data
                wordInClusterRaw = rawAnswers[commonIndex]
                wordInClusterCount = countsData[commonIndex]
                wordErrors = t9Data[commonIndex]
                wordSentity = 0

                if neutralData[commonIndex] > abs(negativeData[commonIndex]) and neutralData[commonIndex] > positiveData[commonIndex]:
                    wordSentity = 'neutral'
                elif positiveData[commonIndex] > neutralData[commonIndex] and positiveData[commonIndex] > negativeData[commonIndex]:
                    wordSentity = 'positive'
                elif abs(negativeData[commonIndex]) > neutralData[commonIndex] and abs(negativeData[commonIndex]) > positiveData[commonIndex]:
                    wordSentity = 'negative'

                answers.append(
                    {
                        "answer": wordInClusterRaw,
                        "count": wordInClusterCount,
                        "cluster": clusters_names[clusterIndex],
                        "sentiment": wordSentity,
                        "userErrorsFixes": wordErrors
                    }
                )

        clusterIndex += 1

    result = {
        "question": question,
        "id": id_,
        "answers": answers,
    }

    with open(f"jsoned_{id_}.json", "wb") as f:
        f.write(json.dumps(result, indent=4))

    return FileResponse(f"jsoned_{id_}.json")


# Tables list output with question for FRONTEND
@app.get("/tableslist")
def tableslist():
    return JSONResponse({"result" : getTables()})

# View for adding new sentence in progress
@app.post("/processsentence")
def processsentence(sentence: str, id_: str):
    tables = getTables()
    
    # Identity check
    logger.debug(tables)
    
    identity_checker = False
    for index, data in enumerate(tables):
        if data['table_id'] == id_ :
            identity_checker = True
        else:
            pass

    if not identity_checker:
        return Response(status_code=400)
    else:
        try:
            cur.execute(f""" SELECT * FROM "%s" """, (int(id_),))
            data = cur.fetchall()
        except:
            conn.rollback()
            return Response(status_code=404)

        countsData = []
        rawAnswers = []
        for index, subdata in enumerate(data):
            logger.debug(subdata[0]) # answer
            logger.debug(subdata[1]) # count

            rawAnswers.append(subdata[0])
            countsData.append(subdata[1])


        newAnswer = pure_text(sentence)
        scores = 0
        try:
            scores = tone(sentence)
        except:
            scores = {'pos': 0.0, 'neu': 0.0, 'neg':0.0}
        
        positive = scores['pos']
        neutral =  scores['neu']
        negative = scores['neg']
        t9_text = newAnswer
            
        counts = 1
        if newAnswer in rawAnswers: 
            commonIndex = rawAnswers.index(newAnswer)
            counts = countsData[commonIndex] 
        elif sentence in rawAnswers:
            commonIndex = rawAnswers.index(sentence)
            counts = countsData[commonIndex] 

        try:
        # Add individual answer to new table
            cur.execute("""
                        INSERT INTO "%s" 
                            (answer, count, positive, neutral, negative, t9)
                        VALUES
                            (%s, %s, %s, %s, %s, %s)
                        """, (int(id_), sentence, counts, positive, neutral, negative, t9_text))
            conn.commit()
            # Я должен вернуть ему список всех айди и вопросов
            return JSONResponse(content=getTables(), status_code=201)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            cur.execute("""
                        UPDATE "%s" 
                        SET "count" = %s
                        WHERE "answer" = %s
                        """, (int(id_), counts+1, sentence)) 
            conn.commit()
            return JSONResponse(content=getTables(), status_code=202)


# Analisys for table by its id
@app.post("/tabledetailview/{id_}")
def tabledetailview(id_: str):
    tables = getTables()
    
    # Check for identity of tables
    headQuestion = 0
    identitity_checker = False
    for index, data in enumerate(tables):
        logger.debug(data["table_id"])
        if str(data["table_id"]) == id_:  
            identitity_checker = True
            headQuestion = data["table_head_question"]

    # Take data from files loading into DB
    if identitity_checker:
        cur.execute(f""" SELECT * FROM "%s" """, (int(id_),))
        data = cur.fetchall()

        countsData = []
        clustarisationData = []
        positiveData = []
        neutralData = []
        negativeData = []
        t9Data = []
        rawAnswers = []
        for index, subdata in enumerate(data):
            logger.debug(subdata[0]) # answer
            logger.debug(subdata[1]) # count
            logger.debug(subdata[2]) # positive
            logger.debug(subdata[3]) # neutral
            logger.debug(subdata[4]) # negative
            logger.debug(subdata[5]) # t9

            clustarisationData.append(get_text(subdata[0]))
            rawAnswers.append(subdata[0])
            countsData.append(subdata[1])
            positiveData.append(subdata[2])
            neutralData.append(subdata[3])
            negativeData.append(subdata[4])
            t9Data.append(subdata[5])
        
        clustersData, metrics = Clustarisation(clustarisationData)
        logger.debug(metrics)
        logger.debug(clustersData)

        result = {}

        totalPositive = 0
        totalNeutral = 0
        totalNegative = 0

        clusters = []
        for clusterName in clustersData:
            wordsInCluster = clustersData[clusterName]
            
            # Defining data to frontender
            wordsSentiment = []
            tagCloud = []

            numPositive = 0
            numNeutral = 0
            numNegative = 0
            
            maximum = 0
            maximumName = 'none'

            for wordInCluster in wordsInCluster:
                commonIndex = clustarisationData.index(wordInCluster)

                # gaining common data
                wordInClusterRaw = rawAnswers[commonIndex]
                wordInClusterCount = countsData[commonIndex]
                wordInClusterPositive = positiveData[commonIndex]
                wordInClusterNeutral = neutralData[commonIndex]
                wordInClusterNegative = negativeData[commonIndex]

                # naming costyl 
                if maximum < wordInClusterCount:
                    maximum = wordInClusterCount
                    maximumName = wordInCluster

                # sentiment analysis
                if wordInClusterPositive > abs(wordInClusterNegative) and wordInClusterPositive > wordInClusterNeutral:
                    totalPositive += 1
                    numPositive += 1
                elif abs(wordInClusterNegative) > wordInClusterPositive and abs(wordInClusterNegative) > wordInClusterNeutral:
                    totalNegative += 1
                    numNegative += 1
                elif wordInClusterNeutral > wordInClusterPositive and wordInClusterNeutral > abs(wordInClusterNegative):
                    totalNeutral += 1
                    numNeutral += 1

                # data gathering for tag cloud
                tagCloud.append([f"{wordInClusterRaw}", wordInClusterCount])
                
                # words sentiments in scope
                wordsSentiment.append({
                    "answer": wordInCluster,
                    "positive": wordInClusterPositive,
                    "neutral": wordInClusterNeutral,
                    "negative": wordInClusterNegative
                })
            
            clusters.append(
                {
                    "cluster_name": maximumName,
                    "tagCloud": tagCloud,
                    "numPositive": numPositive,
                    "numNeutral": numNeutral,
                    "numNegative": numNegative,
                    "wordsSentiment": wordsSentiment
                }
            )
        
        result_metrics = {
            "silhoute_all": str(metrics["silhoute_all"]),
            "inertial_all": str(metrics["Inertia_all"]),
        }

        result = {
            "metrics": result_metrics,
            "headQuestion": headQuestion,
            "totalPositive": totalPositive,
            "totalNeutral": totalNeutral,
            "totalNegative": totalNegative,
            "clusters": clusters
        }
            
    return JSONResponse({'result': result})

# Answer model for POST
class Answer(BaseModel):
    usertext: str

# Single answer processing (tone (+), censor (-), t9 (-), cluster! (-))
@app.post("/answer")
def answerProcessing(item: Answer):
    logger.debug(f"Answer is --- {item.usertext}")

    t9_correction = censor_text(pure_text(item.usertext), censored_words)
    scores = tone(remove_emoji(item.usertext))

    result = {
        "positive": scores['pos'],
        "neutral": scores['neu'],
        "negative": scores['neg'],
        "t9": t9_correction
    }

    logger.success(result)

    return JSONResponse(content=result)

# JSON files processing (filtering --> database)
@app.post("/files")
def filesProcessing(file: UploadFile = File(...)):
    tables = getTables()
    
    data = file.file.read()
    jsoned = json.loads(bytes.decode(data))

    # Identity check
    id_ = jsoned['id']
    question = jsoned['question']

    logger.debug(tables)
    
    identity_checker = False
    for index, data in enumerate(tables):
        if data['table_id'] == id_ and data["table_head_question"] == question:
            identity_checker = True
        else:
            pass

    if identity_checker:
        return Response(status_code=400)
    else:
        logger.debug(jsoned["answers"])
        data = jsoned["answers"]

        # Sign In Table in DB
        cur.execute("""
                    INSERT INTO tables_list
                        (table_id, table_head_question)
                    VALUES (%s, %s);
                        """, (id_, question))
        conn.commit()

        # Create new relation in DB
        cur.execute("""
                    CREATE TABLE "%s" 
                    (answer text, count integer, positive real, neutral real, negative real, t9 text, PRIMARY KEY (answer, count, positive, neutral, negative, t9));
                    """, (id_, ))
        conn.commit()
        
        # Data filling
        
        # Preprocess data identity error 
        result_answers = []
        for subdata in data:
            logger.debug(subdata)

            answer = subdata['answer']
            answer = remove_emoji(answer)

            logger.debug(answer)
            
            logger.debug(answer)

            result_answers.append(answer)

        logger.debug(result_answers)
        count = collections.Counter(result_answers)
        for subanswer in count: 

            logger.debug(count[subanswer])
            logger.debug(subanswer)

            counts = count[subanswer]
            
            pured = pure_text(subanswer)
            scores = 0
            try:
                scores = tone(subanswer)
            except:
                scores = {'pos': 0.0, 'neu': 0.0, 'neg':0.0}
            
            positive = scores['pos']
            neutral =  scores['neu']
            negative = scores['neg']
            t9_text = pured
            
            try:
            # Add individual answer to new table
                cur.execute("""
                            INSERT INTO "%s" 
                                (answer, count, positive, neutral, negative, t9)
                            VALUES
                                (%s, %s, %s, %s, %s, %s)
                            """, (id_, subanswer, counts, positive, neutral, negative, t9_text))
                conn.commit()
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                cur.execute("""
                            UPDATE "%s" 
                            SET "count" = %s
                            WHERE "answer" = %s
                            """, (id_, counts+1, subanswer)) 
                conn.commit()

    # Я должен вернуть ему список всех айди и вопросов
    return JSONResponse(content=getTables(), status_code=201)

def Clustarisation(text):
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
    limit = int((len(text)//2))

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

    metrics = mbkmeans_clusters(1-cosine_matrix,max_key)
    logger.debug(metrics)

    return clusters, metrics

# Clusterisation
@app.post("/clusters")
def get_s_text(text: List[str] = Query(None)):
    return JSONResponse({"data": Clustarisation(text)})
