from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in, cancel_p24_in, TradePairs

from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import Accounts, Currency, TradePairs, Balances
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
import crypton.settings as settings
from django.db import connection
from decimal import Decimal
from sdk.liqpay import liqpay
from sdk.p24 import p24
# from sdk.crypto import CryptoAccount
from main.global_check import *


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'

    def handle(self, *args, **options):
        from sdk.p24 import p24

        cursor = connection.cursor()
        cursor.execute(
            "SELECT sum(balance) FROM main_accounts WHERE currency_id=1 AND balance>0 AND balance<1000000 AND id!=353 ");
        s = cursor.fetchone() * 1
        if s == (None, ):
            s = Decimal("0.0")
        else:
            (s, ) = s
        cursor.execute(
            "SELECT sum(amnt)*0.99 FROM main_cardp2ptransfers WHERE status in ('created','processing','processing2','auto') AND pub_date>='2015-05-08' ");

        s1 = cursor.fetchone() * 1
        if s1 == (None, ):
            s1 = Decimal("0.0")
        else:
            (s1, ) = s1

        D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID2, settings.P24_PASSWD2,
                settings.P24MERCH_CARD2)
        D1 = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)
        BalanceUAH = Decimal(D.balance()) + Decimal(D1.balance())
        print BalanceUAH
        Delta = (BalanceUAH - s - s1 + 30020)
        print "Delta is %s" % Delta
        if Delta < 0:
            print "Delta is  bad %s" % Delta
            lock_global("uah_balance")
