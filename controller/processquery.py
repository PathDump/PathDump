import restapi as r
import json
from threading import Thread
import confparser as cp
import os

results=[]

def wrapper (func, args, results):
    results.append ( func (*args) )

def httpcmd (server, req, url):
    return r.get (server, json.dumps(req), url)

def handlerequest (req, url):
    if req['api'] == 'check_source':
        md5file = req['name'] + '.md5'
        req.update ({'checksum': load_file (md5file)})
    elif req['api'] == 'send_source':
        srcfile = req['name']
        req.update ({'file': load_file (srcfile)})
        md5file = srcfile + '.md5'
        req.update ({'checksum': load_file (md5file)})
   # This api should be called only from queries installed in host 
    elif req['api'] == 'postFlow':
        # TODO: NEED TO BE IMPLEMENTED
        return json.dumps ([{'controller': True}])
   # This api should be called only from queries installed in host 
    elif req['api'] == 'postResult':
        print req['result']
        # TODO: NEED TO BE IMPLEMENTED
        return json.dumps ([{'controller': True}])

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
            data += json.loads (content)

    results = []
    return json.dumps (data)

def load_file (filename):
    filepath = os.getcwd() + '/' + cp.options['repository'] + '/' + filename
    with open (filepath, 'r') as f:
        return f.read()
