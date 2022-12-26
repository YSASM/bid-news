#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
echo "[program:News]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9260 run:editor" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
echo "stdout_logfile = /app/log/api_run.log" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
supervisorctl start News
if [ "$MODE"x == "test"x ];then
    while [ true ];do
        nohup /usr/bin/python3 run.py >> log/run.log 2>&1
        sleep 86400000
    done
else
    exec /usr/bin/python3 run.py >> log/run.log 2>&1
fi
