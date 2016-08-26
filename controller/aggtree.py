#!/usr/bin/python
import random
import json
from pprint import pprint
import sys

def buildGroupTree (filename):
    gtree = {}

    with open(filename) as data_file:
        data = json.load (data_file)

    for group in data:
        gid      = group ['gid']
        gtree[gid]          = {}
        gtree[gid]['host'] = group['host']
        gtree[gid]['child'] = group['child']
    return gtree

def initTreeNode (tree, cur, parent):
    tree[cur] = {}
    tree[cur]['parent'] = parent
    tree[cur]['child'] = []
    tree[cur]['gtchild'] = []
    return tree[cur]

def buildAggTree (tree, parent, cur, gtree, gtcur):
    tnode = initTreeNode (tree, cur, parent)

    if len (gtree[gtcur]['child']) == 0:
        # add remaining hosts in the group tree
        for node in gtree[gtcur]['host']:
            if node not in tree:
                tnode['child'].append (node)
                initTreeNode (tree, node, cur)
        return

    for gtchild in gtree[gtcur]['child']:
        node = cur
        while node in tree:
            node = random.choice (gtree[gtchild]['host'])
        tnode['child'].append(node)
        tnode['gtchild'].append(gtchild)

    for i in range (0, len (tree[cur]['child'])):
        child = tnode['child'][i]
        gtchild = tnode['gtchild'][i]
        buildAggTree (tree, cur, child, gtree, gtchild)

def cleanupMetaData (tree):
    for v in tree.itervalues():
        del v['gtchild']

if __name__ == '__main__':
    random.seed(1)
    tree = {}

    gtree = buildGroupTree (sys.argv[1])
    buildAggTree (tree, 'controller', 'controller', gtree, 'controller')

    cleanupMetaData (tree)

    data = json.dumps(tree)
    pprint (tree)
    print '----'
    pprint (data)

