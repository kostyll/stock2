from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in, cancel_p24_in, TradePairs

from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models  import Accounts, Currency, TradePairs,Balances
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
import crypton.settings as settings
from django.db import connection
from decimal import Decimal
from sdk.liqpay import liqpay
from sdk.p24 import p24
#from sdk.crypto import CryptoAccount


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
        from sdk.p24 import p24
        ("SELECT sum(balance) FROM main_accounts WHERE currency_id=1 AND balance>0 AND balance<1000000 AND id!=353");
                         
        D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID2, settings.P24_PASSWD2, settings.P24MERCH_CARD2)
        D1 = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)
        BalanceUAH  = Decimal(D.balance() ) + Decimal(D1.balance())
        print BalanceUAH


                    
       
