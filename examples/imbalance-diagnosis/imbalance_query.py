import pathdumpapi as pdapi
import heapq
import json

def run (argv, coll):
    h = []
    binSize = argv[0]
    linkID = argv[1]
    timeRange = argv[2]
    result = {}

    flows = pdapi.getFlows (linkID, timeRange)
    for flow in flows:
        (bytec, pktc) = pdapi.getCount (flow, timeRange)
        edge=linkID[0]+'-'+linkID[1]
        bucket = bytec/binSize
        if edge not in result:
            result[edge]={}
        if bucket not in result[edge]:
            result[edge][bucket] = 0
        result[edge][bucket] += 1
    print "Result from child:",result
    return [result]
