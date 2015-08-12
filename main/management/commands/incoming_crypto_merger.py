from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw

from main.models import CryptoTransfers, Currency, Accounts, crypton_in
from sdk.crypto import CryptoAccount
import crypton.settings 
from sdk.crypto_settings import Settings as CryptoSettings

from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
import os
import sys

from main.my_cache_key import my_lock, my_release, LockBusyException


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        try :
              Time = args[0]    
              Time = int(Time)
        except :
              Time = 0 
	print "process  time %i" % ( Time) 
	LOCK = "in_cryptoblck_info"
	LOCK = LOCK 
	lock = None
	try:
      		lock = my_lock(LOCK)
		
		for CurrencyTitle in  CryptoSettings.keys():
			
			print "start proces %s" % CurrencyTitle
			if CurrencyTitle !="BTC":
				process_in_crypto(Time, CurrencyTitle)
	except :
		print "Unexpected error:", sys.exc_info()[0]	
        finally:
		my_release(lock)
       
def process_in_crypto(Time, CurrencyTitle):
	       
        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
        List = Crypton.listtransactions()
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        getcontext().prec = crypton.settings.TRANS_PREC
        for trans in List :
                Txid = trans["txid"]
	#	print "receive transactions %s" % (str(trans))
                if  trans.has_key("blocktime")  and trans["blocktime"]<Time:
#			print "old transactions ";
#			print "blocktime is %i " % trans["blocktime"]
                        continue

		#if trans["amount"]<0.0001:
		#	continue  
                if trans["category"] == "receive":
                        Account  = None
                        Trans = None
			New = False
                        Decimal = format_numbers_strong(trans["amount"])
                        try :
                               Account  = Accounts.objects.get(reference = trans["address"])  
                               Trans = CryptoTransfers.objects.get( crypto_txid = Txid, currency = CurrencyInstance )  
                        except Accounts.DoesNotExist:
#                               notify_admin_withdraw(u"unrecognized crypto incoming to %s %s %s" % (trans["address"],
 #                                                                                                    Decimal,
  #                                                                                                   CurrencyTitle
   #                                                                                                  ) ) 
                               continue
                        except  CryptoTransfers.DoesNotExist:
				Trans =  CryptoTransfers(crypto_txid = Txid,
                                                                        status="created",
                                                                        amnt = Decimal,
                                                                        currency = CurrencyInstance ,
                                                                        account = trans["address"],
                                                                        user = Account.user,
									confirms = 0)
				
				Trans.save()	
				print "in one trans to our accounts"
                        	print "#%i receive %s to %s amount of %s" % (Trans.id ,Txid, trans["address"], trans['amount'] )
        #                print "confirmations %i" % (trans["confirmations"] )                        
        #                print "this trans is %s" % (Trans.status)
                        if (Trans.status == "processing" or Trans.status == "created" ) and trans["confirmations"] > CryptoSettings[CurrencyTitle]["min_confirmation"]:
                                print "processing it %s" % (str(trans))
                                Trans.confirms = int(trans["confirmations"])
                                Trans.status = "processing"
                                Trans.save()
#				print "in in"
                                crypton_in(Trans, user_system)
                                
                        if Trans.status == "processing" or Trans.status == "created":     
 #                               print "update confirmations"
                                Trans.status = "processing"
                                Trans.confirms = int(trans["confirmations"])
                                Trans.save()
        
