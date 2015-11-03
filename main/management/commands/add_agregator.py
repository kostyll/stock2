from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from main.models import Currency, Accounts, TradePairs

from main.http_common import format_numbers_strong
from django.db import connection
from decimal import getcontext


class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'

    def handle(self, *args, **options):
        prefix = args[0]
        CurrencyTitle = args[1]
        min_trade = args[2]
        ordering_stock = args[3]
        CurrencyInstance1 = Currency.objects.get(title=CurrencyTitle)
        new_transit = User.objects.create_user("transit_%s_%s" % (prefix, CurrencyTitle),
                                               "admin@",
                                               "test_test")
        new_transit.is_active = False
        new_transit.save()
        AccountTradeOn = Accounts(user=new_transit, currency=CurrencyInstance1, balance="0.00")
        AccountTradeBase = Accounts(user=new_transit, currency=CurrencyInstance1, balance="0.00")
        AccountTradeOn.save()
        AccountTradeBase.save()
        Title = "%s_%s" % (prefix, CurrencyTitle.lower())
        Url = "%s_%s" % (prefix, CurrencyTitle.lower())
        TradePairsInstance = TradePairs(title=Title,
                                        url_title=Url,
                                        ordering=int(ordering_stock),
                                        transit_on=AccountTradeOn,
                                        transit_from=AccountTradeBase,
                                        currency_on=CurrencyInstance1,
                                        currency_from=CurrencyInstance1,
                                        status="created",
                                        min_trade_base=min_trade
        )
        TradePairsInstance.save()
        
        
           
 
       
