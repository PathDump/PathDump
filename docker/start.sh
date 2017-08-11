/usr/bin/mongod --fork --logpath /var/log/mongodb.log
cd /code/host/test
python push_to_mongo.py
cd /code/host/pathdump_host
python agent.py pathdump.cfg
