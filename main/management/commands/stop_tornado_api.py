from django.core.management.base import BaseCommand, CommandError
import urllib2
import time
import json
import sys
import socket
#python ./manage.py btce_btc_usd https://btc-e.com/api/2/btc_usd/trades  btc_usd 10
class Command(BaseCommand):
    args = ''
    help = 'gathering btc-e stat'
    def handle(self, *args, **options):
        Url = "http://127.0.0.1:8081/stop"
        D = urllib2.urlopen(Url, timeout=10)
        print D.read()
        
            
                                





