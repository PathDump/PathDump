ovs-vsctl add-br br8 -- set bridge br8 datapath_type=pica8 other-config=datapath-id=0000000000000008
ovs-vsctl set-controller br8 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br8 protocols=OpenFlow13
ovs-vsctl add-port br8 ge-1/1/13 vlan_mode=trunk -- set interface ge-1/1/13 type=pica8
ovs-vsctl add-port br8 ge-1/1/14 vlan_mode=trunk -- set interface ge-1/1/14 type=pica8
ovs-vsctl add-port br8 ge-1/1/15 vlan_mode=trunk -- set interface ge-1/1/15 type=pica8
ovs-vsctl add-port br8 ge-1/1/16 vlan_mode=trunk -- set interface ge-1/1/16 type=pica8
ovs-vsctl add-br br5 -- set bridge br5 datapath_type=pica8 other-config=datapath-id=0000000000000005
ovs-vsctl set-controller br5 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br5 protocols=OpenFlow13
ovs-vsctl add-port br5 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br5 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br5 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br5 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br6 -- set bridge br6 datapath_type=pica8 other-config=datapath-id=0000000000000006
ovs-vsctl set-controller br6 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br6 protocols=OpenFlow13
ovs-vsctl add-port br6 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br6 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br6 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br6 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
ovs-vsctl add-br br7 -- set bridge br7 datapath_type=pica8 other-config=datapath-id=0000000000000007
ovs-vsctl set-controller br7 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br7 protocols=OpenFlow13
ovs-vsctl add-port br7 ge-1/1/9 vlan_mode=trunk -- set interface ge-1/1/9 type=pica8
ovs-vsctl add-port br7 ge-1/1/10 vlan_mode=trunk -- set interface ge-1/1/10 type=pica8
ovs-vsctl add-port br7 ge-1/1/11 vlan_mode=trunk -- set interface ge-1/1/11 type=pica8
ovs-vsctl add-port br7 ge-1/1/12 vlan_mode=trunk -- set interface ge-1/1/12 type=pica8
