from django.core.management.base import BaseCommand, CommandError
from main.models import Orders, TradePairs
from main.tornado.api import return_rest2acc, order_finish
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
        process_small_orders()


def process_small_orders():
    for CurrentTradePair in TradePairs.objects.filter(status="processing"):

        for item in Orders.objects.filter(trade_pair=CurrentTradePair, status="processing"):
            if item.currency1 == CurrentTradePair.currency_on:

                return_rest2acc(item, item.sum1)
                item.sum1 = 0
                item.status = "processed"
                item.save()
            else:

                return_rest2acc(item, item.sum1)
                item.sum1 = 0
                item.status = "processed"
                item.save()
                 
                 
