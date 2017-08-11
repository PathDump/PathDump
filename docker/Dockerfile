#Dockerizing MongoDB: Dockerfile for building MongoDB images
# Based on ubuntu:latest, installs MongoDB following the instructions from:
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

# Format: FROM    repository[:version]
FROM       ubuntu:latest

# Format: MAINTAINER Name <email@addr.ess>
MAINTAINER Praveen Tammana <praveen.tammana@ed.ac.uk>

# Installation:
# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

RUN apt-get -y install build-essential python-dev
# Install python-pip
RUN apt-get -y install python-pip
RUN pip install netaddr
RUN pip install bson
RUN pip install flask
RUN pip install pymongo
RUN apt-get -y install python-netifaces

#RUN apt-get -y install curl

#Install supervisor
#RUN apt-get -y install supervisor
#RUN mkdir -p /var/log/supervisor
#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


RUN mkdir -p /code
ADD . /code

WORKDIR /code
RUN pip install -r requirements.txt

# Expose port 27017 from the container to the host
EXPOSE 5000 


# Set usr/bin/mongod as the dockerized entry-point application
COPY start.sh /usr/local/start.sh
#CMD ["/bin/bash","/usr/local/start.sh"]
#CMD ["/usr/bin/mongod"]
#CMD ["/usr/bin/cd","/code"]
#CMD ["python","host_agent.py","docker"]


