# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sdk.crypto import CryptoAccount 
from main.models import Accounts, PoolAccounts, Currency
from datetime import date


class Command(BaseCommand):
    args = ''
    help = 'adding lots of accounts'
    def handle(self, *args, **options):
        CurrencyTitle = args[0]           
        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
        CurIns =  Currency.objects.get(title = CurrencyTitle)
        
        bulk_add = []
        for account in Accounts.objects.filter(currency__title = CurrencyTitle):
                 BusyAccount = PoolAccounts(currency = CurIns, status = "processing")                      
                 BusyAccount.user =  account.user
                 BusyAccount.status = "processing"
                 BusyAccount.address = account.reference
                 bulk_add.append(BusyAccount)
                   
        for i in xrange(1,500):
                 FreeAccount = PoolAccounts(currency = CurIns, status = "created")                      
                 FreeAccount.pub_date = date.today() 
                 NewAdress  = Crypton.getnewaddress()
                 FreeAccount.address = NewAdress 
                 bulk_add.append(FreeAccount)    
                 
        PoolAccounts.objects.bulk_create(buld_add)
                 
                                
           
                                

       
       