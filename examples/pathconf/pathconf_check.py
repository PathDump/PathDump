import sys
import zmq
import json
import pathdumpapi as pdi

init = False
socket = None
FOUR_HOPS_LEN = 6 # [srcip,tor-agg,agg-core,core-agg,agg-tor,dstip]

def initialize(argv):
    global socket

    url = str(argv[0])
    filter_str = str(argv[1])
    #  Socket to subscribe for flow records
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect(url)

    # Python 2 - ascii bytes to unicode str
    if isinstance(filter_str, bytes):
       filter_str = filter_str.decode('ascii')
    print("Collecting flow stats host agent",url,filter_str)
    socket.setsockopt_string(zmq.SUBSCRIBE, filter_str)
    

def run(argv, collection):
    global init,socket,FOUR_HOPS_LEN
    if not init:
        initialize(argv)
        init = True
    
    if socket:
        print "waiting for data"
        string = socket.recv_string()
        filter_str=str(argv[1])
        string = string[len(filter_str):]
        flow_record = json.loads(string)
        path = flow_record['path']
        if len(path) > FOUR_HOPS_LEN:
            flowID = {}
            reason = 'PC_FAIL'
            data = {'path':path}
            flowID['sip']   = flow_record['sip']
            flowID['sport'] = flow_record['sport']
            flowID['dip']   = flow_record['dip']
            flowID['dport'] = flow_record['dport']
            flowID['proto'] = flow_record['proto']
            pdi.postFlow(flowID, reason, [data])
            return "Posted PC_FAIL flow record"
        else:
            return "Path is valid"
