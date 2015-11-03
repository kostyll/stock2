from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from main.models import Balances, Accounts, Currency
from sdk.crypto import CryptoAccount
import crypton.settings

from sdk.crypto_settings import Settings as CryptoSettings

from django.db import connection
from decimal import getcontext, Decimal


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every 30 minute cache balance on hot wallets'

    def handle(self, *args, **options):
        CurrencyTitle = args[0]
        Crypton = CryptoAccount(CurrencyTitle, "trade_stock")
        CurrencyInstance = Currency.objects.get(title=CurrencyTitle)
        getcontext().prec = crypton.settings.TRANS_PREC
        BalanceDictionary = {}

        for item in Accounts.objects.filter(currency=CurrencyInstance):
            if item.reference is not None and item.reference != "":
                print "process account "
                print item.reference
                try:
                    item = Balances.objects.get(account=item.reference)

                    BalanceDictionary[item.account] = Decimal("0.0")
                except:
                    NewBalance = Balances(account=item.reference, balance=Decimal("0.0"), currency=CurrencyInstance)
                    NewBalance.save()
                    BalanceDictionary[NewBalance.account] = Decimal("0.0")

        for item in Balances.objects.filter(currency=CurrencyInstance):
            BalanceDictionary[item.account] = Decimal("0.0")

        List = Crypton.listunspent()
        for trans in List:

            Address = trans["address"]
            Amount = Decimal(trans["amount"])
            print " unspent inputs in %s of %s " % (Address, Amount)
            if BalanceDictionary.has_key(Address):
                PreBalance = BalanceDictionary[Address]
                BalanceDictionary[Address] = PreBalance + Amount
            else:
                BalanceDictionary[Address] = Amount
                NewBalance = Balances(account=Address, balance=Decimal("0.0"), currency=CurrencyInstance)
                NewBalance.save()
        WholeSum = Decimal("0.0")
        for trans in Balances.objects.filter(currency=CurrencyInstance):
            trans.balance = BalanceDictionary[trans.account]
            WholeSum = WholeSum + trans.balance
            trans.save()

        try:
            item = Balances.objects.get(account="whole", currency=CurrencyInstance)
            item.balance = WholeSum
            item.save()
        except:
            NewBalance = Balances(account="whole", currency=CurrencyInstance, balance=WholeSum)
            NewBalance.save()
                           
                
        
       
       
       
