#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT

if [ "$MODE"x == "test"x ];then
    while [ true ];do
        nohup /usr/bin/python3 main.py >> log/run.log 2>&1
        sleep 86400000
    done
else
    exec /usr/bin/python3 main.py >> log/run.log 2>&1
fi
