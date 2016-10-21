#!/bin/bash

# install external python packages using pip
pip install Flask
pip install watchdog

if [ "$#" -ne 1 ]; then
    echo "Please specify the home directory for PathDump"
    exit 1
fi

home=$1

if [ ! -d "$home" ]; then
    mkdir $home
fi

cp -f *.py $home
cp -f ../config/controller/pathdump.cfg $home
cp -f ../config/controller/grouptree.json $home
