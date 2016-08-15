PathDump
========

## Building PathDump

## Dependency
* Python 2.7+
* Linux Kernel 3.x <-- Fix me!
* Open vSwitch 2.x <-- Fix me!: http://openvswitch.org/
* MongoDB: https://www.mongodb.org/
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
