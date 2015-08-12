# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sdk.crypto import CryptoAccount
from main.models import Accounts


class Command(BaseCommand):
    args = ''
    help = 'fix user settings'
    def handle(self, *args, **options):
        CurrencyTitle = args[0]           
        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")

        for account in Accounts.objects.filter(currency__title = CurrencyTitle):
                 NewAdress  = Crypton.getnewaddress()
                 print u"new address %s for %s" % (NewAdress, account.user.email )
                 account.reference = NewAdress
                 account.save()
                 
                 
                                
           
                                

       
       