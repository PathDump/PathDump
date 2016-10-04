import os
import imp
from bson import json_util
import json
import restapi
import netifaces as ni
import confparser as cp
import pathdumpapi as pdapi
from threading import Thread
import time
import socket
import zmq

cwd = os.getcwd()
subsURL = "tcp://localhost:5556"
subsFilter = "TIB "
subsQueries={}
subsSocket=None
instQueries = {}

def buildFlowidFilter (flowID):
    sip_filter = ''
    sport_filter = ''
    dip_filter = ''
    dport_filter = ''
    proto_filter = ''

    if 'sip' in flowID and flowID['sip'] != "*":
        sip_filter = {'sip' : flowID['sip']}

    if 'sport' in flowID and flowID['sport'] != "*":
        sport_filter = {'sport' : flowID['sport']}

    if 'dip' in flowID and flowID['dip'] != "*":
        dip_filter = {'dip' : flowID['dip']}

    if 'dport' in flowID and flowID['dport'] != "*":
        dport_filter = {'dport' : flowID['dport']}

    if 'proto' in flowID and flowID['proto'] != "*":
        proto_filter = {'proto' : flowID['proto']}

    return (sip_filter, sport_filter, dip_filter, dport_filter, proto_filter)

def buildLinkFilter (linkID):
    link_filter = '' 
    link = ''
    if linkID[0] != "*" and linkID[1] != "*":
        link = linkID[0] + "-" + linkID[1]
        link_filter = {'path': link}
    elif linkID[0] == "*" and linkID[1] == "*":
        link_filter = '' # DO NOTHING
    elif linkID[0] == "*":
        link = '[0-9]+' + "-" + linkID[1]
        link_filter = {'path': {"$regex": link}}
    else:
        link = linkID[0] + "-" + '[0-9]+'
        link_filter = {'path': {"$regex": link}}

    return link_filter

def buildTimeFilter (timeRange):
    stime_filter = ''
    etime_filter = ''

    if timeRange[0] != "*":
        stime_filter = {'start' : {'$gte' : timeRange[0]}}

    if timeRange[1] != "*":
        etime_filter = {'end' : {'$lte' : timeRange[1]}}

    return (stime_filter, etime_filter)

def buildPathFilter (path):
    path_filter = ''
    if len (path) != 0:
        path_filter = {'path': {'$all': path}}

    return path_filter

def doAndFilters (filters):
    # format: {'$and' : [{}, {}]
    ret_fltr = {'$and': []}
    for fltr in filters:
        if fltr != '':
            ret_fltr['$and'].append (fltr)

    nelem = len (ret_fltr['$and'])
    if nelem == 0:
        return ''
    elif nelem == 1:
        return ret_fltr['$and'][0]
    else:
        return ret_fltr

# returns an IP address as Node ID
def getCurNodeID ():
    return socket.gethostname() 
    #return ni.ifaddresses('eth0')[2][0]['addr']

def wrapper (func, args, results):
    results.append (func (*args))

def initializeSubscription():
    global subsSocket,subsURL,subsFilter
    
    if subsSocket == None:
        #  Socket to subscribe for flow records
        context = zmq.Context()                                                                      
        subsSocket = context.socket(zmq.SUB)
        subsSocket.connect(subsURL)                          
        fltr=subsFilter
        # Python 2 - ascii bytes to unicode str
        if isinstance(fltr, bytes):
            fltr = fltr.decode('ascii')
        print("Collecting flow stats host agent",subsURL,fltr)
        subsSocket.setsockopt_string(zmq.SUBSCRIBE, fltr)

def execSubsQueries(argv):
    global subsQueries,subsSocket,instQueries
    for qname in subsQueries.keys():
        if qname in instQueries and instQueries[qname]:
            runQuery(subsQueries[qname], argv)
        else:
            del subsQueries[qname]
            del instQueries[qname]
            if len(subsQueries)==0:
                print "NO queries subscribed for flows. Closing socket"
                subsSocket.close()
                subsSocket=None

def listenRecords(filter_str):
    while True and len(subsQueries) > 0:
        print "listening for records"
        msg = subsSocket.recv_string() 
        flow_record = json.loads(msg[len(filter_str):])  
        execSubsQueries(flow_record)

