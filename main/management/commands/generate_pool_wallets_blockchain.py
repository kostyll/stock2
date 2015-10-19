# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from sdk.crypto import CryptoAccount
from sdk.crypto_settings import Settings as CryptoSettings
from main.models import Accounts, PoolAccounts, Currency
from datetime import date
from blockchain.wallet import Wallet


class Command(BaseCommand):
    args = ''
    help = 'adding lots of accounts'

    def handle(self, *args, **options):
        CurIns = Currency.objects.get(title="BTC")
        Crypton = Wallet(CryptoSettings["BTC"]["host"],
                         CryptoSettings["BTC"]["rpc_user"],
                         CryptoSettings["BTC"]["rpc_pwd"])

        bulk_add = []
        # for account in Accounts.objects.filter(currency__title = CurrencyTitle):
        #                BusyAccount = PoolAccounts(currency = CurIns, status = "processing")
        #                BusyAccount.user =  account.user
        #                BusyAccount.status = "processing"
        #                BusyAccount.address = account.reference
        #                bulk_add.append(BusyAccount)

        for i in xrange(1, 50):
            FreeAccount = PoolAccounts(currency=CurIns, status="created")
            FreeAccount.pub_date = date.today()
            d = Crypton.new_address(label="pool")
            print d.address
            Addr = d.address
            FreeAccount.address = Addr
            bulk_add.append(FreeAccount)

        PoolAccounts.objects.bulk_create(bulk_add)
                 
                                
           
                                

       
       
