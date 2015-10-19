from django.core.management.base import BaseCommand, CommandError
from main.models import Orders, TradePairs
from main.api import return_rest2acc, order_finish
from  main.msgs import system_notify
from django.db import connection
from datetime import datetime
from decimal import getcontext
import sys

from main.my_cache_key import my_lock, my_release, LockBusyException


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        URL_TITLE = args[0]
        LOCK = "small_orders"
        LOCK += URL_TITLE
        lock = my_lock(LOCK)
        print "small orders "
        print "============================="
        try:
            lock = my_lock(LOCK)
            process_small_orders(URL_TITLE)
        except LockBusyException as e:
            print "operation is locked", e.value
        except:
            print "Unexpected error:", str(sys.exc_info())

        my_release(lock)


def process_small_orders(TradePairUrl):
    CurrentTradePair = TradePairs.objects.get(url_title=TradePairUrl)
    for item in Orders.objects.filter(trade_pair=CurrentTradePair, status="processing"):
        if item.currency1 == CurrentTradePair.currency_on:

            if item.sum1 < CurrentTradePair.min_trade_base:
                system_notify(order_finish(item), item.user)
                return_rest2acc(item, item.sum1)
                item.sum1 = 0
                item.status = "processed"
                item.save()
        else:

            if item.sum2 < CurrentTradePair.min_trade_base:
                system_notify(order_finish(item), item.user)
                return_rest2acc(item, item.sum1)
                item.sum1 = 0
                item.status = "processed"
                item.save()
                
                 
                 
