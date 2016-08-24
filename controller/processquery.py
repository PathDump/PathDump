import restapi as r
import json
import threading

results=[]

def wrapper (func, args, results):
    results.append ( func (*args) )

def httpcmd (server, req, url):
    req = json.loads (req)
    return r.get (server, json.dumps(req), url)

def handlerequest (req, url):
    global results
    workers = []
    tree = req['tree']
    for child in tree['controller']['child']:
        t = threading.Thread (target = wrapper, args = (httpcmd,
                                                        (child,
                                                         json.dumps(req),
                                                         url,),
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
