# PathDump

PathDump is a datacenter network debugger that partitions the debugging
functionality between the edge devices and the network switches. This repository
maintains the implementations of PathDump's core mechanisms and example
debugging applications.

## Building and running PathDump

PathDump comprises of three components: controller, end-host and switch.
PathDump requires a dedicated machine for the controller component. The end-host
module should be installed in every server in a datacenter network. Deploying
switch rules can be done either the controller machine or any of the servers,
and running the scripts one is sufficient.

* To build, install and run the controller component, refer to
[README](controller/README.md) under the controller directory.

* To build, install and run the end-host component, refer to
[README](host/README.md) under the host directory.

* To configure and install switch rules at individual switches, refer to
[README](switch/README.md) under the switch directory.
