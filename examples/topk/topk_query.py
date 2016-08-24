import pathdumpapi as pdapi
import heapq

def run (argv, coll):
    h = []
    topk = argv[0]
    linkID = argv[1]
    timeRange = argv[2]

    flows = pdapi.getFlows (linkID, timeRange)
    for flow in flows:
        (bytec, pktc) = pdapi.getCount (flow, timeRange)
        if len (h) < topk or bytec > h[0][0]:
            if len (h) == topk: heapq.heappop (h)
            heapq.heappush (h, (bytec, flow))
    return h
