import heapq

def run (argv, data):
    result = {}
    for eachChildResult in data:
        for edge in eachChildResult.keys():
            if edge not in result:
                result[edge] = {}
            for eachBucket in eachChildResult[edge].keys():
                if eachBucket not in result[edge]:
                    result[edge][eachBucket] = 0
                result[edge][eachBucket] += eachChildResult[edge][eachBucket]
    return [result]
