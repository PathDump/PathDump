from pymongo import MongoClient
from bson import json_util
import pymongo
import socket
import sys
import json
from datetime import datetime

client=MongoClient('localhost', 27017)
database=client['PathDump']
collection=database['TIB']

# returns an IP address as Node ID
def getCurNodeID ():
    return socket.gethostname()

def pushToDB(entries):
    for e in entries:
        e['start']=datetime.now()
        e['end']=datetime.now()
        e['log']=datetime.now()
        #print e
        try:
            collection.insert(e);
        except:
            type,value,traceback = sys.exc_info()
            print type.message;
            sys.exit()

def clearDB():
    collection.remove({})

def loadFileAndPushToDB(filename):
    fh=open(filename,'r')
    clearDB()
    pushToDB(json.load(fh))

loadFileAndPushToDB('data/'+getCurNodeID()+'.json')




