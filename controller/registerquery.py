#!/usr/bin/python

import ctrlapi as capi
import sys

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print 'usage:', sys.argv[0], '<query file>'
        exit (0)
    filename = sys.argv[1]

    data = capi.registerQuery (filename)
    print data
