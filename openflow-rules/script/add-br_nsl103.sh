ovs-vsctl add-br br9 -- set bridge br9 datapath_type=pica8 other-config=datapath-id=0000000000000009
ovs-vsctl set-controller br9 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br9 protocols=OpenFlow13
ovs-vsctl add-port br9 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br9 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br9 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br9 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br10 -- set bridge br10 datapath_type=pica8 other-config=datapath-id=000000000000000A
ovs-vsctl set-controller br10 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br10 protocols=OpenFlow13
ovs-vsctl add-port br10 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br10 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br10 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br10 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
ovs-vsctl add-br br11 -- set bridge br11 datapath_type=pica8 other-config=datapath-id=000000000000000B
ovs-vsctl set-controller br11 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br11 protocols=OpenFlow13
ovs-vsctl add-port br11 ge-1/1/9 vlan_mode=trunk -- set interface ge-1/1/9 type=pica8
ovs-vsctl add-port br11 ge-1/1/10 vlan_mode=trunk -- set interface ge-1/1/10 type=pica8
ovs-vsctl add-port br11 ge-1/1/11 vlan_mode=trunk -- set interface ge-1/1/11 type=pica8
ovs-vsctl add-port br11 ge-1/1/12 vlan_mode=trunk -- set interface ge-1/1/12 type=pica8
ovs-vsctl add-br br12 -- set bridge br12 datapath_type=pica8 other-config=datapath-id=000000000000000C
ovs-vsctl set-controller br12 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br12 protocols=OpenFlow13
ovs-vsctl add-port br12 ge-1/1/13 vlan_mode=trunk -- set interface ge-1/1/13 type=pica8
ovs-vsctl add-port br12 ge-1/1/14 vlan_mode=trunk -- set interface ge-1/1/14 type=pica8
ovs-vsctl add-port br12 ge-1/1/15 vlan_mode=trunk -- set interface ge-1/1/15 type=pica8
ovs-vsctl add-port br12 ge-1/1/16 vlan_mode=trunk -- set interface ge-1/1/16 type=pica8
