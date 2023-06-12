from flask import Flask, jsonify, request
import requests
from cassandra.cluster import Cluster, ConsistencyLevel
from datetime import datetime
import hazelcast


app = Flask(__name__)

cluster = Cluster(['cassandra'])
session = cluster.connect()

client = hazelcast.HazelcastClient(
cluster_name="logs" , cluster_members=["hazelcast"]
)

logging = client.get_list("cassandra_logs")

@app.route('/', methods=['GET', 'POST'])
def init():
    querry = ""
    if request.method == 'POST':
      page_id = int(str(request.data)[2:-1])
      querry = f"""SELECT review_body FROM tables.pages WHERE page_id={page_id}"""
    else:
        return "Please send POST requesr with page_id"
    domains = []
    result = []
    now = datetime.now()
    try:
        prepare = session.prepare(querry)
        prepare.consistency_level=ConsistencyLevel.LOCAL_ONE
        result = session.execute(prepare)
        logging.add({"time": str(now), "event" : querry})
    except Exception as e:
        logging.add({"time": str(now), "event" : str(e)})
        return {"message" : "Something went wrong. Try Again", "Exc" : str(e)}
    
    for row in result:
        domains.append(row.review_body)
    return jsonify(page=domains)


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
        num = int(num)
        size = logging.size().result()
        
        for i in range(size-1, -1, -1):
            ret_logs.append(logging.get(i).result())
    return jsonify(ret_logs)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)


