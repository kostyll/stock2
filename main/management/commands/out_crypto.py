from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw
from main.msgs import notify_email
from main.models import CryptoTransfers, Currency, Accounts, crypton_in, get_decrypted_user_pin
from sdk.crypto import CryptoAccount
import crypton.settings 
from sdk.crypto_settings import Settings as CryptoSettings
import sys
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
from main.my_cache_key import my_lock, my_release, LockBusyException
import os
import sys
from main.global_check import * 


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        CurrencyTitle = args[0]    
        
        try :
              Time = int(Time)
        except :
              Time = 0  

        LOCK = "out_crypto"
        LOCK +=  CurrencyTitle
        lock = None
        try:
                lock = my_lock(LOCK)
                process_out(CurrencyTitle)
                my_release(lock)
        except LockBusyException as e:
                print "operation is locked", e.value
                sys.exit(0)
        except:
                print "Unexpected error:", str(sys.exc_info())

def process_out(CurrencyTitle):

        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        if  check_global_lock():
            raise LockBusyException("global check crypto currency has raised")

        getcontext().prec = crypton.settings.TRANS_PREC
        for obj in CryptoTransfers.objects.filter(status="processing", 
                                                  debit_credit ="out",
                                                  currency = CurrencyInstance):
               print "sending funds of %s to %s amount %s"  % (obj.user.username,  obj.account, obj.amnt)

               if not obj.verify(get_decrypted_user_pin(obj.user)):
                    print "SALT FAILED"
                    continue
                else:
                    print "Salt ok"
                    obj.status = "processed"
                    obj.user_accomplished = user_system               
                    obj.save()
                    obj.order.status = "processed"                      
                    Txid = Crypton.sendto(obj.account, float(obj.amnt))
                    print "txid %s" % (Txid) 
                    obj.order.save()                       
                    obj.crypto_txid = Txid
                    obj.save()
                    notify_email(obj.user, "withdraw_notify", obj)

