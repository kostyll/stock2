#!/bin/sh
kill `cat manage_api.pid`
#openssl des3 -d -in settings2.des3 -out crypton/settings.py
#uwsgi --ini uwsgi_api.ini
python ./manage.py runfcgi host=0.0.0.0 port=8367 daemonize=true maxspare=4 pidfile=/home/btctrade/stock/manage_api.pid
#rm crypton/settings.py
