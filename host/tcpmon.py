from subprocess import Popen, PIPE
from threading import Thread, Lock
import os
import signal
from helperapi import cwd
import time

proc = None
stop_flag = False
mon_lock=Lock()
mon_flows={}
candidates = {}

def init():
    global proc, candidates, mon_flows, stop_flag
    if proc == None:
        candidates = {}
        mon_flows={}
        stop_flag = False
        cmd = cwd + '/tcpretrans'
        proc = Popen ([cmd, ''], stdout = PIPE, bufsize = 1)
        t = Thread (target = monitor_retransmit, args = ())
        t.start()

def cleanup():
    global stop_flag, candidates, mon_flows
    stop_flag = True
    candidates = {}
    mon_flows={}

def monitor_retransmit():
    global proc

    with proc.stdout:
        for line in iter (proc.stdout.readline, b''):
            if stop_flag:
                break

            tokens = line.split()
            if len(tokens) < 5 or (tokens[2] == '-:-' and tokens[4] == '-:-') \
                    or tokens[0] == "TIME":
                continue

            key = tokens[1] + ':' + tokens[3] + ':6'

            mon_lock.acquire()
            if key not in mon_flows:
                print "updating mon_flows", key
                mon_flows.update ({key: 1})
            mon_lock.release()

    os.kill (proc.pid, signal.SIGTERM)
    proc.wait() # wait for the subprocess to exit
    proc = None

def updatePoorFlows (frequency):
    global candidates, mon_flows

    rm_ent = []
    poorFlows = []
    mon_lock.acquire()
    for key in candidates.iterkeys():
        if key not in mon_flows:
            # no consecutive retransmissions found for the flow (i.e., key)
            # hence reset its entry from candidates dictionary
            rm_ent.append (key)
        else:
            # retransmission occurred again. So, increment frequency by 1
            candidates[key] += 1

            # now this flow meets the frequency condition.
            # So, it is a poor TCP flow 
            if  candidates[key] >= frequency:
                print "raising alarm:", key, candidates[key]
                poorFlows.append (key)
                rm_ent.append (key)

    # Check whether flows from mon_flows are not in candidates dictionary.
    # If so, those flows are new ones that experience retransmission.
    # So, create a new entry in the candidates dictionary.
    for key, count in mon_flows.items():
        if key not in candidates:
            candidates.update ({key: 1})

    for key in rm_ent:
        del candidates[key]
    # reset mon_flows dictionary
    mon_flows = {}
    mon_lock.release()

    return poorFlows

# if __name__ == '__main__':
#     init()

#     try:
#         while True:
#             poorFlows = updatePoorFlows (3)
#             for f in poorFlows:
#                 print '\tpoorflow id:', f
#             time.sleep (5)
#     except KeyboardInterrupt:
#         cleanup()
#         exit (1)
