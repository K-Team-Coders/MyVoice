import psycopg2
import os

from dotenv import load_dotenv
load_dotenv('DB.ENV')

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DBNAME = os.getenv("DBNAME")

connection = psycopg2.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    dbname=DBNAME
)

cursor = connection.cursor()

# Добавление отношение dronecnas
cursor.execute("""
CREATE TABLE public.dronescnas
    (
        name text,
        country text,
        range_ double precision,
        params json,
        PRIMARY KEY (name, country, range_)
    );

ALTER TABLE IF EXISTS public.dronescnas
    OWNER to postgres;
""")
connection.commit()

# Добавление отношения spiders
cursor.execute("""
CREATE TABLE public.spiders
    (
        spider text,
        url text,
        data text,
        PRIMARY KEY (spider, url, data)
    );

ALTER TABLE IF EXISTS public.spiders
    OWNER to postgres;
""")
connection.commit()

