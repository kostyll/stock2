#!/bin/sh
kill `cat /home/btctrade/stock/manage_api.pid`
python ./manage.py runfcgi host=127.0.0.1 port=8367 daemonize=true maxspare=2 pidfile=/home/btctrade/stock/manage_api.pid
