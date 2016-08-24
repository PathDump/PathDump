import heapq

def run (argv, data):
    h = []
    topk = argv[0]

    for bytec, flow in data:
        if len (h) < topk or bytec > h[0][0]:
            if len (h) == topk: heapq.heappop (h)
            heapq.heappush (h, (bytec, flow))
    return h
