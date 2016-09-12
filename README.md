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
* Flask: http://flask.pocoo.org/
* Ryu: http://osrg.github.io/ryu/
* Perf-tools: https://github.com/brendangregg/perf-tools
* 

## Folder structure
```
|-- src
    |-- controller
       |-- Network (scripts to generate switch rules)
       |-- API (Query processing)
	   |--Apps
	     |-- Alerts
	     |-- MapReduce
	     |-- Loops
    |-- host
       |--FlowMonitor (user space -> DB go here)
       |--Datapath (OVS kernel changes)
       |--API (Query processing)
|-- examples
|-- lib
|-- conf
|-- README.md
|-- LICENSE
```
### Mongodb build instructions 
# Download mongo-cxx-driver-legacy-1.1.2.zip 
unzip mongo-cxx-driver-legacy-1.1.2.zip 
cd mongo-cxx-driver
sudo scons --prefix /usr/local --c++11=on install

### Yaml build and install instruction
git clone https://github.com/jbeder/yaml-cpp.git
mkdir build
cd build/
cmake ..
make
sudo make install

