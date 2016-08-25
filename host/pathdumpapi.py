from pymongo import MongoClient
import pymongo
from datetime import datetime
from pprint import pprint 
import helperapi as helper
from copy import deepcopy
from threading import Thread
import imp
import json

client=MongoClient('localhost', 27017)
database=client['pathdump']
collection=database['TIB']

query_results = []

def getFlows (linkID, timeRange):
    # data_filter = {'paths': {'$elemMatch': {'path': linkexp}}}
    link_fltr = helper.buildLinkFilter (linkID)
    (stime_fltr, etime_fltr) = helper.buildTimeFilter (timeRange)
    data_fltr = helper.doAndFilters ([link_fltr, stime_fltr, etime_fltr])

    proj_fltr = {'sip': 1, 'sport': 1, 'dip': 1, 'dport': 1, 'proto': 1,
                 'path': 1, 'bytes': 1, 'pkts': 1, 'start': 1, 'end': 1,
                 '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)
    flows = []
    for f in cursor:
        flow = {'flowid': {}, 'path': None}
        flow['flowid']['sip'] = f['sip']
        flow['flowid']['sport'] = f['sport']
        flow['flowid']['dip'] = f['dip']
        flow['flowid']['dport'] = f['dport']
        flow['flowid']['proto'] = f['proto']
        flow['path'] = f['path']
        flow['bytes'] = f['bytes']
        flow['pkts'] = f['pkts']
        flow['start'] = (f['start'] - datetime(1970,1,1)).total_seconds()
        flow['end'] = (f['end'] - datetime(1970,1,1)).total_seconds()
        # pprint (flow)
        flows.append (flow)

    return flows

def getPaths (flowID, linkID, timeRange):
    (sip_fltr, sport_fltr, dip_fltr, dport_fltr, proto_fltr) = \
        helper.buildFlowidFilter (flowID)
    link_fltr = helper.buildLinkFilter (linkID)
    (stime_fltr, etime_fltr) = helper.buildTimeFilter (timeRange)
    data_fltr = helper.doAndFilters ([sip_fltr, sport_fltr, dip_fltr,
                                     dport_fltr, proto_fltr,
                                     stime_fltr, etime_fltr])

    proj_fltr = {'path': 1, '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)
    paths = []
    for path in cursor:
        pprint (path)
        paths.append (path)

    return paths

def getCount (Flow, timeRange):
    if Flow['bytes'] and Flow['pkts']:
        return (Flow['bytes'], Flow['pkts'])

    (sip_fltr, sport_fltr, dip_fltr, dport_fltr, proto_fltr) = \
        helper.buildFlowidFilter (Flow['flowid'])
    path_fltr = helper.buildPathFilter (Flow['path'])
    (stime_fltr, etime_fltr) = helper.buildTimeFilter (timeRange)
    data_fltr = helper.doAndFilters ([sip_fltr, sport_fltr, dip_fltr,
                                     dport_fltr, proto_fltr, path_fltr,
                                     stime_fltr, etime_fltr])

    # proj_fltr = {'bytes': 1, 'pkts': 1, 'path': 1, '_id': 0}
    proj_fltr = {'bytes': 1, 'pkts': 1, '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)

    bytec = 0 # byte count
    pktc  = 0 # packet count
    for c in cursor:
        # if helper.isSamePath (Flow['path'], c['path']) == True:
        bytec += c['bytes']
        pktc += c['pkts']

    # print bytec, pktc
    return (bytec, pktc)

def getDuration (Flow, timeRange):
    (sip_fltr, sport_fltr, dip_fltr, dport_fltr, proto_fltr) = \
        helper.buildFlowidFilter (Flow['flowid'])
    path_fltr = helper.buildPathFilter (Flow['path'])
    (stime_fltr, etime_fltr) = helper.buildTimeFilter (timeRange)
    data_fltr = helper.doAndFilters ([sip_fltr, sport_fltr, dip_fltr,
                                     dport_fltr, proto_fltr, path_fltr, 
                                     stime_fltr, etime_fltr])

    # proj_fltr = {'start': 1, 'end': 1, 'path': 1, '_id': 0}
    proj_fltr = {'start': 1, 'end': 1, '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)

    start = -1
    end = -1
    for c in cursor:
        # if helper.isSamePath (Flow['path'], c['path']) == True:
        if start == -1 or start > c['start']:
            start = c['start']
        if end == -1 or end <  c['end']:
            end = c['end']

    delta = end - start
    return delta.total_seconds()

def postFlow (flowID, Reason, Paths):
    return True

'''
def execQuery (Tree, Query, AggCode=None):
    global query_results

    cur = helper.getCurNodeID ()
    # if the current node is a leaf node, get data from database
    if len (Tree[cur]['child']) == 0:
        return helper.processTIB (Query, collection)

    # From now on, the following handles when the current node is a relay node
    workers=[]
    # 1) create a worker thread at the current node
    t = Thread (target = helper.wrapper,
                args = (helper.processTIB, (deepcopy(Query), collection,),
                        query_results))
    workers.append (t)

    # 2) deliver query to child nodes
    for child in Tree[cur]['child']: 
        print "calling", child
        # further optimization (should be implemented): construct a subtree for
        # each child and pass it on to the httpcmd as argument
        t = Thread (target = helper.wrapper, args = (helper.httpcmd,
                                                     (child, 'execQuery',
                                                      deepcopy (Tree),
                                                      deepcopy(Query),
                                                      deepcopy(AggCode),),
                                                     query_results))
        workers.append (t)

    # 3) start workers
    for worker in workers:
        worker.start()

    # 4) wait for workers finishes -> this part might be hung forever
    for worker in workers:
        worker.join()

    data=[]
    for res in query_results:
        if len (res) == 2:
            resp, content = res
            content = json.loads (content)
        else:
            content = res
        data += content

    # 4) process collected data using AggCode
    output = helper.processCollectedData (AggCode, data)

    # reset variables 
    query_results = []

    return output
'''

def installQuery (Tree, Query, Interval):
    return True

def uninstallQuery (Tree, Query):
    return True

def getPoorTCPFlows (freq):
    flowID = ''
    return flowID

def handleLeafNode (req):
    if req['api'] == 'execQuery':
        query    = req['query']
        return helper.processTIB (query, collection)
    elif req['api'] == 'check_source':
        name     = req['name'] 
        checksum = req['checksum'] 
        output = helper.checkSource (name, checksum)
        print output
        return output

def getThreadArgument (local, req, node=None):
    if local:
        api = req['api']
        if api == 'execQuery':
            query   = req['query']
            return (helper.processTIB, (query, collection))
        elif api == 'check_source':
            name     = req['name']
            checksum = req['checksum']
            return (helper.checkSource, (name, checksum))
    else:
        return (helper.httpcmd, (node, req))

def handleRequest (req):
    global query_results

    Tree = req['tree']
    cur = helper.getCurNodeID ()
    if len (Tree[cur]['child']) == 0:
        return handleLeafNode (req)

    # From now on, the following handles when the current node is a relay node
    workers = []
    # 1) create a worker thread at the current node
    (func, argv) = getThreadArgument (True, req)
    t = Thread (target = helper.wrapper, args = (func, argv, query_results))
    workers.append (t)

    # 2) deliver query to child nodes
    for child in Tree[cur]['child']: 
        print "calling:", child
        (func, argv) = getThreadArgument (False, req, child)
        # further optimization (should be implemented): construct a subtree for
        # each child and pass it on to the httpcmd as argument
        t = Thread (target = helper.wrapper, args = (func, argv,
                                                     query_results))
        workers.append (t)

    # 3) start workers
    for worker in workers:
        worker.start()

    # 4) wait for workers finishes -> this part might be hung forever
    for worker in workers:
        worker.join()

    print "11111111111111111111111111111111"
    data=[]
    for res in query_results:
        if len(res) > 0 and type(res) == type(()) and 'content-type' in res[0]:
            resp, content = res
            content = json.loads (content)
        else:
            content = res

        data += content
    print "22222222222222222222222222222222"
    # reset variables 
    query_results = []

    if req['api'] == 'execQuery' and 'aggcode' in req:
        # 4) process collected data using AggCode
        return helper.processCollectedData (req['aggcode'], data)
    else:
        return data

# linkID = ('*', '16')
# timeRange = ('*', datetime.datetime(2015, 11, 9, 19, 10, 32, 765000))

# linkID = ('7', '16')
# timeRange = (datetime.datetime(2015, 11, 9, 19, 10, 30, 765000), datetime.datetime(2015, 11, 9, 19, 10, 32, 765000))

# linkID = ('7', '16')
# timeRange = ('*', '*')

# flowID = {'sip': '10.4.2.3', 'sport': '9000', 'dip': '10.3.2.3',
#           'dport': '60217', 'proto': '6'}

# flowID = {'sip': '*', 'sport': '9000', 'dip': '10.3.2.3',
#           'dport': '*', 'proto': '6'}
# Path = ['8-15', '15-18', '18-13', '13-6']
# Flow = {'flowid': flowID, 'path': Path}
# linkID = ('*', '*')
# timeRange = (datetime.datetime(2015, 11, 9, 19, 10, 30, 765000), datetime.datetime(2015, 11, 9, 19, 10, 32, 765000))
# getDuration (Flow, timeRange)
