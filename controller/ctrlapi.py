import restapi as r
from bson import json_util
import json
from copy import deepcopy
import flowcoll

controller = "0.0.0.0"

# parsing of request should be done here
# then, correct API should be called
#
# request json format example 1
#   {'api': 'execQuery'}
#   {'tree': {...}}
#   {'query': {'name': 'topk_query.py',
#              'argv': [1000]}}
#   {'aggcode': {'name': 'topk_query_agg.py',
#              'argv': [1000]}}
#
# request json format example 2
#   {'api': 'installQuery'}
#   {'tree': {...}}
#   {'query': {'name': 'topk_query.py',
#              'argv': [1000]}}
#   {'interval': 0.1}
#
# request json format example 3
#   {'api': 'uninstallQuery'}
#   {'query': {'name': 'topk_query.py',
#              'checksum': 'eea7d80064c3c1d9374e2897ccd69a98'}}

def execQuery (tree, query, aggcode=None):
    hosts = check_source (tree, query['name'])
    if send_source (hosts, tree, query['name']) == False:
        return []

    if aggcode:
        hosts = check_source (tree, aggcode['name'])
        if send_source (hosts, tree, aggcode['name']) == False:
            return []

    req = buildReq ('execQuery', tree, query, aggcode)
    resp, content = r.get (controller, json.dumps (req, default=json_util.default), "pathdump")
    if resp['status'] != '200':
        return []
    else:
        return json.loads (content, object_hook=json_util.object_hook)

def installQuery (tree, query, interval):
    hosts = check_source (tree, query['name'])
    if send_source (hosts, tree, query['name']) == False:
        return []

    req = buildReq ('installQuery', tree, query, None, interval)
    resp, content = r.get (controller, json.dumps (req, default=json_util.default), "pathdump")
    if resp['status'] != '200':
        return []
    else:
        return json.loads (content, object_hook=json_util.object_hook)

def uninstallQuery (tree, query):
    req = buildReq ('uninstallQuery', tree, query)
    resp, content = r.get (controller, json.dumps (req, default=json_util.default), "pathdump")
    if resp['status'] != '200':
        return []
    else:
        return json.loads (content, object_hook=json_util.object_hook)

def buildReq (api, tree, query, aggcode=None, interval=None):
    req = {'api': api}
    req.update ({'tree': tree})
    req.update ({'query': query})
    if aggcode:
        req.update ({'aggcode': aggcode})
    if interval is not None:
        req.update ({'interval': interval})
    return req

def check_source (tree, filename):
    req = {'api': 'check_source'}
    req.update ({'tree': tree})
    req.update ({'name': filename})

    resp, content = r.post (controller, json.dumps (req, default=json_util.default), "pathdump")
    return json.loads (content, object_hook=json_util.object_hook)

def send_source (hosts, tree, filename):
    if source_available_at (hosts):
        return True

    # need to send a copy of source to hosts which don't have it
    send_tree = remove_hosts_from_tree (hosts, tree)
    
    req = {'api': 'send_source'}
    req.update ({'tree': send_tree})
    req.update ({'name': filename})

    resp, content = r.post (controller, json.dumps (req, default=json_util.default), "pathdump")
    return source_available_at (json.loads (content, object_hook=json_util.object_hook))

def remove_hosts_from_tree (hosts, tree):
    send_tree = deepcopy (tree)

    for entry in hosts:
        host, val = entry.items()[0]
        if not val: continue
        # the host already has a copy of source, so it should be removed from
        # the send_tree
        parent = send_tree[host]['parent']
        if len (send_tree[host]['child']):
            # host is not a leaf node, so all of its child nodes should be
            # linked to its parent
            for new_child in send_tree[host]['child']:
                send_tree[parent]['child'].append (new_child)
                send_tree[new_child]['parent'] = parent

        # remove host from its parent
        send_tree[parent]['child'].remove (host)
        # remove host from the send_tree
        del (send_tree[host])

    # print 'send_tree:', send_tree
    return send_tree

def source_available_at (hosts):
    for entry in hosts:
        host, val = entry.items()[0]
        if not val:
            return False
    return True

def getAggTree (groupnodes):
    req = {'api': 'getAggTree'}
    req.update ({'groupnodes': groupnodes})

    resp, content = r.get (controller, json.dumps (req, default=json_util.default), "pathdump")
    if resp['status'] != '200':
        return {}
    else:
        return json.loads (content, object_hook=json_util.object_hook)[0]

def getFlowCollectionDir():
    req = {'api': 'getFlowCollDir'}

    resp, content = r.get (controller, json.dumps (req, default=json_util.default), "pathdump")
    if resp['status'] != '200':
        return ''
    else:
        return json.loads (content, object_hook=json_util.object_hook)[0]

def getPoorTCPFlow():
    if not flowcoll.started:
        dirpath = getFlowCollectionDir()
        flowcoll.init (dirpath)

    try:
        flow = flowcoll.getFlowRecord('POOR_PERF')
    except KeyboardInterrupt:
        flowcoll.cleanup()
        raise

    return flow
