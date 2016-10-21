# PathDump host modules

Implementation of PathDump host modules. A host has three modules: OVS module,
flow monitor, and query agent. The OVS module has an OVS patch file (to enable
PathDump packet processing) and two configuration scripts. The flow monitor
module reads the path information from the OVS and stores it into a local
database (implemented using MongDB). Finally, the query agent interacts with
thePathDump controller and other query agents in different end-hosts and process
queries.

## How to install

To install the modules,

```
sudo ./install.sh <directory>
```

\<directory\> is the target directory to install the host modules. If the user
has write permission on the target directory, 'sudo' can be omitted.


## How to run

First, go to the directory that all of the modules are installed.
The following shows an example for configuring and running host modules:

```
sudo ./start_vswitch.sh
sudo ./vifconfig.sh -s
sudo ./flowmon <k> <interface name> &
sudo ./agent.py <config file>
```

The script, vifconfig.sh is is written for a testbed at the University of
Edinburgh. Depending on the conditions (e.g., topology, # of servers, etc.) of a
test network, the script may need modification or users need to write their own
script. At a minimum, there are two parameters that reqiures attention. The
first parameter is a physical interface name (e.g., eth1) which a bridge is
attached to; the second parameter is a OpenFlow controller's IP address and port
number (e.g., 129.215.164.111:6633). Before the script is executed, these
parameters should be changed accordingly.

For flowmon, \<k\> is the number of interfaces that a switch has in a *k*-ary
fat-tree topology and \<interface name\> refers to a name of a local interface.
For example, with k=4 and local interface is vnet0, run ./flowmon 4 vnet0.

For agent.py, \<config file\> is a PathDump host configuration file. An example
configuration file (pathdump.cfg) is in config/host. This configuration file is
copied to the specified installation directory during the installation process.

## Dependency

The installation script attempts to install all of the required software
packages. Details of the required software packages and Python packages are as
follows:

* MongoDB (>= 3.0.6)
* MongoDB Legacy C++ Driver 1.1.2
* ZeroMQ (ZMQ) library
* ZMQ C++ binding
* Open vSwitch 2.3.90 (branch name: abcf3ef4c3f75963f46a11501685363e3ceb7c0e)
* Python Flask package (Flask)
* Python Watchdog package (watchdog)
* Python YAML package (pyyaml)
* Python ZMQ binding package (pyzmq)
* tcpretrans perl script in Perf-tools (https://github.com/brendangregg/perf-tools)

External Python packages (Flask, watchdog, pyyaml, and pyzmq) are installed
using pip during the installation process.

## Additional notes

The OVS kernel module is patched and tested on Ubuntu 12.04.5 LTS (Kernel
version: 3.13.0-32-generic).

The 'tcpretrans' perl script is only used from the Perf-tools package. Hence,
instead of installing the whole package, the perl script is already included in
the PathDump source base.
