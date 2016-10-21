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


## Dependency

The installation script attempts to install all of the required software
packages. The following software packages and Python packages are required:

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
instead of installing the whole package, we only include the perl script in the
PathDump source base.

An example configuration file is config/host/pathdump.cfg. This configuration
file is copied to the specified installation directory during the installation
process.