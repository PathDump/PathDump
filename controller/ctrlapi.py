import restapi as r
import json

controller = "0.0.0.0"

def execQuery (tree, query, aggcode=None):
    hosts = check_source (tree, query['name'])
    send_source (hosts, tree, query['name'])
    hosts = check_source (tree, aggcode['name'])
    send_source (hosts, tree, aggcode['name'])

    req = buildReq ('execQuery', tree, query, aggcode)
    resp, content = r.get (controller, json.dumps (req), "pathdump")
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
    print content
    return content

# DO FROM HERE!!
def send_source (hosts, tree, filename):
    # for host, retval in hosts.iteritems():
    #     if retval == False:

    # req = {'api': 'send_source'}
    # req.update ({'tree': tree})
    # req.update ({'name': filename})
    return True
