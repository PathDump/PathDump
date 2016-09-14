#!/usr/bin/python
import random
import json
from pprint import pprint
import sys

grouptree = {}

def buildGroupTree (filename):
    global grouptree
    grouptree = {}

    with open(filename) as data_file:
        data = json.load (data_file)

    for group in data:
        gid      = group ['gid']
        grouptree[gid]          = {}
        grouptree[gid]['host']  = group['host']
        grouptree[gid]['child'] = group['child']

def initTreeNode (aggtree, cur, parent):
    if cur not in aggtree:
        aggtree[cur] = {}
        aggtree[cur]['parent'] = parent
        aggtree[cur]['child'] = []
        aggtree[cur]['gtchild'] = []
    return aggtree[cur]

def buildAggTree (aggtree, parent, cur, gtree, gtcur):
    tnode = initTreeNode (aggtree, cur, parent)

    if len (gtree[gtcur]['child']) == 0:
        # add remaining hosts in the group tree
        for node in gtree[gtcur]['host']:
            if node not in aggtree:
                tnode['child'].append (node)
                initTreeNode (aggtree, node, cur)
        return

    for gtchild in gtree[gtcur]['child']:
        node = cur
        bupdate = True
        while node in aggtree:
            node = random.choice (gtree[gtchild]['host'])
            if len (gtree[gtchild]['host']) == 1 and node in aggtree:
                bupdate = False
                break
        if not bupdate: continue
        tnode['child'].append(node)
        tnode['gtchild'].append(gtchild)

    for i in range (0, len (aggtree[cur]['child'])):
        child = tnode['child'][i]
        gtchild = tnode['gtchild'][i]
        buildAggTree (aggtree, cur, child, gtree, gtchild)

def cleanupMetaData (aggtree):
    for v in aggtree.itervalues():
        del v['gtchild']

'''
if __name__ == '__main__':
    random.seed(1)
    aggtree = {}

    buildGroupTree (sys.argv[1])
    groupnodes = sys.argv[2].split()
    for gn in groupnodes:
        buildAggTree (aggtree, 'controller', 'controller', grouptree, gn)

    cleanupMetaData (aggtree)

    data = json.dumps(aggtree)
    pprint (aggtree)
    print '----'
    pprint (data)
'''
