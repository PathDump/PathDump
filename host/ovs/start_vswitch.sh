# Below commands kill/remove (if one running) openvswitch dependencies
# (datapathmodule, userspace modules) and restarts them in /usr/local/var/run
# directory. So run this script with sudo permissions.

kill `cd /usr/local/var/run/openvswitch && cat ovsdb-server.pid ovs-vswitchd.pid`

rmmod openvswitch
modprobe libcrc32c
modprobe vxlan
modprobe gre
insmod $(pwd)/openvswitch.ko
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
             --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
             --private-key=db:Open_vSwitch,SSL,private_key \
             --certificate=db:Open_vSwitch,SSL,certificate \
             --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
             --pidfile --detach
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
