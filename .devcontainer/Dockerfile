# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app

RUN apt-get update  \
    && pip3 install -r requirements.txt