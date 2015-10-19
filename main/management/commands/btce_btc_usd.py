from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db.models import Max
from main.models import btce_trade_stat_minute_usd
import urllib2
import time
import json
import sys
import socket

# Commenting the following line out removes the bug
from main.my_cache_key import my_lock, my_release, LockBusyException
# python ./manage.py btce_btc_usd https://btc-e.com/api/2/btc_usd/trades  btc_usd 10
class Command(BaseCommand):
    args = ''
    help = 'gathering btc-e stat'

    def handle(self, *args, **options):
        Url = args[0]
        Type = args[1]

        socket.setdefaulttimeout(10)
        LOCK = "btce"
        LOCK = LOCK + Type
        Lock = my_lock(LOCK)
        try:
            Decoder = json.JSONDecoder()
            Last = btce_trade_stat_minute_usd.objects.all().aggregate(Max('btc_tid'))
            # Last{'unixtime__max': None}
            if Last["btc_tid__max"] is None:
                Last = 0
            else:
                Last = Last["btc_tid__max"]
            bulk_add = []

            D = urllib2.urlopen(Url, timeout=10)
            Str = D.read()

            Res = Decoder.decode(Str)
            Res.reverse()

            for i in Res:

                if i['tid'] > Last:
                    Last = i['tid']
                    generated_date = datetime.fromtimestamp(int(i['date']))
                    bulk_add.append(btce_trade_stat_minute_usd(unixtime=i['date'],
                                                               amount=i['amount'],
                                                               price=i['price'],
                                                               ask_bid=i['trade_type'],
                                                               datetime=generated_date,
                                                               btc_tid=Last,
                                                               stock_type=Type
                    ))

            btce_trade_stat_minute_usd.objects.bulk_create(bulk_add)
            d = len(bulk_add)
            print "add %i" % (d)
        except:
            print "Unexpected error:", sys.exc_info()[0]
        my_release(Lock)
        sys.exit(0)
            
                                





