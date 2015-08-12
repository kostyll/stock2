from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw
from main.msgs import notify_email
from main.models import CryptoTransfers, Currency, Accounts, crypton_in,get_decrypted_user_pin
from sdk.crypto import CryptoAccount
from  crypton import settings 
from sdk.crypto_settings import Settings as CryptoSettings
import sys
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
from main.my_cache_key import my_lock, my_release, LockBusyException
import os
import sys
from main.global_check import * 
from blockchain.wallet import Wallet
import blockchain.util
from blockchain.exceptions import APIException
import urllib2 
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
        lock = my_lock(LOCK)
        try:
                process_out(CurrencyTitle)
                my_release(lock)
        except LockBusyException as e:
                    print "operation is locked", e.value
        except urllib2.HTTPError:
                print "url error"
                my_release(lock)
        except APIException as e:
            print e.message
            if not e.message.startswith(u"Insufficient Funds"):
                print "release lock"
                my_release(lock)
        except:
            print "Unexpected error:", str(sys.exc_info())

def process_out(CurrencyTitle):
        blockchain.util.TIMEOUT = 160
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        if not check_btc_balance() or check_global_lock():
            raise LockBusyException("global check crypto currency has raised")

        Crypton = Wallet(CryptoSettings["BTC"]["host"],
                         CryptoSettings["BTC"]["rpc_user"],
                         CryptoSettings["BTC"]["rpc_pwd"])#sys.exit(0)
        getcontext().prec = settings.TRANS_PREC
        for obj in CryptoTransfers.objects.filter(status="processing", 
                                                  debit_credit ="out",
                                                  currency = CurrencyInstance):

                Amnt  =  int(obj.amnt*100000000)
                print "sending funds of %s to %s amount %i"  % (obj.user.username,  obj.account, Amnt)
                if 1 and not obj.verify(get_decrypted_user_pin(obj.user)):
                                print "SALT FAILED"
                                continue
                    else:
                                print "Salt ok"

                obj.status = "processed"
                obj.user_accomplished = user_system               
                obj.save()
                Account = obj.account
                Account = clean(Account)                     
                Txid = Crypton.send(Account, Amnt )
                print "txid %s" % (Txid.tx_hash)
                obj.order.status = "processed"
                obj.order.save()                       
                obj.crypto_txid = Txid.tx_hash
                obj.save()
                notify_email(obj.user, "withdraw_notify", obj)


def clean(d):
        d = d.replace(" ","")
        return ''.join([i if ord(i) < 128 else '' for i in d])
