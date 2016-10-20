import pathdumpapi as pdapi

GOOD_MAX_HOPS = 6 # [srcip, tor-agg, agg-core, core-agg, agg-tor, dstip]

def run (flowRecord):
    path = flowRecord['path']
    if len(path) > GOOD_MAX_HOPS:
        flowID = {}
        reason = 'PC_FAIL'
        data = {'path':path}
        flowID['sip']   = flowRecord['sip']
        flowID['sport'] = flowRecord['sport']
        flowID['dip']   = flowRecord['dip']
        flowID['dport'] = flowRecord['dport']
        flowID['proto'] = flowRecord['proto']
        pdapi.postFlow (flowID, reason, [data])
