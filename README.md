PathDump
========

## Building PathDump

## Dependency
* Python 2.7+
* Linux Kernel 3.x <-- Fix me!
* Open vSwitch 2.3.90 <-- Fix me!: http://openvswitch.org/
* MongoDB: https://www.mongodb.org/
* MongoDB Legacy C++ Driver 1.0.6: https://github.com/mongodb/mongo-cxx-driver/releases/tag/legacy-1.0.6
* YAML: https://github.com/jbeder/yaml-cpp/releases/tag/release-0.5.3
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
       |--FlowMonitor (OVS kernel -> user space -> DB go here)
       |--API (Query processing)
           |--Apps
             |-- Alerts
	     |-- MapReduce
|-- examples
|-- lib
|-- conf
|-- README.md
|-- LICENSE
```
