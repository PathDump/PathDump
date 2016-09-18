PathDump
========

## Building PathDump

## Dependency
* Python 2.7+
* Linux Kernel 3.x <-- Fix me!
* Open vSwitch 2.3.90 <-- Fix me!: http://openvswitch.org/
* MongoDB: https://www.mongodb.org/
* MongoDB Legacy C++ Driver 1.1.2: https://github.com/mongodb/mongo-cxx-driver/releases/tag/legacy-1.1.2
* YAML: https://github.com/jbeder/yaml-cpp
* libzmq: https://github.com/zeromq/libzmq 
* Flask: http://flask.pocoo.org/
* Ryu: http://osrg.github.io/ryu/
* Perf-tools: https://github.com/brendangregg/perf-tools
* 

## Folder structure
```
|-- src
    |-- controller
    |-- host
       |--ovs-patch (OVS kernel -> user space)
       |--flow-mon (user space -> DB go here)
       |--query-agent (API's)
|-- examples
|-- lib
|-- conf
|-- README.md
|-- LICENSE
```

## Mongodb build and install instructions 
* Download mongo-cxx-driver-legacy-1.1.2.zip 
```
unzip mongo-cxx-driver-legacy-1.1.2.zip 
cd mongo-cxx-driver
sudo scons --prefix /usr/local --c++11=on install
```
## Lib zeromq for c++ build and install instructions
```
git clone https://github.com/zeromq/libzmq
mkdir cmake-build && cd cmake-build
cmake .. && make -j 4
make test && make install && sudo ldconfig
git clone https://github.com/zeromq/cppzmq
cd cppzmq && sudo cp zmq.hpp zmq_addon.hpp /usr/local/include/
```
