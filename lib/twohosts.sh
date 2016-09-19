	
  del_bridges() {
	ovs-vsctl del-br br0

}

  del_flows() {
	ovs-ofctl del-flows br0
	}

	
  add_bridges() {
	ovs-vsctl add-br br0
	
	
        #ovs-vsctl set-controller br0 tcp:129.215.91.10:6653
        ovs-vsctl set-controller br0 tcp:129.215.164.111:6633

	
	
	ovs-vsctl add-port br0 eth1
	ovs-vsctl add-port br0 vnet0 -- set interface vnet0 type=internal
		
}
  add_cust_flows1() {
	ovs-ofctl add-flow br0 in_port=1,arp,actions=output:2
	ovs-ofctl add-flow br0 in_port=2,arp,actions=output:1
	ovs-ofctl add-flow br0 in_port=1,ip,actions=output:2
	ovs-ofctl add-flow br0 in_port=2,ip,actions=output:1
	}

  add_cust_flows2() {
        ovs-ofctl add-flow br0 in_port=19,ip,actions=output:1
        ovs-ofctl add-flow br0 in_port=20,ip,actions=output:1
        ovs-ofctl add-flow br0 in_port=21,ip,actions=output:1
        ovs-ofctl add-flow br0 in_port=22,ip,actions=output:1
        ovs-ofctl add-flow br0 in_port=1,ip,nw_dst=10.1.1.2,actions=output:19
        ovs-ofctl add-flow br0 in_port=1,ip,nw_dst=10.1.1.3,actions=output:20
        ovs-ofctl add-flow br0 in_port=1,ip,nw_dst=10.1.2.2,actions=output:21
        ovs-ofctl add-flow br0 in_port=1,ip,nw_dst=10.1.2.3,actions=output:22
        }
  


# Usage info
   show_help() {
   cat << EOF
    
       -d          delete bridges
       -o          delete flows 	     		
       -b          add bridges,ports
       -f	   add flows
       -c	   add strip vlan cust flows for vnet1
       -v          add strip vlan cust flows for VM 	
       -a	   install simple topology
EOF
  }
   
  # Initialize our own variables:
  while getopts "hdobfacv" opt; do
       case "$opt" in
           h)  show_help
	       exit 0
	       ;;	
	   d)  del_bridges
               exit 0
               ;;
           o)  del_flows
               exit 0
               ;;
           b)  add_bridges
               exit 0
               ;;
           f)  add_flows
               exit 0 
               ;;
	   c)  add_cust_flows1
	       exit 0
	       ;;	
	   v)  add_cust_flows2
	       exit 0
	       ;;	
	   a)  del_bridges
	       add_bridges
	       del_flows
	       add_cust_flows
	       exit 0
	       ;;
       esac
   done

