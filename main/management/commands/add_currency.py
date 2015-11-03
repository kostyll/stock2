from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import Currency, Accounts, TradePairs
from django.db import connection
from decimal import getcontext


class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'

    def handle(self, *args, **options):
        CurrencyTitle1 = args[0]
        CurrencyTitle2 = args[1]
        min_trade = args[2]
        ordering_stock = args[3]
        CurrencyInstance1 = Currency.objects.get(title=CurrencyTitle1)
        CurrencyInstance2 = Currency.objects.get(title=CurrencyTitle2)
        new_transit = User.objects.create_user("T%s_%s" % ( CurrencyTitle1, CurrencyTitle2 ),
                                               "admin@btc-trade.com.ua",
                                               "test_test")
        new_transit.is_active = False
        new_transit.save()
        AccountTradeOn = Accounts(user=new_transit, currency=CurrencyInstance1, balance="0.00")
        AccountTradeBase = Accounts(user=new_transit, currency=CurrencyInstance2, balance="0.00")
        AccountTradeOn.save()
        AccountTradeBase.save()
        Title = "%s/%s" % (CurrencyTitle1, CurrencyTitle2 )
        Url = "%s_%s" % (CurrencyTitle1.lower(), CurrencyTitle2.lower() )
        TradePairsInstance = TradePairs(title=Title,
                                        url_title=Url,
                                        ordering=int(ordering_stock),
                                        transit_on=AccountTradeOn,
                                        transit_from=AccountTradeBase,
                                        currency_on=CurrencyInstance1,
                                        currency_from=CurrencyInstance2,
                                        status="created",
                                        min_trade_base=min_trade
        )
        TradePairsInstance.save()
        
        
           
 
       
