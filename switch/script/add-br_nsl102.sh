ovs-vsctl add-br br16 -- set bridge br16 datapath_type=pica8 other-config=datapath-id=0000000000000010
ovs-vsctl set-controller br16 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br16 protocols=OpenFlow13
ovs-vsctl add-port br16 ge-1/1/13 vlan_mode=trunk -- set interface ge-1/1/13 type=pica8
ovs-vsctl add-port br16 ge-1/1/14 vlan_mode=trunk -- set interface ge-1/1/14 type=pica8
ovs-vsctl add-port br16 ge-1/1/15 vlan_mode=trunk -- set interface ge-1/1/15 type=pica8
ovs-vsctl add-port br16 ge-1/1/16 vlan_mode=trunk -- set interface ge-1/1/16 type=pica8
ovs-vsctl add-br br13 -- set bridge br13 datapath_type=pica8 other-config=datapath-id=000000000000000D
ovs-vsctl set-controller br13 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br13 protocols=OpenFlow13
ovs-vsctl add-port br13 ge-1/1/1 vlan_mode=trunk -- set interface ge-1/1/1 type=pica8
ovs-vsctl add-port br13 ge-1/1/2 vlan_mode=trunk -- set interface ge-1/1/2 type=pica8
ovs-vsctl add-port br13 ge-1/1/3 vlan_mode=trunk -- set interface ge-1/1/3 type=pica8
ovs-vsctl add-port br13 ge-1/1/4 vlan_mode=trunk -- set interface ge-1/1/4 type=pica8
ovs-vsctl add-br br14 -- set bridge br14 datapath_type=pica8 other-config=datapath-id=000000000000000E
ovs-vsctl set-controller br14 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br14 protocols=OpenFlow13
ovs-vsctl add-port br14 ge-1/1/5 vlan_mode=trunk -- set interface ge-1/1/5 type=pica8
ovs-vsctl add-port br14 ge-1/1/6 vlan_mode=trunk -- set interface ge-1/1/6 type=pica8
ovs-vsctl add-port br14 ge-1/1/7 vlan_mode=trunk -- set interface ge-1/1/7 type=pica8
ovs-vsctl add-port br14 ge-1/1/8 vlan_mode=trunk -- set interface ge-1/1/8 type=pica8
ovs-vsctl add-br br15 -- set bridge br15 datapath_type=pica8 other-config=datapath-id=000000000000000F
ovs-vsctl set-controller br15 tcp:129.215.164.111:6633
ovs-vsctl -- set bridge br15 protocols=OpenFlow13
ovs-vsctl add-port br15 ge-1/1/9 vlan_mode=trunk -- set interface ge-1/1/9 type=pica8
ovs-vsctl add-port br15 ge-1/1/10 vlan_mode=trunk -- set interface ge-1/1/10 type=pica8
ovs-vsctl add-port br15 ge-1/1/11 vlan_mode=trunk -- set interface ge-1/1/11 type=pica8
ovs-vsctl add-port br15 ge-1/1/12 vlan_mode=trunk -- set interface ge-1/1/12 type=pica8
