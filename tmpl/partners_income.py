from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from main.models import CryptoTransfers, PoolAccounts, Currency, Accounts, crypton_in
import crypton.settings 

from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
import sys

from main.my_cache_key import my_lock, my_release, LockBusyException


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        
        LOCK = "partners_pay"
        LOCK = LOCK
        lock = my_lock(LOCK)
        try:
            process_partners_program()
        except :
            print "Unexpected error:", sys.exc_info()[0]    
        
        my_release(lock)
       
def process_partners_program():
    
    
    
     
