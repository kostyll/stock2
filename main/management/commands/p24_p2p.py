from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import CardP2PTransfers, TransError, p2p_inner_process, get_comisP2P
import time
from datetime import timedelta
from main.msgs import notify_email, notify_admin_withdraw_fail
from django.contrib.auth.models import User
import os
import sys
from main.my_cache_key import my_lock, my_release, LockBusyException
from crypton import settings
from main.global_check import *


def get_p24():
    from sdk.p24 import p24

    return p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'

    def handle(self, *args, **options):

        LOCK = "p2p_lock"
        lock = my_lock(LOCK)

        # try :
        if not check_global_lock():
            print "start process"
            process_command()
            my_release(lock)
        else:
            print "global check"
            #except :
            #	print "Unexpected error:", sys.exc_info()[0]


def process_command():
    Now = datetime.now()
    admin_system = User.objects.get(id=1)
    for item in CardP2PTransfers.objects.filter(status="auto"):
        time.sleep(1)
        print "process withdraw %s to card %s date %s amnt is %s" % (item.user.username,
                                                                     item.CardNumber,
                                                                     item.pub_date,
                                                                     item.amnt )
        if 1 and not item.verify(settings.COMMON_SALT):
            print "SALT FAILED"
            continue
        if (Now - item.pub_date) > timedelta(seconds=900):
            P24 = get_p24()
            item.status = "processed"
            item.save()
            print "start process"
            Result = None
            CardNumber = item.CardNumber
            CardNumber.replace(" ", "")
            try:
                NewAmnt = get_comisP2P(CardNumber, item.amnt)
                Result = P24.pay2p(item.id, CardNumber, NewAmnt)
            except TransError as e:
                item.status = "processing"
                item.save()
            except Exception as e:
                i.status = "processing"
                i.save()
                notify_admin_withdraw_fail(i, str(e))
                continue
            if Result:
                p2p_inner_process(admin_system, item)
            else:
                item.status = "core_error"
                item.save()

            time.sleep(1)
        else:
            print "it's not a time "
  
