#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Please specify the home directory for PathDump"
    exit 1
fi

home=$1

if [ ! -d "$home" ]; then
    mkdir $home
fi

mkdir tmpbuild
pushd tmpbuild

# Install steps for mongo-cxx (note: mongo-c and libbson dependency is there)
wget https://github.com/mongodb/mongo-cxx-driver/archive/legacy-1.1.2.zip
unzip legacy-1.1.2.zip 
pushd mongo-cxx-driver-legacy-1.1.2
sudo scons --prefix /usr/local --c++11=on install
popd

# Install steps for libzmq
git clone https://github.com/zeromq/libzmq
pushd libzmq
./autogen.sh
./configure     # add other options here
make
make check
sudo make install
sudo ldconfig
popd

#zmq cpp binding installation
git clone https://github.com/zeromq/cppzmq
pushd cppzmq && sudo cp zmq.hpp zmq_addon.hpp /usr/local/include/
popd
sudo pip install pyyaml
sudo pip install watchdog
sudo pip install pyzmq

# ovs checkout to older version, applies patch and then build
git clone https://github.com/openvswitch/ovs.git
pushd ovs
git checkout abcf3ef4c3f75963f46a11501685363e3ceb7c0e
git apply ../../ovs/ovs-linux-kernel.patch
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make -j 8
make modules_install
popd

popd

pushd flow-mon
make
popd

cp -f ./query-agent/* $home
cp -f ./flow-mon/bin/flowmon $home
cp -f ./ovs/*.sh $home
cp -f ./tmpbuild/ovs/datapath/linux/openvswitch.ko $home
cp -f ../config/host/pathdump.cfg $home
