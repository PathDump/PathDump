import pathdumpapi as pdapi

def run (argv, coll):
    freq = argv[0]

    for flowid in pdapi.getPoorTCPFlows (freq):
        pdapi.postFlow(flowid, 'POOR_PERF', [])
