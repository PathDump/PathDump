import imp
import restapi
import netifaces as ni
import json

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

def isSamePath (p1, p2):
    if len(p1) != len(p2):
        return False
    for i in range(0, len(p1)):
        if p1[i] != p2[i]:
            return False

    return True

# returns an IP address as Node ID
def getCurNodeID ():
    return ni.ifaddresses('eth0')[2][0]['addr']

def wrapper (func, args, results):
    results.append (func (*args))

def processTIB (source, collection):
    print "rec app call"
    module = imp.load_source ('', source['path'])
    # module must implement 'run' function
    return module.run (source['argv'], collection)

def processCollectedData (source, data):
    module = imp.load_source ('', source['path'])
    # module must implement 'run' function
    return module.run (source['argv'], data)

def httpcmd (node, api, tree, query, aggcode=None, interval=None):
    reqbody = {'api': api}
    reqbody.update ({'tree': tree})
    reqbody.update ({'query': query})
    if aggcode:
        reqbody.update ({'aggcode': aggcode})
    if interval:
        reqbody.update ({'interval': interval})

    return restapi.post(node, json.dumps (reqbody), "mapreduce")
