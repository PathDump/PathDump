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
* ZMQ: https://github.com/zeromq/libzmq 
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
|-- config
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
* Lib zeromq for c++ build
```
git clone https://github.com/zeromq/libzmq
mkdir cmake-build && cd cmake-build
cmake .. && make -j 4
make test && make install && sudo ldconfig
git clone https://github.com/zeromq/cppzmq
cd cppzmq && sudo cp zmq.hpp zmq_addon.hpp /usr/local/include/
```
* Python Watchdog module
```
pip install watchdog
```
