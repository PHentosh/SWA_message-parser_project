docker-compose build 

docker-compose up -d


#docker exec -it spark_master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /src/spark_read.py