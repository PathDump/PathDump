#!flask/bin/python
from flask import Flask
from flask import make_response
from flask import abort
from flask import request
import pathdumpapi as pdapi
import json
import sys
# import mapreduce as mr

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World" 


@app.route('/mapreduce',methods=['POST'])
def getmapreducepost():
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
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
        else:
            abort (404)

        # content=mr.distquery(request.json)
        # return content

@app.route('/mapreduce',methods=['GET'])
def getmapreduceget():
    # MLEE: parsing of request should be done here
    #       then, correct API should be called
    #
    #       request json format example 1
    #       {'api': 'execQuery'}
    #       {'tree': {...}}
    #       {'query': {'path': '/var/opt/pathdump/apps/topk.py',
    #                  'argv': [1000]}}
    #       {'aggcode': {'path': '/var/opt/pathdump/apps/topk_agg.py',
    #                  'argv': [1000]}}
    #
    #       request json format example 2
    #       {'api': 'installQuery'}
    #       {'tree': {...}}
    #       {'query': {'path': '/var/opt/pathdump/apps/topk.py',
    #                  'argv': [1000]}}
    #       {'interval': 0.1}
    #
    #       request json format example 3
    #       {'api': 'uninstallQuery'}
    #       {'querypath': '/var/opt/pathdump/apps/topk.py'}
    if not request.json or not 'api' in request.json:
        abort (404)
    else:
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

        # content=mr.distquery(request.json)
        # return content


if __name__ == '__main__':
    hostname=sys.argv[1]
    print "I am ",hostname
    app.run(debug=True,host="0.0.0.0")
