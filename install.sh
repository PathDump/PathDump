# Install steps for mongo-cxx (note: mongo-c and libbson dependency is there)
wget https://github.com/mongodb/mongo-cxx-driver/archive/legacy-1.1.2.zip
unzip legacy-1.1.2.zip 
cd mongo-cxx-driver-legacy-1.1.2
sudo scons --prefix /usr/local --c++11=on install
cd ../
# Install steps for libzmq
git clone https://github.com/zeromq/libzmq
cd libzmq
./autogen.sh
./configure     # add other options here
make
make check
sudo make install
sudo ldconfig
cd ../
#zmq cpp binding installation
git clone https://github.com/zeromq/cppzmq
cd cppzmq && sudo cp zmq.hpp zmq_addon.hpp /usr/local/include/
cd ../
sudo pip install pyyaml
sudo pip install watchdog
sudo pip install pyzmq
# ovs checkout to older version, applies patch and then build
git clone https://github.com/openvswitch/ovs.git
cd ovs
git checkout abcf3ef4c3f75963f46a11501685363e3ceb7c0e
git apply ../../host/ovs-patch/ovs-linux-kernel.diff
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make -j 8

