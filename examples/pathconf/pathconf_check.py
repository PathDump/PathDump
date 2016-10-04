import sys
import json
import pathdumpapi as pdi

FOUR_HOPS_LEN = 6 # [srcip,tor-agg,agg-core,core-agg,agg-tor,dstip]


def run(flowRecord):
    global FOUR_HOPS_LEN
    path = flowRecord['path']
    if len(path) > FOUR_HOPS_LEN:
        flowID = {}
        reason = 'PC_FAIL'
        data = {'path':path}
        flowID['sip']   = flowRecord['sip']
        flowID['sport'] = flowRecord['sport']
        flowID['dip']   = flowRecord['dip']
        flowID['dport'] = flowRecord['dport']
        flowID['proto'] = flowRecord['proto']
        pdi.postFlow(flowID, reason, [data])
