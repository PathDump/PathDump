import pathdumpapi as pdapi
from bson import json_util
import json
import datetime

def run (argv, coll):
    flowid = argv[0]
    timeRange = json.loads (json.dumps(argv[1]),
                            object_hook=json_util.object_hook)
    if isinstance (timeRange[0], datetime.datetime):
        timeRange[0].replace (tzinfo=None)
    if isinstance (timeRange[1], datetime.datetime):
        timeRange[1].replace (tzinfo=None)
    linkID = ('*', '*')

    return pdapi.getPaths (flowid, linkID, timeRange)
