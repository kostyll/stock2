from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw
from main.msgs import notify_email
from main.models import CryptoTransfers, Currency, Accounts, crypton_in, add_trans
from sdk.crypto import CryptoAccount
import crypton.settings 
from sdk.crypto_settings import Settings as CryptoSettings
import sys
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
from main.my_cache_key import my_lock, my_release, LockBusyException
from main
import os
import sys
from main.global_check import check_crypto_currency 


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
	excet:
	    print "Unexpected error:", str(sys.exc_info())



def process_out(CurrencyTitle):

        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
        user_system = User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        if not check_crypto_currency(CurrencyInstance) :
            raise LockBusyException("global check crypto currency has raised")
	
#sys.exit(0)
        getcontext().prec = crypton.settings.TRANS_PREC
        for obj in CryptoTransfers.objects.filter(status="processing", 
                                                  debit_credit ="out",
                                                  currency = CurrencyInstance):
                
               print "sending funds of %s to %s amount %s"  % (obj.user.username,  obj.account, obj.amnt)
               # TODO user private keys
               UserPrivateKey  =
               if not obj.verify( UserPrivateKey ):
                    print "SIGN FAILED"
                    continue


               obj.status = "processed"
               obj.user_accomplished = user_system               
               obj.save()
               obj.order.status = "processed"                      
               obj.order.save() 
               Txid = None

               try:
                    InnerAccount = Accounts.objects.get( reference = obj.account )
                    Txid = "Move between accounts"
                    add_trans( obj.order.transit_1 , obj.order.sum1, obj.order.currency1,
                                InnerAccount, order, 
                                "payin", None )
                    
               except Accounts.DoesNotExist:
                    Txid = Crypton.sendto(obj.account, float(obj.amnt))
                    
               print "txid %s" % (Txid) 
                                     
               obj.crypto_txid = Txid
               obj.sign_record(crypton.settings.CRYPTO_SALT)
               obj.save()
               notify_email(obj.user, "withdraw_notify", obj)

