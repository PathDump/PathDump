import ctrlapi as capi
import heapq

def aggregate (topk, data):
    h = []
    for bytec, flow in data:
        if len (h) < topk or bytec > h[0][0]:
            if len (h) == topk: heapq.heappop (h)
            heapq.heappush (h, (bytec, flow))
    return h

if __name__ == "__main__":
    # tree = {'controller': {'parent': 'controller', 'child': ["172.17.0.3"]},
    #         '172.17.0.3': {'parent': 'controller', 'child': ['172.17.0.4', '172.17.0.5']},
    #         '172.17.0.4': {'parent': '172.17.0.3', 'child': []},
    #         '172.17.0.5': {'parent': '172.17.0.3', 'child': []}}
    topk = 10
    linkID = ('*', '*')
    timeRange = ('*', '*')
    query = {'name': 'topk_query.py', 'argv': [topk, linkID, timeRange]}
    aggcode =  {'name': 'topk_query_agg.py', 'argv': [topk]}

    tree = capi.getAggTree (['controller'])
    data = capi.execQuery (tree, query, aggcode)

    output = aggregate (topk, data)
    for bytec, flow in output:
        print 'flowid:', flow['flowid'], 'path:', flow['path'], 'bytes:', bytec
