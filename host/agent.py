from flask import Flask
from flask import make_response
from flask import abort
from flask import request
from threading import Thread
import json
import sys
import os
import helperapi as helper
import confparser as cp

query_results = []

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World" 


@app.route('/pathdump', methods=['POST'])
def getpathdumppost():
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
        output = handleRequest (request.json)
        return json.dumps (output)

@app.route('/pathdump', methods=['GET'])
def getpathdumpget():
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
        output = handleRequest (request.json)
        return json.dumps (output)

def handleRequest (req):
    global query_results

    Tree = req['tree']
    cur = helper.getCurNodeID ()
    if len (Tree[cur]['child']) == 0:
        return helper.handleLeafNode (req)

    # From now on, the following handles when the current node is a relay node
    workers = []
    # 1) create a worker thread at the current node
    (func, argv) = helper.getThreadArgument (True, req)
    t = Thread (target = helper.wrapper, args = (func, argv, query_results))
    workers.append (t)

    # 2) deliver query to child nodes
    for child in Tree[cur]['child']: 
        (func, argv) = helper.getThreadArgument (False, req, child)
        # further optimization (should be implemented): construct a subtree for
        # each child and pass it on to the httpcmd as argument
        t = Thread (target = helper.wrapper, args = (func, argv,
                                                     query_results))
        workers.append (t)

    # 3) start workers
    for worker in workers:
        worker.start()

    # 4) wait unitl workers finish -> this part might be hung forever
    for worker in workers:
        worker.join()

    data=[]
    for res in query_results:
        if len(res) > 0 and type(res) == type(()) and 'content-type' in res[0]:
            resp, content = res
            content = json.loads (content)
        else:
            content = res
        data += content
    # reset variables 
    query_results = []

    if req['api'] == 'execQuery' and 'aggcode' in req:
        # 4) process collected data using AggCode
        return helper.processCollectedData (req['aggcode'], data)
    else:
        return data

def initialize ():
    options = None
    if len (sys.argv) == 2:
        options = cp.parse_config (sys.argv[1])
    if options:
        cp.options = options
    print cp.options

    # create app repository if it doesn't exist
    if not os.path.exists (cp.options['repository']):
        os.makedirs (cp.options['repository'])

    if 'controller' not in cp.options:
        sys.exit ("No controller IP address!")

if __name__ == '__main__':
    initialize ()
    app.run (debug = True, host = "0.0.0.0")