def runQuery(source, argv):
    filepath = cp.options['repository'] + '/' + source['name']
    module = imp.load_source ('', filepath)
    # module must implement 'run' function
    return module.run (argv)

def processTIB (source, collection):
    filepath = cp.options['repository'] + '/' + source['name']
    module = imp.load_source ('', filepath)
    # module must implement 'run' function
    return module.run (source['argv'], collection)

def processCollectedData (source, data):
    filepath = cp.options['repository'] + '/' + source['name']
    module = imp.load_source ('', filepath)
    # module must implement 'run' function
    return module.run (source['argv'], data)

def httpcmd (node, req):
    return restapi.post (node, json.dumps (req, default=json_util.default), "pathdump")

def checkSource (name, checksum):
    filepath = cwd + '/' + cp.options['repository'] + '/' + name
    md5fpath = filepath + '.md5'
    try:
        with open (md5fpath, 'r') as f:
            chksum = f.read()
        if not os.path.exists (filepath) or chksum != checksum:
            return [{getCurNodeID(): False}]
        else:
            return [{getCurNodeID(): True}]
    except IOError:
        return [{getCurNodeID(): False}]

def saveSource (name, checksum, filedata):
    filepath = cwd + '/' + cp.options['repository'] + '/' + name
    md5fpath = filepath + '.md5'
    try:
        with open (filepath, 'w') as f:
            f.write (filedata)
        with open (md5fpath, 'w') as f:
            f.write (checksum)
        return [{getCurNodeID(): True}]
    except IOError:
        return [{getCurNodeID(): False}]

def schedQuery (qname, interval, func, args):
    global instQueries

    while qname in instQueries and instQueries[qname]:
        time.sleep (interval)
        if not instQueries[qname]:
            break
        result = func (*args)
        print result

    # remove query because uninstallQuery was executed
    if qname in instQueries:
        del instQueries[qname]

def installQuery (query, interval):
    global instQueries

    qname = query['name']

    # the query is already installed
    if qname in instQueries:
        return [{getCurNodeID(): False}]

    instQueries[qname] = True
    print "Installing query ",qname
    if interval > 0.0:
        t = Thread (target = schedQuery, args = (qname, interval, processTIB,
                                                 (query, pdapi.collection)))
        t.start()
    elif interval==0.0:
        # data should be a stream of TIB records being exported from memory
        subsQueries[qname]=query
        if len(subsQueries)==1:
            initializeSubscription()
            t = Thread (target=listenRecords, args =(subsFilter,))
            t.start()
    return [{getCurNodeID(): True}]

def uninstallQuery (qname):
    global instQueries

    # no need for tight synchronization, so no locking mechanism is implemented
    if qname in instQueries:
        instQueries[qname] = False
    print "Uninstalling query ",qname
    print "Current installed queries",instQueries

    return [{getCurNodeID(): True}]

def handleLeafNode (req):
    if req['api'] == 'execQuery':
        query    = req['query']
        return processTIB (query, pdapi.collection)
    elif req['api'] == 'check_source':
        name     = req['name'] 
        checksum = req['checksum'] 
        return checkSource (name, checksum)
    elif req['api'] == 'send_source':
        name     = req['name'] 
        checksum = req['checksum']
        filedata = req['file']
        return saveSource (name, checksum, filedata)
    elif req['api'] == 'installQuery':
        query    = req['query']
        interval = req['interval']
        return installQuery (query, interval)
    elif req['api'] == 'uninstallQuery':
        qname    = req['query']['name']
        return uninstallQuery (qname)

def getThreadArgument (local, req, node=None):
    if local:
        api = req['api']
        if api == 'execQuery':
            query   = req['query']
            return (processTIB, (query, pdapi.collection))
        elif api == 'check_source':
            name     = req['name']
            checksum = req['checksum']
            return (checkSource, (name, checksum))
        elif api == 'send_source':
            name     = req['name'] 
            checksum = req['checksum']
            filedata = req['file']
            return (saveSource, (name, checksum, filedata))
        elif req['api'] == 'installQuery':
            query    = req['query']
            interval = req['interval']
            return (installQuery, (query, interval))
        elif req['api'] == 'uninstallQuery':
            qname    = req['query']['name']
            return (uninstallQuery, (qname,))
    else:
        return (httpcmd, (node, req))
