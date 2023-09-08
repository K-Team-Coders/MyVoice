import os
from dotenv import load_dotenv

from loguru import logger
import psycopg2
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

conn = 0
cur = 0
dockerized = False

try:     
    IP=os.environ.get("IP")
    PORT=os.environ.get("PORT")
    DBNAME=os.environ.get("POSTGRES_DB")
    USER=os.environ.get("POSTGRES_USER")
    PASSWORD=os.environ.get("POSTGRES_PASSWORD")

    logger.success(('Docker DB connection started \n', IP, PORT, DBNAME, USER, PASSWORD, ' - env variables!'))

    conn = psycopg2.connect(
        dbname=DBNAME, 
        host=IP, 
        user=USER, 
        password=PASSWORD, 
        port=PORT)

    cur = conn.cursor()

    logger.success('Docker DB connected!')
    dockerized = True

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

@app.get("/home/")
def home():
    return Response(status_code = 200)

