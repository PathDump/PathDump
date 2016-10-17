#!/usr/bin/python

from flask import Flask
from flask import make_response
from flask import abort
from flask import jsonify
from flask import request
import json
import processquery as pq 
import sys
import confparser as cp
import aggtree
import os
import shutil
import hashlib


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(404)
def not_found (error):
    return make_response (json.dumps ({'error': 'Not found'}), 404)

@app.route('/pathdump', methods=['POST'])
def getpathdumppost():
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
        content = pq.handlerequest (request.json, "pathdump")
        return content

@app.route('/pathdump', methods=['GET'])
def getpathdumpget():
    if not request.json or not 'api' in request.json:
        abort(404)
    else:
        content = pq.handlerequest (request.json, "pathdump")
        return content

def md5 (fname):
    hash_md5 = hashlib.md5()
    with open (fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update (chunk)
    return hash_md5.hexdigest()

def initialize ():
    if len (sys.argv) == 2:
        cp.parse_config (sys.argv[1])

    # create app repository if it doesn't exist
    directory = cp.options['home'] + '/' + cp.options['repository']
    if not os.path.exists (directory):
        os.makedirs (directory)
        shutil.copy ('retrieve_flow.py', directory + '/retrieve_flow.py')
        md5val = md5('retrieve_flow.py')
        md5file = directory + '/retrieve_flow.py.md5'
        with open (md5file, "w") as f:
            f.write (md5val + '\n')
        f.close()

    # create flowrecord collection directory if it doesn't exist
    directory = cp.options['home']+'/'+cp.options['collection']
    if not os.path.exists (directory):
        os.makedirs (directory)

    aggtree.buildGroupTree (cp.options['home']+'/'+cp.options['grouptree'])

if __name__ == '__main__':
    initialize ()
    app.run (debug = True, host = "0.0.0.0")

    # app.run (debug = True, host = "0.0.0.0", processes = 2)
