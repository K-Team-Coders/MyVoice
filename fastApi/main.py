import os
import time

import psycopg2
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ml features
from ..ml.tone import tone

# Initial code
# Database connection setup

conn = 0
cur = 0

logger.debug("Waiting for DB service Up...")
time.sleep(10)

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

@app.post("/")
def root():
    return {"message": "Hello World"}
