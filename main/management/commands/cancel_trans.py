from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw
from main.msgs import notify_email
from main.models import add_trans, Trans
import sys
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext, Decimal
from main.my_cache_key import my_lock, my_release, LockBusyException
import os


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
	i = args[0]        
        obj = Trans.objects.get(id=i)		
	cancel_trans(obj)
	
def cancel_trans(obj):
        add_trans(obj.user2,
                  obj.amnt,
                  obj.currency,
                  obj.user1,
                  None,
                  "canceled",
                  obj.id,
                  False)
	
