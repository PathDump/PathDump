#!flask/bin/python
from flask import Flask
from flask import make_response
from flask import abort
from flask import jsonify
from flask import request
import json
import processquery as pq 
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)

@app.route('/mapreduce',methods=['POST'])
def getmapreducepost():
    if not request.json or not 'api' in request.json:
        abort(404)
    else:
        content=pq.handlerequest(request.json,"mapreduce")
        return content

@app.route('/mapreduce',methods=['GET'])
def getmapreduceget():
    if not request.json or not 'api' in request.json:
        abort(404)
    else:
        content=pq.handlerequest(request.json,"mapreduce")
        return content


if __name__ == '__main__':
    ip = "0.0.0.0"
    app.run(debug=True,host=ip)


