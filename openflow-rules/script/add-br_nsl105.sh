ovs-vsctl add-br br1 -- set bridge br1 datapath_type=pica8 other-config=datapath-id=0000000000000001
ovs-vsctl set-controller br1 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br1 protocols=OpenFlow13
ovs-vsctl add-port br1 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br1 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br1 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br1 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br2 -- set bridge br2 datapath_type=pica8 other-config=datapath-id=0000000000000002
ovs-vsctl set-controller br2 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br2 protocols=OpenFlow13
ovs-vsctl add-port br2 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br2 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br2 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br2 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
ovs-vsctl add-br br3 -- set bridge br3 datapath_type=pica8 other-config=datapath-id=0000000000000003
ovs-vsctl set-controller br3 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br3 protocols=OpenFlow13
ovs-vsctl add-port br3 ge-1/1/9 vlan_mode=trunk -- set interface ge-1/1/9 type=pica8
ovs-vsctl add-port br3 ge-1/1/10 vlan_mode=trunk -- set interface ge-1/1/10 type=pica8
ovs-vsctl add-port br3 ge-1/1/11 vlan_mode=trunk -- set interface ge-1/1/11 type=pica8
ovs-vsctl add-port br3 ge-1/1/12 vlan_mode=trunk -- set interface ge-1/1/12 type=pica8
ovs-vsctl add-br br4 -- set bridge br4 datapath_type=pica8 other-config=datapath-id=0000000000000004
ovs-vsctl set-controller br4 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br4 protocols=OpenFlow13
ovs-vsctl add-port br4 ge-1/1/13 vlan_mode=trunk -- set interface ge-1/1/13 type=pica8
ovs-vsctl add-port br4 ge-1/1/14 vlan_mode=trunk -- set interface ge-1/1/14 type=pica8
ovs-vsctl add-port br4 ge-1/1/15 vlan_mode=trunk -- set interface ge-1/1/15 type=pica8
ovs-vsctl add-port br4 ge-1/1/16 vlan_mode=trunk -- set interface ge-1/1/16 type=pica8
