import ctrlapi as capi
import heapq
import sys

def aggregate (topk, data):
    h = []
    for bytec, flow in data:
        if len (h) < topk or bytec > h[0][0]:
            if len (h) == topk: heapq.heappop (h)
            heapq.heappush (h, (bytec, flow))
    return h

if __name__ == "__main__":
    if len (sys.argv) == 2:
        binSize = int (sys.argv[1])
    else:
        binSize = 10000

    linkID = ('9', '17')
    timeRange = ('*', '*')
    query = {'name': 'imbalance_query.py', 'argv': [binSize, linkID, timeRange]}
    aggcode =  {'name': 'imbalance_query_agg.py', 'argv': []}

    tree = capi.getAggTree (['controller'])
    data = capi.execQuery (tree, query, aggcode)

    for eachChildResult in data:
        for eachEdge in eachChildResult.keys():
            for eachBucket in eachChildResult[eachEdge].keys():
                print "Edge:",eachEdge,"Bucket",eachBucket,"Count",eachChildResult[eachEdge][eachBucket]