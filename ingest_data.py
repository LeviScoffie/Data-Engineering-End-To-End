
import pandas as pd
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import psycopg2

import os

from time import time

import argparse


def main(params):

    user= params.user
    password= params.password
    host= params.host
    port= params.port
    db= params.db
    table_name= params.table_name
    url= params.url

    csv_name = "output.csv"

    # download csv
    url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
    os.system(f"wget {url} -O {csv_name}")
    # conn = psycopg2.connect(database="taxi_ny", user="root" ,password="root", host="/tmp")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
  


    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    # First we create a table with the column_names and instert the rows bit by bit

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


# Now we do it for the rows and if exists, meaning if there other rows just add onto the rows thus appeend.
# Use the magic command to time it
# Create a Loop for the operation

    while True:
        t_start = time()
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk..., took %.3f seconds' % (t_end-t_start))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name,table name,url of csv
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where we will write results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
