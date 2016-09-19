ovs-vsctl add-br br19 -- set bridge br19 datapath_type=pica8 other-config=datapath-id=0000000000000013
ovs-vsctl set-controller br19 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br19 protocols=OpenFlow13
ovs-vsctl add-port br19 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br19 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br19 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br19 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br20 -- set bridge br20 datapath_type=pica8 other-config=datapath-id=0000000000000014
ovs-vsctl set-controller br20 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br20 protocols=OpenFlow13
ovs-vsctl add-port br20 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br20 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br20 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br20 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
