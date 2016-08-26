import restapi as r
import json
from copy import deepcopy

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
    hosts = check_source (tree, aggcode['name'])
    if send_source (hosts, tree, aggcode['name']) == False:
        return []

    req = buildReq ('execQuery', tree, query, aggcode)
    resp, content = r.get (controller, json.dumps (req), "pathdump")
    # resp = {'status': '300'}
    if resp['status'] != '200':
        return []
    else:
        return json.loads (content)

def buildReq (api, tree, query, aggcode=None, interval=None):
    req = {'api': api}
    req.update ({'tree': tree})
    req.update ({'query': query})
    if aggcode:
        req.update ({'aggcode': aggcode})
    if interval:
        req.update ({'interval': interval})
    return req

def check_source (tree, filename):
    req = {'api': 'check_source'}
    req.update ({'tree': tree})
    req.update ({'name': filename})

    resp, content = r.post (controller, json.dumps (req), "pathdump")
    return json.loads (content)

def send_source (hosts, tree, filename):
    if source_available_at (hosts):
        return True

    # need to send a copy of source to hosts which don't have it
    send_tree = remove_hosts_from_tree (hosts, tree)
    
    req = {'api': 'send_source'}
    req.update ({'tree': send_tree})
    req.update ({'name': filename})

    resp, content = r.post (controller, json.dumps (req), "pathdump")
    return source_available_at (json.loads (content))

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
