from threading import Thread, Lock
from collections import deque
import os
import ctrlapi
import datetime

tid = None
msgqueue = deque ([])
queue_lock = Lock()
logfp = None

def init ():
    global tid, logfp
    if tid:
        return
    logname = 'ppflows_' + str(os.getpid()) + '.log'
    logfp = open (logname, 'w', 1)

    tid = Thread (target = postflow_handler, args = ())
    tid.start()

def cleanup():
    global logfp

    if logfp:
        logfp.close()
        logfp = None


def push_flowdata (fid, reason, paths):
    global msgqueue, queue_lock

    queue_lock.acquire()
    msgqueue.append ((fid, reason, paths))
    queue_lock.release()

def postflow_handler ():
    global msgqueue, queue_lock

    while True:
        queue_lock.acquire()
        if len (msgqueue) == 0:
            queue_lock.release()
            continue
        msg = msgqueue.popleft()
        queue_lock.release()

        fid    = msg[0]
        reason = msg[1]
        paths  = msg[2]
        if reason == 'POOR_PERF':
            tree = {'controller': {'parent': 'controller',
                                   'child': [fid['dip']]},
                    fid['dip']: {'parent': 'controller', 'child': []}}
            from_ts = datetime.datetime.now() - datetime.timedelta(minutes=10)
            timeRange = (from_ts, '*')
            # FOR TEST ONLY
            # tree = {'controller': {'parent': 'controller',
            #                        'child': ['172.17.0.3']},
            #         '172.17.0.3': {'parent': 'controller', 'child': []}}
            # timeRange = (datetime.datetime(2015, 11, 9, 20, 20, 52, 765000) - datetime.timedelta(minutes=10), '*')
            # FOR TEST ONLY
            query = {'name': 'retrieve_flow.py', 'argv': [fid, timeRange]}
            data = ctrlapi.execQuery (tree, query)
            save_flowrecord (fid, data)
        elif reason == 'PC_FAIL':
            # TODO: NEED TO HANDLE THIS CASE
            continue

def save_flowrecord (fid, data):
    global logfp

    if not logfp: return

    sip   = fid['sip']
    sport = fid['sport']
    dip   = fid['dip']
    dport = fid['dport']
    proto = fid['proto']
    str_fid = sip + ' ' + sport + ' ' + dip + ' ' + dport + ' ' + proto
    for d in data:
        str_path = concat_path (d['path'])
        output = str_fid + ' ' + str_path + '\n'
        logfp.write (output)

def concat_path (path):
    str_path = ''
    str_path = path[0]
    for i in range(1, len(path)):
        str_path = str_path + ' ' + path[i]

    return str_path
