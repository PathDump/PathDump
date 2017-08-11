import httplib2
import socket

port="5000"
h = httplib2.Http(socket.gethostname()+".cache")

def post(server,data,POSTURL):
    url="http://"+server+":"+port+"/"+POSTURL
    resp,content = h.request(
    uri = url,
    method = 'POST',
    headers={'Content-Type' : 'application/json'},
    body=data)
    return resp,content

def get(server,data,GETURL):
    url="http://"+server+":"+port+"/"+GETURL
    resp,content = h.request(
    uri = url,
    method = 'GET',
    headers={'Content-Type' : 'application/json'},
    body=data)
    return resp,content
