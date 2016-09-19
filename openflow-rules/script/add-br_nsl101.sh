ovs-vsctl add-br br17 -- set bridge br17 datapath_type=pica8 other-config=datapath-id=0000000000000011
ovs-vsctl set-controller br17 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br17 protocols=OpenFlow13
ovs-vsctl add-port br17 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br17 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br17 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br17 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br18 -- set bridge br18 datapath_type=pica8 other-config=datapath-id=0000000000000012
ovs-vsctl set-controller br18 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br18 protocols=OpenFlow13
ovs-vsctl add-port br18 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br18 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br18 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br18 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
