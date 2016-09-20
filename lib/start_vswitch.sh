kill `cd /usr/local/var/run/openvswitch && cat ovsdb-server.pid ovs-vswitchd.pid`
#kill `cd /run/openvswitch && cat ovsdb-server.pid ovs-vswitchd.pid`
make
make modules_install
rmmod openvswitch
modprobe libcrc32c
modprobe vxlan
modprobe gre
#insmod /home/ubuntu/pathdump/ovswitch/datapath/linux/openvswitch.ko
insmod $(pwd)/ovs/datapath/linux/openvswitch.ko
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
             --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
             --private-key=db:Open_vSwitch,SSL,private_key \
             --certificate=db:Open_vSwitch,SSL,certificate \
             --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
             --pidfile --detach
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
sleep 2
sh twohosts.sh -b
#sleep 10
sh twohosts.sh -c
ifconfig eth1 0
ifconfig vnet0 up

