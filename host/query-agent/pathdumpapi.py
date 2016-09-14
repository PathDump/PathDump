from pymongo import MongoClient
import pymongo
from datetime import datetime
import helperapi as helper
import confparser as cp
import tcpmon

client=MongoClient('localhost', 27017)
database=client['pathdump']
collection=database['TIB']

def getFlows (linkID, timeRange):
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

    proj_fltr = {'bytes': 1, 'pkts': 1, '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)

    bytec = 0 # byte count
    pktc  = 0 # packet count
    for c in cursor:
        bytec += c['bytes']
        pktc += c['pkts']

    return (bytec, pktc)

def getDuration (Flow, timeRange):
    (sip_fltr, sport_fltr, dip_fltr, dport_fltr, proto_fltr) = \
        helper.buildFlowidFilter (Flow['flowid'])
    path_fltr = helper.buildPathFilter (Flow['path'])
    (stime_fltr, etime_fltr) = helper.buildTimeFilter (timeRange)
    data_fltr = helper.doAndFilters ([sip_fltr, sport_fltr, dip_fltr,
                                     dport_fltr, proto_fltr, path_fltr, 
                                     stime_fltr, etime_fltr])

    proj_fltr = {'start': 1, 'end': 1, '_id': 0}
    if data_fltr == '':
        cursor = collection.find (None, proj_fltr)
    else:
        cursor = collection.find (data_fltr, proj_fltr)

    start = -1
    end = -1
    for c in cursor:
        if start == -1 or start > c['start']:
            start = c['start']
        if end == -1 or end <  c['end']:
            end = c['end']

    delta = end - start
    return delta.total_seconds()

def postFlow (flowID, Reason, Paths):
    req = {'api': 'postFlow'}
    req.update ({'fid': flowID})
    req.update ({'reason': Reason})
    req.update ({'paths': Paths})
    return helper.httpcmd (cp.options['controller'], req)

def getPoorTCPFlows (freq):
    tcpmon.init()
    poorFlows = tcpmon.updatePoorFlows (freq)
    flowIDs = []
    for fid in poorFlows:
        tokens = fid.split (':')
        if len (fields) != 5:
            continue
        flowid = {}
        flowid['sip']   = tokens[0]
        flowid['sport'] = tokens[1]
        flowid['dip']   = tokens[2]
        flowid['dport'] = tokens[3]
        flowid['proto'] = tokens[4]
        flowIDs.append (flowid)
    return flowIDs

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
