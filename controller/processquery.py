import restapi as r
from bson import json_util
import json
from threading import Thread
import confparser as cp
import os
import postflow as pf
import aggtree
import myutil

results=[]

def wrapper (func, args, results):
    results.append ( func (*args) )

def httpcmd (server, req, url):
    return r.get (server, json.dumps(req, default=json_util.default), url)

def handlerequest (req, url):
    if req['api'] == 'check_source':
        md5file = req['name'] + '.md5'
        filepath = cp.options['home']+'/'+cp.options['repository']+'/'+md5file
        req.update ({'checksum': myutil.load_file (filepath)})
    elif req['api'] == 'send_source':
        srcfile = req['name']
        filepath = cp.options['home']+'/'+cp.options['repository']+'/'+srcfile
        req.update ({'file': myutil.load_file (filepath)})
        filepath = filepath + '.md5'
        req.update ({'checksum': myutil.load_file (filepath)})
   # This api should be called only from queries installed in host 
    elif req['api'] == 'postFlow':
        # initialize a thread if it is not already done
        pf.init()
        # retrieve flow ID from the request and push it into a shared buffer
        pf.push_flowdata (req['fid'], req['reason'], req['paths'])

        # in background, the thread will concurrently execute a query in order
        # to fetch a flow record from the destination host and put the record
        # into a local file, so here we just return
        return json.dumps ([{'controller': True}], default=json_util.default)
   # This api should be called only from queries installed in host 
    elif req['api'] == 'postResult':
        # print req['result']
        # TODO: an extension; should be implemented
        return json.dumps ([{'controller': True}], default=json_util.default)
    elif req['api'] == 'getAggTree':
        tree = {}
        for gn in req['groupnodes']:
            aggtree.buildAggTree (tree, 'controller', 'controller',
                                  aggtree.grouptree, gn)
        aggtree.cleanupMetaData (tree)
        return json.dumps ([tree], default=json_util.default)
    elif req['api'] == 'getFlowCollDir':
        colldir = cp.options['home'] + '/' + cp.options['collection']
        return json.dumps ([colldir], default=json_util.default)
    elif req['api'] == 'registerQuery':
        filepath = cp.options['home']+'/'+cp.options['repository']+'/'+req['name']
        retval = myutil.save_file (filepath, req['data'])
        if retval:
            md5val = myutil.md5 (filepath)
        retval = myutil.save_file (filepath + '.md5', md5val + '\n')
        return json.dumps ([retval], default=json_util.default)

    return execRequest (req, url)

def execRequest (req, url):
    global results
    workers = []
    tree = req['tree']
    for child in tree['controller']['child']:
        t = Thread (target = wrapper, args = (httpcmd, (child, req, url),
                                              results))
        workers.append (t)

    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    data = []
    for res in results:
        resp, content = res
        if resp['status'] == '200':
            data += json.loads (content, object_hook=json_util.object_hook)

    results = []
    return json.dumps (data, default=json_util.default)

