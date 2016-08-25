#!flask/bin/python
from flask import Flask
from flask import make_response
from flask import abort
from flask import request
import pathdumpapi as pdapi
import json
import sys
import confparser as cp
import os

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World" 


@app.route('/pathdump',methods=['POST'])
def getpathdumppost():
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
        output = pdapi.handleRequest (request.json)
        return json.dumps (output)
        '''
        if request.json['api'] == 'execQuery':
            aggtree = request.json['tree']
            query   = request.json['query']
            aggcode = request.json['aggcode']
            print '\n\n\nPOST'
            print aggtree
            print '------'
            print query
            print '------'
            print aggcode
            output = pdapi.execQuery (aggtree, query, aggcode)
            return json.dumps (output)
        elif request.json['api'] == 'installQuery':
            aggtree = request.json['tree']
            query    = request.json['query']
            interval = request.json['interval']
            return pdapi.installQuery (aggtree, query, interval)
        elif request.json['api'] == 'uninstallQuery':
            aggtree = request.json['tree']
            query    = request.json['query']
            return pdapi.uninstallQuery (aggtree, query)
        elif request.json['api'] == 'check_source':
            aggtree = request.json['tree']
            name = request.json['name'] 
            checksum = request.json['checksum'] 
            output = helper.checkSource (aggtree, name, checksum)
            return json.dumps (output)    
        else:
            abort (404)
        '''

@app.route('/pathdump',methods=['GET'])
def getpathdumpget():
    # MLEE: parsing of request should be done here
    #       then, correct API should be called
    #
    #       request json format example 1
    #       {'api': 'execQuery'}
    #       {'tree': {...}}
    #       {'query': {'name': 'topk_query.py',
    #                  'argv': [1000]}}
    #       {'aggcode': {'name': 'topk_query_agg.py',
    #                  'argv': [1000]}}
    #
    #       request json format example 2
    #       {'api': 'installQuery'}
    #       {'tree': {...}}
    #       {'query': {'name': 'topk_query.py',
    #                  'argv': [1000]}}
    #       {'interval': 0.1}
    #
    #       request json format example 3
    #       {'api': 'uninstallQuery'}
    #       {'query': {'name': 'topk_query.py',
    #                  'checksum': 'eea7d80064c3c1d9374e2897ccd69a98'}}
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
        output = pdapi.handleRequest (request.json)
        return json.dumps (output)
        '''
        if request.json['api'] == 'execQuery':
            aggtree = request.json['tree']
            query   = request.json['query']
            aggcode = request.json['aggcode']
            print '\n\n\n'
            print aggtree
            print '------'
            print query
            print '------'
            print aggcode
            output = pdapi.execQuery (aggtree, query, aggcode)
            return json.dumps (output)
        elif request.json['api'] == 'installQuery':
            aggtree = request.json['tree']
            query    = request.json['query']
            interval = request.json['interval']
            return pdapi.installQuery (aggtree, query, interval)
        elif request.json['api'] == 'uninstallQuery':
            aggtree = request.json['tree']
            query    = request.json['query']
            return pdapi.uninstallQuery (aggtree, query)
        else:
            abort (404)
        '''

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

if __name__ == '__main__':
    initialize ()
    app.run(debug=True,host="0.0.0.0")
