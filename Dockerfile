FROM --platform=linux/amd64 python:3.12.7-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py


RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]
