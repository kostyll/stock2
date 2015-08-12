#!/bin/sh
kill `cat /home/btc_trade/test_crypton/manage.pid`
cd /home/btc_trade/test_crypton
/usr/bin/python ./manage.py syncdb
/usr/bin/python /home/btc_trade/test_crypton/manage.py runfcgi host=127.0.0.1 port=8366 pidfile=/home/btc_trade/test_crypton/manage.pid daemonize=true maxspare=5
