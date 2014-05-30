#!/bin/bash
while [ true ]
do
    RUNNING=`netstat | grep -v localhost | egrep 'fcserver.*ESTABLISHED' | wc -l`
    LOCAL=`lsof | egrep 'localhost.*localhost:fcserver.*ESTABLISHED' | wc -l`
    if [ $RUNNING -gt 1 ]
    then
        /usr/local/bin/pulse-restart-fcserver
        echo "too many streams!" > /tmp/fcserver.status
    elif [ $RUNNING -eq 1 ]
    then
        if [ $LOCAL -gt 0 ]
        then
            echo "killing local streams" > /tmp/fcserver.status
            /usr/local/bin/pulse-killall-local-streams
        else
            echo "controlled by foreign host" > /tmp/fcserver.status
        fi
    else
        if [ $LOCAL -gt 1 ]
        then
            echo "too many local streams" > /tmp/fcserver.status
            /usr/local/bin/pulse-killall-local-streams
        elif [ $LOCAL -eq 0 ]
        then
            echo "no streams" > /tmp/fcserver.status
            /usr/local/bin/pulse-start-script lava_lamp.py
        else
            echo "running local stream" > /tmp/fcserver.status
        fi
    fi
   sleep 3
done
