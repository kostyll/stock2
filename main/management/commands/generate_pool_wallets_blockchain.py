# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sdk.crypto import CryptoAccount
from main.models import Accounts, PoolAccounts, Currency
from datetime import date
from blockchain.wallet import Wallet


class Command(BaseCommand):
    args = ''
    help = 'adding lots of accounts'
    def handle(self, *args, **options):
        CurIns = Currency.objects.get(title = "BTC")
        Crypton = Wallet("8b11fe28-34c7-4275-a013-c94727abac38",")","_")
        
        bulk_add = []

                   
        for i in xrange(1,200):
                 FreeAccount = PoolAccounts(currency = CurIns, status = "created")                      
                 FreeAccount.pub_date = date.today() 
                 d = Crypton.new_address(label = Req.user.username)          
                 Addr = d.address   
                 FreeAccount.address = Addr 
                 bulk_add.append(FreeAccount)    
                 
        PoolAccounts.objects.bulk_create(buld_add)
                 
                                
           
                                

       
       