from kafka import KafkaProducer
from cassandra.cluster import Cluster
from datetime import datetime
from urllib.request import urlopen
import json
import requests
import psycopg2

cluster = Cluster(['cassandra'])
session = cluster.connect()

session.execute("""CREATE KEYSPACE IF NOT EXISTS tables WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };""")

session.execute("""CREATE TABLE IF NOT EXISTS tables.pages (
                    page_id int,
                    review_body text,
                    PRIMARY KEY (page_id) 
                    );""")

# producer = KafkaProducer(bootstrap_servers=['kafka:29092'],value_serializer=lambda v: json.dumps(v).encode('utf-8'))


conn = psycopg2.connect(dbname='default_database', user='postgres', 
                        password='postgres', host='database')


url = 'https://stream.wikimedia.org/v2/stream/page-create'
r = requests.get(url, stream=True)

# def acked(err, msg):
#     if err is not None:
#         print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
#     else:
#         print("Message produced: %s" % (str(msg.value)))


timestamp = 0
mes = 0
for line in r.iter_lines():
    if line:
        #print(line)
        if "id" == str(line)[2:4]:
            st = line[4:]
            idstr = json.loads(st)
            timestamp = idstr[0]["timestamp"]
            mes = 1
        if mes == 1 and "data" == str(line)[2:6]:
            cursor = conn.cursor()

            st = line[6:]
            
            datastr = json.loads(st)
            if "user_id" not in  datastr["performer"].keys():
                timestamp = 0
                mes = 0
                continue
            to_add = {}
            to_add["timest"] = int((int(timestamp)/1000) // 1)
            
            to_add["uri"] = datastr["meta"]["uri"]
            to_add["domain"] = datastr["meta"]["domain"]
            to_add["page_id"] = datastr["page_id"]
            to_add["page_title"] = datastr["page_title"]
            to_add["user_text"] = datastr["performer"]["user_text"]
            to_add["user_is_bot"] = datastr["performer"]["user_is_bot"]
            to_add["user_id"] = datastr["performer"]["user_id"]
            print("put")
            uri = datastr["meta"]["uri"].replace("'", "\'")#.replace('%', '\%').replace("'", "\'").replace("_", "\_")
            domain = datastr["meta"]["domain"].replace("'", "\'")#.replace('%', '\%').replace("'", "\'").replace("_", "\_")
            title = datastr["page_title"].replace("'", "\'")#.replace('%', '\%').replace("'", "\'").replace("_", "\_")
            name = datastr["performer"]["user_text"].replace("'", "\'")#.replace('%', '\%').replace("'", "\'").replace("_", "\_")
            
            #print(to_add["timest"])
            #print(timestamp)
            dt = datetime.fromtimestamp(to_add["timest"])
            querry = f"""
                INSERT INTO main_table 
                VALUES (
                '{str(dt)}',
                '{uri}',
                '{domain}',
                {datastr["page_id"]},
                '{title}',
                '{name}',
                {datastr["performer"]["user_is_bot"]},
                {datastr["performer"]["user_id"]});
                """
            f = urlopen(uri)
            myfile = str(f.read())[2:-1]
            cassandra_query = f"""
                INSERT INTO tables.pages (page_id, review_body)
                VALUES ({datastr["page_id"]}, 
                $${myfile}$$);
            """
        
            try:
                cursor.execute(querry)
                conn.commit()
                #producer.send("dataflow", to_add)
            except:
                conn.rollback()
                print("False querry:")
                print(querry)
        
            try:
                session.execute(cassandra_query)
            except Exception as e:
                print("False querry:")
                print(cassandra_query)
                print(e)
            cursor.close()
            timestamp = 0
            mes = 0

conn.close()

# producer.produce("test", key="key", value="value", callback=acked)

# # Wait up to 1 second for events. Callbacks will be invoked during
# # this method call if the message is acknowledged.
# producer.poll(1)