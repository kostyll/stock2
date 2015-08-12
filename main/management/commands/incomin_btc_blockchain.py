from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import   notify_admin_withdraw
from main.models import CryptoTransfers, Currency, Accounts, crypton_in, sato2Dec
from sdk.crypto import CryptoAccount
from sdk.crypto_settings import Settings as CryptoSettings

import crypton.settings 


import urllib2
import time
import json

from main.my_cache_key import my_lock, my_release, LockBusyException
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
import os
import sys




class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        
        Time =  0   
        try :
              Time = int(args[0])
        except :
              Time = 0  
        print "from %i " % (Time)
        LOCK = "in_cryptoblck_info"
    #	lock = None
        try:
            lock = my_lock(LOCK)
            process_block_info(Time)

        except LockBusyException as e:
                   print "operation is locked", e.value
        except :
               print "Unexpected error:",str( sys.exc_info())

        my_release(lock)
	
       
def process_block_info(Time):
       
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = "BTC")
        getcontext().prec = crypton.settings.TRANS_PREC
        LastBlock = get_last_block()
        print "current block height is %i " % (LastBlock)
        AccountList = Accounts.objects.filter(currency = CurrencyInstance ).order_by('balance')
        OwnAccounts = {}
        for i in AccountList:
                OwnAccounts[i.reference] = 1
	
        for Account in AccountList :
                Address = Account.reference
                if Address is None :
                        continue
                
                print "process adress %s" % (Address)
                
                try:
                        TransList = get_adress_list(Address)
                except :
                        print "get error during processing the "
                        continue

                for trans in TransList:
                        Txid = trans["hash"]
                        print "find trans %s for %s " % (Txid, Address )
                    
                        if  trans["time"]<Time:
                                print "this trans is old"
                                continue
                        
                        print str(trans)
                        
                        try :
                                Confirmations = LastBlock - trans["block_height"] + 1
                        except :
                                continue
                        
                        if is_out(trans["inputs"], OwnAccounts) : 
                                print "it is out trans for us %s" % (Txid)
                                continue
                        
                        
                        try:
                                Decimal = get_in_acc(trans["out"],  Address )
                        except :
                                print "get error during processing the "
                                continue
                        
                        if Decimal == 0:
                                print "it is out trans for %s " % (Address)
                                continue
                        
                        Trans = None
                        print "confirmations %i" % ( Confirmations )                        
                        print " amount of %s" % (Decimal )
                        
                        
                        try :
                                Trans = CryptoTransfers.objects.get(crypto_txid = Txid)  
                        except  CryptoTransfers.DoesNotExist:   
                                Trans =  CryptoTransfers(crypto_txid = Txid,
                                                         status="created",
                                                         amnt = Decimal,
                                                         currency = CurrencyInstance ,
                                                         account = Address,
                                                         user = Account.user,
                                                         confirms = Confirmations   
                                                         )
                                Trans.save()
                                
                        print "#%i receive %s to %s amount of %s" % (Trans.id, Txid, Address, Trans.amnt )
                        print "this trans is %s" % ( Trans.status )
                        continue 
 	                if Confirmations > CryptoSettings["BTC"]["min_confirmation"] and Trans.status!= "processed":
                           print "processing it"
                           Trans.confirms = Confirmations
                           Trans.status = "processing"
                           Trans.save()
                           crypton_in(Trans, user_system)
                           Trans.status = "processed"
                           Trans.save()
                                        
                        if Trans.status == "processing" or Trans.status == "created":     
                           print "update confirmations"
                           Trans.status = "processing"
                           Trans.confirms = Confirmations
                           Trans.save()
       
def get_adress_list( Adr ):
    Url = "https://blockchain.info/address/%s?format=json" % (Adr)
    
    Decoder = json.JSONDecoder()
    D = urllib2.urlopen(Url)
    Str = D.read()        
    Res = Decoder.decode(Str)
    return Res["txs"]

def is_out(Trans, OwnAccounts ):
   print str(Trans)
	
   for i in Trans:
        	if OwnAccounts.has_key( i["prev_out"]["addr"] ) :


	           return  True

   return False

def get_in_acc(Trans, Address):    
    Sum = 0    
    for i in Trans:
        if i["addr"] == Address :
           print "receive %i" % (i["value"])
           
           Sum = Sum + i["value"]
           
    return sato2Dec(Sum)
    
    
    
def get_last_block():
        Url = "https://blockchain.info/blocks?format=json"
        Decoder = json.JSONDecoder()
        D = urllib2.urlopen(Url)
        Str = D.read()        
        Res = Decoder.decode(Str)
        return Res["blocks"][0]["height"]
        
