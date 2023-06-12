from flask import Flask, jsonify, request, render_template
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/B_1', methods=['GET'])
def B_1():
    querry = """SELECT domain FROM main_table GROUP BY domain;"""

    postgress = json.loads(requests.post('http://relation_db:8080', data=querry).content.decode("utf-8"))
    return jsonify(str(postgress))

@app.route('/B_2', methods=['GET'])
def B_2():
    user_id = request.args.get('user_id')
    if user_id: 
        user_id = int(user_id)
        querry = f"""SELECT uri, page_id FROM main_table WHERE user_id={user_id};"""

        postgress = json.loads(requests.post('http://relation_db:8080', data=querry).content.decode("utf-8"))
        return jsonify(str(postgress))
    else:
        return jsonify(message='Please specify user_id')

@app.route('/B_3', methods=['GET'])
def B_3():
    domain = request.args.get('domain')
    if domain:
        querry = f"""SELECT COUNT(page_id) FROM main_table WHERE domain='{domain}';"""
        postgress = json.loads(requests.post('http://relation_db:8080', data=querry).content.decode("utf-8"))
        return jsonify(str(postgress))
    else:
        return jsonify(message='Please specify domain')

@app.route('/B_4', methods=['GET'])
def B_4():
    page_id = request.args.get('page_id')
    if page_id: 
        page_id = int(page_id)
        querry = f"""SELECT uri, user_id FROM main_table WHERE page_id={page_id};"""
        postgress = json.loads(requests.post('http://relation_db:8080', data=querry).content.decode("utf-8"))
        return jsonify(str(postgress))
    else:
        return jsonify(message='Please specify page_id')

@app.route('/B_5', methods=['GET'])
def B_5():
    start = request.args.get('start')
    end = request.args.get('end')
    if end and start: 
        querry = f"""SELECT t.user_id, t.user_text, COUNT(t.page_id) FROM (SELECT user_id, user_text, page_id FROM main_table WHERE timest BETWEEN timestamp '{start}' AND timestamp '{end}') AS t GROUP BY t.user_id, t.user_text;"""
        postgress = json.loads(requests.post('http://relation_db:8080', data=querry).content.decode("utf-8"))
        return jsonify(str(postgress))
    else:
        return jsonify(message='Please specify time range')


@app.route('/B_6', methods=['GET'])
def B_6():
    page_id = request.args.get('page_id')
    if page_id: 
        postgress = json.loads(requests.post('http://no_sql_db:8081', data=page_id).content.decode("utf-8"))
        return jsonify(str(postgress))
    else:
        return jsonify(message='Please specify page_id')
    
@app.route('/logging', methods=['GET'])
def loging():
    num = request.args.get('num')
    postgress = ""
    cassandra = ""
    if num:
        postgress = json.loads(requests.post(f'http://relation_db:8080/log?num={num}').content.decode("utf-8"))
        cassandra = json.loads(requests.post(f'http://no_sql_db:8081/log?num={num}').content.decode("utf-8"))
    else:
        postgress = json.loads(requests.post('http://relation_db:8080/log').content.decode("utf-8"))
        cassandra = json.loads(requests.post('http://no_sql_db:8081/log').content.decode("utf-8"))
    return jsonify(str({"postgress": postgress, "cassandra": cassandra}))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


