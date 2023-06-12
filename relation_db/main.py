from flask import Flask, jsonify, request
import requests
from datetime import datetime
import hazelcast
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(dbname='default_database', user='postgres', 
                        password='postgres', host='database')
client = hazelcast.HazelcastClient(
    cluster_name="logs", cluster_members=["hazelcast"]
    )
logging = client.get_list("postgres_logs")

@app.route('/', methods=['GET', 'POST'])
def init():

    querry = ""
    if request.method == 'POST':
      querry = str(request.data)[2:-1]
    else:
        return "Please send POST requesr with query"
    cursor = conn.cursor()
    domains = []
    result = []
    now = datetime.now()
    try:
        cursor.execute(querry)
        result = cursor.fetchall()
        logging.add({"time": str(now), "event" : querry})
    except Exception as e:
        logging.add({"time": str(now), "event" : str(e)})
        cursor.execute("ROLLBACK")
        conn.commit()
        return {"message" : "Something went wrong. Try Again", "Exc" : str(e)}
    for row in result:
        if len(row) > 1:
            domains.append(row)
        else:
            domains += row
    cursor.close()
    return jsonify(result=domains)


@app.route('/log', methods=['GET', 'POST'])
def logs():
    num = request.args.get('num')
    ret_logs = []
    if num:
        num = int(num)
        size = logging.size().result()
        for i in range(size-1, size-num-1, -1):
            ret_logs.append(logging.get(i).result())
    else:
        size = logging.size().result()
        for i in range(size-1, -1, -1):
            ret_logs.append(logging.get(i).result())
    return jsonify(logs=ret_logs)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

conn.close()

