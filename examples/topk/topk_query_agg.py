from datetime import datetime
import math

def run (argv, data):
    topk = argv[0]

    children_dict={}
    for entry in data:
        children_dict.update(entry)
        # for key,val in entry.items():
            # if key == "topk":
            #     children_dict.update(val)
            # else:
            #     print "reach here!!!"
            #     odata.append({key:val})
    print "len of children dict:",len(children_dict)
    sorted_flows = sorted(children_dict.iteritems(), key=lambda (k, v): (-v, k))[:topk]

    topk_dict={}
    for k,v in sorted_flows:
        topk_dict.update({k:v})
    print "len of topk dict after reduce:", len(topk_dict)

    odata=[]
    odata.append (topk_dict)
    return odata
