from pymongo import MongoClient
import pymongo
from datetime import datetime

def run (argv, coll):
    topk = argv[0]
    pdata={}
    count=0
    pipeline = [ {"$sort": {"bytes": -1}}, {"$limit": topk} ]
    for res in coll.aggregate (pipeline):
        # pdata.update({res["id"]+uniq_id+"_"+str(count): res["bytes"]})
        key = res["id"] + "_" + "_".join (res['path'])  + "_" + str(count)
        pdata.update({key: res["bytes"]})
        count +=1
    print "len of topk dict before reduce:", len(pdata)

    odata=[]
    # odata.append({'topk': pdata})
    odata.append(pdata)
    return odata
