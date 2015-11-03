# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import Accounts, Currency, TradePairs, Balances
from django.contrib.admin.views.decorators import staff_member_required
from main.http_common import format_numbers_strong
from django.contrib.auth.models import User


'''
 <h3>Мы должны: {{item.currency}} <h3>
 <p>На ордерах: {{item.sum}} {{item.currency}} </p>
 <p>Ошибка: {{item.mistake}} {{item.currency}} </p>
 <p>Комиссия: {{item.comission}} {{item.currency}} </p>
 <p>Сальдо ввод - вывод: {{item.saldo}} </p> 
'''
import crypton.settings as settings
from django.db import connection
from decimal import Decimal
from sdk.liqpay import liqpay
from sdk.p24 import p24
# from sdk.crypto import CryptoAccount



@staff_member_required
def whole_balance(request):
    CurList = Currency.objects.all()
    UAH = Currency.objects.get(id=1)

    CurrencyConsist = []
    CurrencyLocalBalance = []
    CurrencyFor = []
    SaldoCor = []
    cursor = connection.cursor()
    ##    346 mistake object
    #{% for item in currency_consist %}
    #<p>Сальдо {{ item.currency }} : {{ item.sum }} </p>
    #{% endfor %}
    MinesDec = Decimal("-1")
    for cur in CurList:
        Id = cur.id
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id='%s' \
                         AND user_id not in (346, 31) AND abs(balance)>0.000000001 ", [Id])
        s = cursor.fetchone() * 1
        if s == (None, ):
            s = Decimal("0.0")

        CurrencyConsist.append({"currency": cur.title, "sum": format_numbers_strong(s)})

    ##get balances of crypto without uah
    for cur in Accounts.objects.filter(user_id=settings.CRYPTO_USER).exclude(currency_id=1):
        if cur.balance is None:
            cur.balance = Decimal("0")
        CurrencyLocalBalance.append({"currency": cur.currency.title,
                                     "sum": format_numbers_strong(cur.balance * MinesDec)})

    P24User = User.objects.get(username=p24.str_class_name())
    P24 = Accounts.objects.get(user=P24User, currency_id=1)
    LiqPayU = User.objects.get(username=liqpay.str_class_name())
    LiqPay = Accounts.objects.get(user=LiqPayU, currency_id=1)
    TradePair = TradePairs.objects.get(url_title="p2p_transfers")

    CurrencyLocalBalance.append({"currency": "UAH",
                                 "sum": format_numbers_strong(
                                     MinesDec * (TradePair.transit_from.balance + LiqPay.balance + P24.balance)
                                 )})

    CurrencyFor = []
    Balances = {}
    for cur in CurList:
        if cur.id != 1:
            try:
                Crypto = CryptoAccount(cur.title)
                DecSum = Decimal(Crypto.getbalance())
            except:
                DecSum = Decimal("0.0")

            Sum = format_numbers_strong(DecSum)
            Balances[cur.title] = DecSum
            CurrencyFor.append({"currency": cur.title,
                                "sum": Sum})
    D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID2, settings.P24_PASSWD2, settings.P24MERCH_CARD2)
    D1 = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)
    BalanceUAH = Decimal(D.balance()) + Decimal(D1.balance())
    Balances["UAH"] = BalanceUAH

    CurrencyFor.append({"currency": "UAH",
                        "sum": format_numbers_strong(
                            BalanceUAH
                        )
    })
    ComisId = int(settings.COMISSION_USER)
    for cur in CurList:
        Id = int(cur.id)
        if cur.id != 1:
            cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=%i\
                                AND user_id not in (346, %i, 31 ) AND balance>0 " % ( Id, ComisId ), [])
            (s,) = cursor.fetchone() * 1
            if s == None:
                s = Decimal("0.0")

            SaldoCor.append({"currency": cur.title, "sum":
                format_numbers_strong(Balances[cur.title] - s)})

    cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=1\
                                AND user_id not in (346, %i, 12,31 ) AND balance>0 " % ( ComisId ), [])
    (s, ) = cursor.fetchone() * 1
    SaldoCor.append({"currency": "UAH", "sum":
                     format_numbers_strong(Balances["UAH"] - s)})

    return render_to_response('admin/main/whole_balance.html',
                              {'currency_consist': CurrencyConsist,
                               "currency_local_balance": CurrencyLocalBalance,
                               "currency_balance": CurrencyFor,
                               "saldo": SaldoCor},
                                context_instance=RequestContext(request))
