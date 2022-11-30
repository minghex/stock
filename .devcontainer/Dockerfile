# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

RUN apt-get update  \
    && pip3 install tornado \
    && pip3 install akshare \
    && pip3 install xlsxwriter \
    && pip3 install openpyxl --upgrade