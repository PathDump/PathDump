## How to build

Simply run 'make'


## How to run

Note: flowmon is implemented (and tested) for k-ary fat-tree topology.

```
sudo ./flowmon <k value> <interface name>
```

For example with k=4 and local interface is vnet0, run ./flowmon 4 vnet0


## Additional notes

When there are problems (e.g., compilation or segmentation errors), there may be
some issue with dependent libraries, which this program will tell during the
compile and run time. In such case, take a look at the install.sh in the 'host'
directory and check if libraries were installed successfully without errors.
