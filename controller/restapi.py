import httplib2
import json
from datetime import datetime
#from concurrent.futures import ThreadPoolExecutor
#from requests_futures.sessions import FuturesSession
#from requests import Request
#import grequests

#s = FuturesSession(executor=ThreadPoolExecutor(max_workers=30))
port = "5000"
h = httplib2.Http (".cache")


def get (server, data, GETURL):
    url="http://" + server + ":" + port + "/" + GETURL
    resp, content = h.request (uri = url,
                               method = 'GET',
                               headers={'Content-Type' : 'application/json'},
                               body=data)
    return resp,content


def post (server, data, POSTURL):
    url = "http://" + server + ":" + port + "/" + POSTURL
    resp, content = h.request (uri = url,
                               method = 'POST',
                               headers = {'Content-Type' : 'application/json'},
                               body = data)
    return resp, content

'''def post_asycreq(server,data,POSTURL):
    url="http://"+server+":"+port+"/"+POSTURL
    #req = Request('POST',  url,
    #data=data,
    #headers={'Content-Type' : 'application/json'}
    #)
    #prepped = s.prepare_request(req)

    # do something with prepped.body
    # do something with prepped.headers
    data=json.loads(data)
    data.update({"c_req_sent":str(datetime.now())})
    resp = s.post(url, data=json.dumps(data), headers={'Content-Type' : 'application/json'}, verify=False)

    return resp


def post_asyc_grerequest(servers,data,POSTURL):
    urls=[]
    for server in servers:
        urls.append("http://"+server+":"+port+"/"+POSTURL)
    data=json.loads(data)
    data.update({"c_req_sent":str(datetime.now())})
    rs=(grequests.post(u, data=json.dumps(data), headers={'Content-Type' : 'application/json'}) for u in urls)

    return grequests.map(rs)'''
