#!/bin/bash
#
# This script creates and configures a bridge.
#
# Caveat: The script is written for a testbed at the University of Edinburgh.
# Depending on the conditions (e.g., topology, # of servers, etc.) of a test
# network, this script may need modification or users need to write their own
# script. At a minimum, there are two parameters that reqiures attention. The
# first parameter is a physical interface name (e.g., eth1) which a bridge is
# attached to; the second parameter is a OpenFlow controller's IP address and
# port number (e.g., 129.215.164.111:6633). Before this script is executed,
# these parameters should be changed accordingly.
#

declare -A name_to_ip
declare -A ip_to_mac

name_to_ip=(
    ["nsl003"]="10.1.1.2" ["nsl004"]="10.1.1.3"
    ["nsl005"]="10.1.2.2" ["nsl006"]="10.1.2.3"
    ["nsl007"]="10.2.1.2" ["nsl008"]="10.2.1.3"
    ["nsl009"]="10.2.2.2" ["nsl010"]="10.2.2.3"
    ["nsl011"]="10.3.1.2" ["nsl012"]="10.3.1.3"
    ["nsl013"]="10.3.2.2" ["nsl014"]="10.3.2.3"
    ["nsl015"]="10.4.1.2" ["nsl016"]="10.4.1.3"
    ["nsl017"]="10.4.2.2" ["nsl018"]="10.4.2.3"
)

ip_to_mac=(
    ["10.1.1.2"]="9a:b0:ad:56:d9:34" ["10.1.1.3"]="ee:3d:17:22:dc:2d"
    ["10.1.2.2"]="d6:a7:d3:02:9c:bd" ["10.1.2.3"]="fa:68:47:42:43:a1"
    ["10.2.1.2"]="82:91:b7:5a:63:28" ["10.2.1.3"]="2e:84:54:c3:76:d1"
    ["10.2.2.2"]="36:d5:29:59:63:2b" ["10.2.2.3"]="be:6c:7d:62:31:31"
    ["10.3.1.2"]="1e:ca:c3:13:44:43" ["10.3.1.3"]="f6:a6:11:17:44:36"
    ["10.3.2.2"]="06:70:d7:82:29:d0" ["10.3.2.3"]="ba:13:cf:89:66:18"
    ["10.4.1.2"]="6e:47:a6:68:df:fb" ["10.4.1.3"]="3e:ff:e6:a4:1e:1f"
    ["10.4.2.2"]="f6:2c:99:73:fc:d6" ["10.4.2.3"]="4e:b3:0c:da:61:23"
)

setup()
{
    ovs-vsctl add-br br0
    # set controller
    ovs-vsctl set-controller br0 tcp:129.215.164.111:6633
    ovs-vsctl add-port br0 eth1
    ovs-vsctl add-port br0 vnet0 -- set interface vnet0 type=internal

    ovs-ofctl add-flow br0 in_port=1,arp,actions=output:2
    ovs-ofctl add-flow br0 in_port=2,arp,actions=output:1
    ovs-ofctl add-flow br0 in_port=1,ip,actions=output:2
    ovs-ofctl add-flow br0 in_port=2,ip,actions=output:1

    ip=${name_to_ip[$HOSTNAME]}
    macaddr=${ip_to_mac[$ip]}
    echo $ip $macaddr

    # ifconfig eth1 down
    ifconfig vnet0 up
    ifconfig vnet0 $ip
    ifconfig vnet0 hw ether $macaddr

    for ip in "${!ip_to_mac[@]}"; do
        macaddr=${ip_to_mac[$ip]}
        arp -s $ip $macaddr dev vnet0
    done
}

reset()
{
    ovs-ofctl del-flows br0
    ovs-vsctl del-br br0
}

# Usage info
show_help()
{
    cat << EOF
       -h    this menu
       -s    set up bridge and flow rules
       -r    delete bridge and flow rules
EOF
}

while getopts "hsr" opt; do
    case "$opt" in
        h)  show_help
	    exit 0
	    ;;	
	s)  setup
            exit 0
            ;;
        r)  reset
            exit 0
            ;;
    esac
done
