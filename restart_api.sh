#!/bin/sh
kill `cat manage_api.pid`
#openssl des3 -d -in settings2.des3 -out crypton/settings.py
#uwsgi --ini uwsgi_api.ini
<<<<<<< HEAD
python ./manage.py runfcgi host=0.0.0.0 port=8367 daemonize=true maxspare=4 pidfile=/home/btctrade/stock/manage_api.pid
=======
python ./manage.py runfcgi host=0.0.0.0 port=8367 daemonize=true maxspare=4 pidfile=/home/btc_trade/stock2/manage_api.pid
>>>>>>> 137e852afcc19395c1c41f4212fde52f31cbc0a7
#rm crypton/settings.py
