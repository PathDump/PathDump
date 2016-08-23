from datetime import datetime, timedelta
import json
import restapi as r
import argparse
from time import sleep
import os
import random
import math
import sys
from pprint import pprint

parser=argparse.ArgumentParser(description="container sample example")
parser.add_argument('--topk',dest="topk",default=10,help="top k value")
parser.add_argument('--run',dest="run",default="topk",help="run topk")

args=parser.parse_args()
controller="0.0.0.0"

def gettopk(topk, body):
    data=json.dumps (body)
    resp,content = r.get (controller, data, "mapreduce")
    content=json.loads(content)

    output = aggregate (topk, content)
    return output

def createTopKBody (api, tree, query, aggcode):
    reqbody = {'api': api}
    reqbody.update ({'tree': tree})
    reqbody.update ({'query': query})
    if aggcode:
        reqbody.update ({'aggcode': aggcode})
    return reqbody

def aggregate (topk, data):
    children_dict={}
    for entry in data:
        children_dict.update(entry)
    sorted_flows = sorted(children_dict.iteritems(), key=lambda (k, v): (-v, k))[:topk]

    topk_dict={}
    for k,v in sorted_flows:
        topk_dict.update({k:v})
    return topk_dict

if args.run=="topk":
    api = 'execQuery'
    tree = {'controller': {'parent': 'controller', 'child': ["172.17.0.3"]},
            '172.17.0.3': {'parent': 'controller', 'child': ['172.17.0.4', '172.17.0.5']},
            '172.17.0.4': {'parent': '172.17.0.3', 'child': []},
            '172.17.0.5': {'parent': '172.17.0.3', 'child': []}}
    topk = 10
    query = {'path': 'apps/topk.py', 'argv': [topk]}
    aggcode =  {'path': 'apps/topk_agg.py', 'argv': [topk]}
    reqbody = createTopKBody (api, tree, query, aggcode)

    content = gettopk (topk, reqbody)

    for key, val in content.items():
        print key, val 
