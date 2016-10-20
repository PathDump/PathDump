#
# Path conformance application checks paths in each flow record. As an example,
# it treats a path with length > 6 (including links of src->ToR and ToR->dst)
# as abnormal and raises an alarm to the controller.
#
#
import ctrlapi as capi
import sys

if __name__ == "__main__":
    query = {'name': 'pathconf_check.py', 'argv': []}

    tree = capi.getAggTree (['controller'])
    if len (sys.argv) == 2 and sys.argv[1] == 'uninstall':
        data = capi.uninstallQuery (tree, query)
        exit (0)

    interval = 0.0
    retval = capi.installQuery (tree, query, interval) 
    print retval

    while True:
        try:
            flow = capi.getPolicyViolationFlow()
            print 'Violating a path policy:', flow
        except KeyboardInterrupt:
            exit (0)
