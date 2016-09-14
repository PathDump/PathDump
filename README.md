PathDump
========

## Building PathDump

## Dependency
* Python 2.7+
* Python Watchdog module 0.8.3
* Linux Kernel 3.x <-- Fix me!
* Open vSwitch 2.3.90: http://openvswitch.org/
* MongoDB: https://www.mongodb.org/
* MongoDB Legacy C++ Driver 1.1.2: https://github.com/mongodb/mongo-cxx-driver/releases/tag/legacy-1.1.2
* Flask: http://flask.pocoo.org/
* Ryu: http://osrg.github.io/ryu/
* Perf-tools: https://github.com/brendangregg/perf-tools

## Folder structure
```
|-- controller
|-- host
   |--ovs-patch
   |--flow-mon
   |--query-agent
|-- examples
|-- conf
|-- README.md
|-- LICENSE
```

## Required package installation instructions
* MongoDB build
```
unzip mongo-cxx-driver-legacy-1.1.2.zip 
cd mongo-cxx-driver
sudo scons --prefix /usr/local --c++11=on install
```

* Python Watchdog module
```
pip install watchdog
```

