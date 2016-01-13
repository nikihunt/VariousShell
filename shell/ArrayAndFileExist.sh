#!/bin/sh
logfile=debug.log
filename=targetquerystr
array=("user_channel" "entry" "topic" "source" "local" "video" "audio" "picture" "editor_select")


for var in ${array[@]};
do
    if [ ! -d "${var}.data" ];then
        `tail -f $logfile | grep $var | head -n 1 > ${var}.data `
    fi
done
