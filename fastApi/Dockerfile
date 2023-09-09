FROM python:3.10.7-alpine

COPY ./requirements.txt .

RUN [ "pip", "install", "--upgrade", "pip"]

RUN [ "pip", "install", "-r", "requirements.txt"]


COPY . .

EXPOSE 8082
