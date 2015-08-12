# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sdk.crypto import CryptoAccount 
from main.models import Accounts, PoolAccounts, Currency
from datetime import date


class Command(BaseCommand):
    args = ''
    help = 'adding lots of accounts'
    def handle(self, *args, **options):
        for   CurrencyTitle  in ('LTC', 'DOGE', 'NVC', 'DRK', 'RMS', 'CLR', 'PPC'):
            Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
            CurIns = Currency.objects.get(title = CurrencyTitle)
        
            bulk_add = []
            Addresses = {}
                
            for i in xrange(1,50):
                    FreeAccount = PoolAccounts(currency = CurIns, status = "created")                      
                    FreeAccount.pub_date = date.today() 
                    NewAdress  = Crypton.getnewaddress()
                    FreeAccount.address = NewAdress 
            
                    if Addresses.has_key(NewAdress):
                        print "repeat address %s" % (NewAdress)
                    else:
                        print "generate %i %s" % (i, NewAdress)
                        bulk_add.append(FreeAccount)    
                
            PoolAccounts.objects.bulk_create(bulk_add)
                
                                
           
                                

       
       
