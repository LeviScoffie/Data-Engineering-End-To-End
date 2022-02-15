docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB=ny_taxi" \
    -v "/home/leviscoffie/Data-Engineering-End-To-End/week_1_basics_n_setup/2_docker_sql/2_docker_sql ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432
     postgres:13



#ny taxi website
https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page



## CREATE NETWORK

docker network create network-pg

# DOCKER CONTAINER FOR POSTGRES
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB=ny_taxi" \
    -v "/home/leviscoffie/Data-Engineering-End-To-End/week_1_basics_n_setup/2_docker_sql/2_docker_sql ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    --network=network-pg \
    --name database-pg \
     postgres:13

# DOCKER INSTANCE FOR PGADMIN
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=network-pg \
  --name adminpg \
    dpage/pgadmin4

docker pull dpage/pgadmin4

# URL
URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
# MANUAL RUN OF DATA INGESTION(WITHOUT DOCKER)
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \ 
  --d=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}




python ingest_data.py --user=root  --password=root   --host=localhost  --port=5432 --d=ny_taxi --table_name=yellow_taxi_trips  --url=${URL}

## INGESTING DATA THROUGH CREATED PIPELINE INTO POSTGRES DATABASE
URL="http://192.168.100.198:8000/yellow_tripdata_2021-01.csv"

python ingest_data.py --user=root  --password=root   --host=localhost  --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips  --url=${URL}



## DOCKER IMAGE BUILD FOR INGESTING DATA INTO DATABASE
docker build -t taxi_ingest:v001 .


docker run -it  --network=pg-network taxi_ingest:v001 --user=root  --password=root   --host=pg-database2   --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips  --url=${URL}