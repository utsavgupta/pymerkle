#!/usr/bin/sh

if [ "$1" = "server" ]
then
    python2.7 src/server.py
elif [ "$1" = "client" ]
then
    python2.7 src/client.py
else
    echo "usage: sh script.sh [server/client]"
    exit 1
fi


   
