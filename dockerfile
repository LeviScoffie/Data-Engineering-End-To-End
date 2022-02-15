<<<<<<< HEAD
FROM python:3.9.1

RUN apt-get install wget

RUN pip install pandas sqlalchemy psycopg2


WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python","ingest_data"] 
||||||| parent of f300649... my commit
=======
FROM python:3.9.1

RUN apt-get install wget

RUN pip install pandas sqlalchemy psycopg2


WORKDIR /app

COPY ingest_data.py ingest_data.py


ENTRYPOINT ["python","ingest_data"] 
>>>>>>> f300649... my commit
