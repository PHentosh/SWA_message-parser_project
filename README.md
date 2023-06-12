## Start

To run project run ./run.sh in terminal. REST API is available at port 5000

To stop project run ./shutdown.sh it will decompose all docker files

## REST API

To access questions you should send HTTP request on coresponding address

API_A:
- 1 - http://localhost:5000/A_1
- 2 - http://localhost:5000/A_2

For API B there also some parameters you cam pass

API_B:
- 1 - http://localhost:5000/B_1
- 2 - http://localhost:5000/B_2?user_id=2345678
- 3 - http://localhost:5000/B_3?domain=commons.wikimedia.org
- 4 - http://localhost:5000/B_4?page_id=132898304
- 5 - http://localhost:5000/B_5?start=2023-6-10%2015:00:00&end=23-6-11%2015:00:00

## producer/read_stream.py

Code here demonstrates an example of data ingestion into Kafka using a Kafka producer. It fetches real-time data from the Wikimedia stream and inserts it into a PostgreSQL database. Here's how the code works:

## Dependencies

The code requires the following dependencies:

- `kafka-python` library for Kafka integration
- `datetime` library for working with timestamps
- `json` library for JSON serialization and deserialization
- `requests` library for making HTTP requests
- `psycopg2` library for working with PostgreSQL databases

Make sure you have these libraries installed before running the code.

## Kafka Producer Configuration

The code sets up a Kafka producer by importing the `KafkaProducer` class from the `kafka` module. It also imports the `socket` library to retrieve the hostname and uses it as the client ID for the producer. The `conf` dictionary specifies the Kafka bootstrap servers and the client ID.

## PostgreSQL Database Connection

The code establishes a connection to a PostgreSQL database using the `psycopg2` library. It provides the necessary connection details such as the database name, username, password, and host.

## Data Ingestion from Wikimedia Stream

The code fetches real-time data from the Wikimedia stream by making an HTTP GET request to the provided URL (`https://stream.wikimedia.org/v2/stream/page-create`). It uses the `requests` library to enable streaming of the response.

The code then iterates over the response content line by line. It checks each line for specific markers (`id` and `data`) to identify relevant data. Once the relevant data is found, it extracts the necessary information and prepares it for ingestion into Kafka and the PostgreSQL database.

## Data Transformation and Ingestion

For each relevant line of data, the code performs the following steps:

1. Extracts the necessary information from the JSON payload.
2. Constructs a dictionary (`to_add`) to hold the extracted data.
3. Escapes any special characters in the extracted strings.
4. Constructs an SQL query using the extracted data.
5. Executes the query using the PostgreSQL connection and commits the transaction.
6. Sends the extracted data to the Kafka topic named "dataflow" using the Kafka producer.

If any error occurs during the execution of the SQL query, the code rolls back the transaction and prints the query for debugging purposes.

## Dockerfile

Dockerfile sets up the necessary environment for running the data ingestion code. Here are the steps performed by the Dockerfile:

1. The base image is set to the latest version of Python.
2. The `kafka-python`, `datetime`, `requests`, and `psycopg2-binary` Python packages are installed using `pip`.
3. The `read_stream.py` file, containing the data ingestion code, is copied to the `/opt/app/` directory inside the Docker image.
4. The entrypoint of the Docker image is set to run the `read_stream.py` script using the Python interpreter.

## Cleanup

Once the data ingestion is complete or an error occurs, the code closes the PostgreSQL connection.


## Docker-compose

This YAML file provides a Docker Compose configuration for setting up a data pipeline environment. It describes the services required to build the pipeline and orchestrates their deployment using Docker containers. The configuration includes services such as Spark, ZooKeeper, Kafka, a producer, a database, and a RESTful API service.

## Networks

---

### D**atapipeline**

This network is created to connect the services within the data pipeline environment. It allows the services to communicate with each other.

## Services

---

### S**park**

This service uses the `bitnami/spark:3` Docker image to run Apache Spark in master mode. It is named "spark_master" and is set to restart automatically. The environment variables `SPARK_MODE` and various other Spark configuration variables are set to configure the Spark instance. It is connected to the `datapipeline` network and mounts the local directory `./spark` to the `/src` directory inside the container.

### Z**ookeeper**

This service uses the `confluentinc/cp-zookeeper:latest` Docker image to run Apache ZooKeeper, which is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and more. It is named "zookeeper" and exposes port 32181. The environment variables `ZOOKEEPER_CLIENT_PORT` and `ZOOKEEPER_TICK_TIME` configure the ZooKeeper instance. It is connected to the `datapipeline` network.

### K**afka**

This service uses the `confluentinc/cp-kafka:latest` Docker image to run Apache Kafka, which is a distributed event streaming platform. It is named "kafka" and exposes port 9092. It depends on the `zookeeper` service to be running. The environment variables configure the Kafka instance, including the broker ID, ZooKeeper connection, listener security protocol, advertised listeners, and more. It is connected to the `datapipeline` network.

### P**roducer**

This service builds an image from the `./producer` directory. It depends on the `kafka` service to be running. It is connected to the `datapipeline` network and has a link to the `database` service. It is set to restart automatically.

### D**atabase**

This service uses the `postgres:latest` Docker image to run a PostgreSQL database. It is named "database" and is set to restart automatically. The environment variables configure the database user, password, and default database name. It exposes port 5432 and is connected to the `datapipeline` network. Additionally, it mounts the local file `./postgres/create_tables.sql` to initialize the database with the provided SQL script.

### R**est_api**

This service builds an image from the `./REST_API_B` directory. It depends on the `database` service to be running. It exposes port 5000 and is connected to the `datapipeline` network. It is set to restart automatically.

All of the services are connected to the `datapipeline` network, which allows them to communicate with each other. They are set to restart automatically to ensure they are always running.

## create_tables.yml

Thia SQL file contains the schema definitions for three tables: `main_table`, `domains`, and `users`. These tables are designed to store data related to web pages, domains, and users in a structured manner. 

## `main_table`

| Column | Data Type |
| --- | --- |
| timest | timestamp |
| uri | varchar(2000) |
| domain | varchar(500) |
| page_id | INT |
| page_title | varchar(500) |
| user_text | varchar(500) |
| is_bot | BOOLEAN |
| user_id | INT |

## `domains`

| Column | Data Type |
| --- | --- |
| timestamp | BIGINT |
| domain | varchar(500) |
| number | INT |
| is_bot | BOOLEAN |


These representations outline the structure of each table and the corresponding data types for their respective columns.