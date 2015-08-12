from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from main.models import PoolAccounts, Accounts, VolatileConsts, Currency, sato2Dec, CryptoTransfers, generate_private_sign

import crypton.settings
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
from blockchain import blockexplorer

import sys
import time

def is_out(Inputs, OwnAccounts ):
    
   for i in Inputs:
            if OwnAccounts.has_key( i.address ) :
               return  True
   return False
               
               
class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'
    def handle(self, *args, **options):
	import blockchain	    
	blockchain.util.TIMEOUT = 60	
        Last = None
        CurrencyInstance = Currency.objects.get(title = "BTC")
        AccountList = PoolAccounts.objects.filter(currency_id = 2 )
        OwnAccounts = {}
	print "get all addresses"
        for i in AccountList:
		if i.address=='' or i.address is None or i.user is None:
			continue 
                OwnAccounts[i.address] = i.user
        
	while True:        
            try:    
                Last  = VolatileConsts.objects.get(Name = "last_btc_process_block")
            except:
                print "there is no previouse info"
                sys.exit(0)

            PrevValue = int(Last.Value)
            time.sleep(1)	 
            NewBlock  = PrevValue + 1
            LatestBlock = blockexplorer.get_latest_block()
            print "start process new block %i %i" % (NewBlock, LatestBlock.height)

            if LatestBlock.height == NewBlock or LatestBlock.height < NewBlock:
                print "there is uncofirmed block do nothing"
                sys.exit(0)
           # try:      
            for Block in blockexplorer.get_block_height(NewBlock):
                for Trans in Block.transactions:
                        for output in Trans.outputs :
                            if OwnAccounts.has_key( output.address):
                               if is_out(Trans.inputs, OwnAccounts ):
                                   break
                               else:
                                    Decimal = sato2Dec(output.value)
                                    try:
                                            TransObj = CryptoTransfers.objects.get(crypto_txid = Trans.hash)
                                            print "trans %s is existed to %s  amnt %s %i"  % (TransObj.crypto_txid, TransObj.user.username, TransObj.amnt, TransObj.id)
                                    except  CryptoTransfers.DoesNotExist:
                                            print "trans %s  to save  %s  amnt %s" % (Trans.hash, output.address, Decimal)
                                            TransObj = CryptoTransfers(crypto_txid = Trans.hash,
                                                                        status="processing",
                                                                        amnt = Decimal,
                                                                        currency = CurrencyInstance ,
                                                                        account = output.address,
                                                                        user = OwnAccounts[ output.address ],
                                                                        confirms = 0
                                                                    )
                                            TransObj.sign_record(crypton.settings.CRYPTO_SALT)
                                            TransObj.save()
           
                Last.Value = NewBlock
                Last.save()
            #except:
	#	print "cant finish operation"
           
           
                                
