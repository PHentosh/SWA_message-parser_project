## Start

To run project run ./run.sh in terminal. REST API is available at port 5000

To stop project run ./shutdown.sh it will decompose all docker files

## REST API

To access questions you should send HTTP request on coresponding address

- 1 - Return the list of existing domains for which pages were created.
- 2 - Return all the pages which were created by the user with a specified user_id.
- 3 - Return the number of articles created for a specified domain.
- 4 - Return the page with the specified page_id
- 5 - Return the id, name, and the number of created pages of all the users who created at least one page in a specified time range. 
- 6 - Return the the page itself by pade_id 
- 7 - Return the last num of querrys that were send. If num not specified return all logs

REST_API:
- 1 - http://localhost:5000/B_1
- 2 - http://localhost:5000/B_2?user_id=2345678
- 3 - http://localhost:5000/B_3?domain=commons.wikimedia.org
- 4 - http://localhost:5000/B_4?page_id=132898304
- 5 - http://localhost:5000/B_5?start=2023-6-10%2015:00:00&end=23-6-11%2015:00:00
- 6 - http://localhost:5000/B_6?page_id=132898304
- 7 - http://localhost:5000/logging?num=4 

## producer/read_stream.py

It fetches real-time data from the Wikimedia stream and inserts it into a PostgreSQL database and Cassandra database. In Cassandra i put only page_id and the page itself, which i pull using python urllib

## Dependencies

The code requires the following dependencies:

- `datetime` library for working with timestamps
- `json` library for JSON serialization and deserialization
- `requests` library for making HTTP requests
- `flask` library for working with PostgreSQL databases
- `hazelcast-python-client` library for working with PostgreSQL databases
- `cassandra-driver` library for working with PostgreSQL databases

Make sure you have these libraries installed before running the code.

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
5. Pull the pade from url using urllib.
6. Executes the query using the PostgreSQL and Cassandra connection and commits the transaction.

If any error occurs during the execution of the SQL query, the code rolls back the transaction and prints the query for debugging purposes.

## Cleanup

Once the data ingestion is complete or an error occurs, the code closes the PostgreSQL connection.


## Docker-compose

This YAML file provides a Docker Compose configuration for setting up a datapipeline environment. It describes the services required to build the pipeline and orchestrates their deployment using Docker containers. The configuration includes services such as producer, a databases, hazelcast, and a RESTful API services.

## Networks

All servises are in one network: datapipeline. It allows the services to communicate with each other.

## Services


### P**roducer**

This service builds an image from the `./producer` directory. It depends on the `kafka` service to be running. It is connected to the `datapipeline` network and has a link to the `database` service. It is set to restart automatically.

### D**atabase**

This service uses the `postgres:latest` Docker image to run a PostgreSQL database. It is named "database" and is set to restart automatically. The environment variables configure the database user, password, and default database name. It exposes port 5432 and is connected to the `datapipeline` network. Additionally, it mounts the local file `./postgres/create_tables.sql` to initialize the database with the provided SQL script.


### R**est_api**

This service builds an image from the `./REST_API` directory. It depends on the `database` service to be running. It exposes port 5000 and is connected to the `datapipeline` network. It is set to restart automatically.

It responcible for all comunication user. It takes requert from user, forms a query and sents it to coresponding servise, wether it`s question to postgress database or cassangra.

### H**azelcast**

It`s hazelcast service, that starts hazelcast cluster, to store logs

### R**elation_db** and C**assandra**

Theese are servises to comunicate with databases. They recive requert by RESTfull API from REST_API container, execute query, parce results and return them.
Also thes logs all queries to Hazelcast.
If asked they can return nessesery logs. 


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