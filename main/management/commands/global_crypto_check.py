from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from  main.finance import notify_admin_withdraw
from main.msgs import notify_email
from main.models import CryptoTransfers, Currency, Accounts, crypton_in, get_decrypted_user_pin
from sdk.crypto import CryptoAccount
import crypton.settings
from sdk.crypto_settings import Settings as CryptoSettings
import sys
from django.db import connection
from decimal import getcontext
from main.my_cache_key import my_lock, my_release, LockBusyException
import os
import sys
from main.global_check import *


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):

        LOCK = "check_crypto"
        lock = None
        try:
            lock = my_lock(LOCK)
            process()
        except LockBusyException as e:
            print "operation is locked", e.value
            sys.exit(0)
        except:
            print "Unexpected error:", str(sys.exc_info())
        finally:
            my_release(lock)


def process():
    # CurrencyInstance = Currency.objects.get(id=3)
    # print "check %s" % CurrencyInstance.title
    #       if not check_crypto_balance(CurrencyInstance) :
    #	       lock_global("inconsistense_"+CurrencyInstance.title )
    #               return

    CurrencyInstance = Currency.objects.get(id=4)
    print "check %s" % CurrencyInstance.title
    if 1 and not check_crypto_balance(CurrencyInstance):
        print "lock %s" % CurrencyInstance.title
        lock_global("inconsistense_" + CurrencyInstance.title)
        return
    CurrencyInstance = Currency.objects.get(id=5)
    print "check %s" % CurrencyInstance.title
    if 0 and not check_crypto_balance(CurrencyInstance):
        lock_global("inconsistense_" + CurrencyInstance.title)
        print "lock %s" % CurrencyInstance.title
        return
    CurrencyInstance = Currency.objects.get(id=7)
    print "check %s" % CurrencyInstance.title
    if 1 and not check_crypto_balance(CurrencyInstance):
        lock_global("inconsistense_" + CurrencyInstance.title)
        print "lock %s" % CurrencyInstance.title
        return
    CurrencyInstance = Currency.objects.get(id=8)
    print "check %s" % CurrencyInstance.title
    if 0 and not check_crypto_balance(CurrencyInstance):
        lock_global("inconsistense_" + CurrencyInstance.title)
        print "lock %s" % CurrencyInstance.title
        return
    CurrencyInstance = Currency.objects.get(id=9)
    print "check %s" % CurrencyInstance.title
    if not check_crypto_balance(CurrencyInstance):
        print "lock %s" % CurrencyInstance.title
        lock_global("inconsistense_" + CurrencyInstance.title)
        return
    CurrencyInstance = Currency.objects.get(id=11)
    print "check %s" % CurrencyInstance.title
    if 1 and not check_crypto_balance(CurrencyInstance, "5200"):
        print "lock %s" % CurrencyInstance.title
        lock_global("inconsistense_" + CurrencyInstance.title)
        return
    CurrencyInstance = Currency.objects.get(id=12)
    print "check %s" % CurrencyInstance.title
    if 0 and not check_crypto_balance(CurrencyInstance):
        print "lock %s" % CurrencyInstance.title
        lock_global("inconsistense_" + CurrencyInstance.title)
        return

    print "check BTC"
    if not check_btc_balance():
        print "lock BTC"
        lock_global("inconsistense_btc")
        return
