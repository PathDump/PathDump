#!/bin/bash

hostname=$1
docker stop pod1.$hostname.inst0
docker rm pod1.$hostname.inst0
docker stop pod1.$hostname.inst1
docker rm pod1.$hostname.inst1
docker stop pod1.$hostname.inst2
docker rm pod1.$hostname.inst2
docker stop pod1.$hostname.inst3
docker rm pod1.$hostname.inst3
weave stop
weave stop-proxy
eval $(weave env --restore)
weave launch nsl002
eval $(weave env)
docker run --name pod1.$hostname.inst0 -P -d -v /home/praveen/switchP/tool:/code -it praveen667/switchp:switchP_host /bin/bash /code/docker/start.sh
docker run --name pod1.$hostname.inst1 -P -d -v /home/praveen/switchP/tool:/code -it praveen667/switchp:switchP_host /bin/bash /code/docker/start.sh 
docker run --name pod1.$hostname.inst2 -P -d -v /home/praveen/switchP/tool:/code -it praveen667/switchp:switchP_host /bin/bash /code/docker/start.sh 
docker run --name pod1.$hostname.inst3 -P -d -v /home/praveen/switchP/tool:/code -it praveen667/switchp:switchP_host /bin/bash /code/docker/start.sh
