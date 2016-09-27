from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from threading import Condition
from threading import Thread
from collections import deque
import time
import os

observer = None
start_time = 0
started = False
queuecv=Condition()
flowqueue=deque()
files = {}

class MyHandler (FileSystemEventHandler):
    def on_modified (self, event):
        if event.is_directory: return
        if event.src_path not in files:
            files[event.src_path] = open (event.src_path, 'r')

        curfile = files[event.src_path]
        while True:
            where = curfile.tell()
            line = curfile.readline()
            if not line:
                curfile.seek (where)
                break
            record = line.rstrip()
            tokens = record.split()
            if float (tokens[0]) < start_time: continue
            queuecv.acquire()
            flowqueue.append (record)
            queuecv.notify()
            queuecv.release()
   
def getFlowRecord(reason):
    queuecv.acquire()
    while len (flowqueue) == 0:
        queuecv.wait(10.0)
    record = flowqueue.popleft()
    queuecv.release()
    tokens = record.split()
    if tokens[1] == reason:
        flow = {'flowid':{}, 'path': []}

        flow['flowid']['sip']   = tokens[2]
        flow['flowid']['sport'] = tokens[3]
        flow['flowid']['dip']   = tokens[4]
        flow['flowid']['dport'] = tokens[5]
        flow['flowid']['proto'] = tokens[6]
        for i in range (7, len(tokens)):
            flow['path'].append (tokens[i])

        return flow

def init (dirpath):
    global observer, started, start_time

    if started: return
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule (event_handler, path = dirpath, recursive = False)
    observer.start()

    start_time = time.time()
    started = True

def cleanup():
    global observer
    observer.stop()
    observer.join()
    observer = None

'''
if __name__ == "__main__":
    dirpath = "/home/myungjin/PathDump/controller/flowrecords"
    init (dirpath)

    try:
        while True:
            getFlowRecord()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
'''
