wget <url to mongo-cxx-driver-1.1.2.zip>
unzip mongo-cxx-driver-legacy-1.1.2.zip 
cd mongo-cxx-driver
sudo scons --prefix /usr/local --c++11=on install
cd ../
git clone https://github.com/zeromq/libzmq
mkdir cmake-build && cd cmake-build
cmake .. && make -j 4
make test && sudo make install && sudo ldconfig
cd ../..
git clone https://github.com/zeromq/cppzmq
cd cppzmq && sudo cp zmq.hpp zmq_addon.hpp /usr/local/include/
cd ../
sudo pip install pyyaml
sudo pip install watchdog
