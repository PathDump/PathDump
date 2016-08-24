import restapi as r
import json

def buildReq (api, tree, query, aggcode=None, interval=None):
    req = {'api': api}
    req.update ({'tree': tree})
    req.update ({'query': query})
    if aggcode:
        req.update ({'aggcode': aggcode})
    if interval:
        req.update ({'interval': interval})
    return req

def execQuery (tree, query, aggcode=None):
    controller = "0.0.0.0"

    req = buildReq ('execQuery', tree, query, aggcode)

    # NEED TO CHECK FILE AVAILIBILITY AT SERVER
    # check_and_send_sources (query, aggcode) <- NEED TO IMPLEMENT

    resp, content = r.get (controller, json.dumps (req), "pathdump")

    if resp['status'] != '200':
        return []
    else:
        return json.loads (content)
