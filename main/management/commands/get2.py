from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from sdk.crypto import CryptoAccount
from main.models import Balances,sato2Dec

from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext

from blockchain.blockexplorer import get_address
import time

class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'
    def handle(self, *args, **options):

	Crypton = CryptoAccount("BTC", "trade_stock")	
	with open("/home/bogdan/crypton/my_accounts.csv") as f:
    		L = f.readlines()
    		Sum = 0
		Dict= {}
    		for address in L: 
			addresses = address.replace("\n","")
			
			Res = addresses.split(",")
			print "%s,%s,%s" % ( Res[0],Crypton.dumpprivkey(Res[0]),Res[1] )
			if Dict.has_key(Res[0]):
				print "repeated "
				continue
			else:
				Dict[Res[0]] = 1			

			try:
				Bal = Balances.objects.get(account = Res[0])
				Bal.balance = sato2Dec(Res[1])
				Bal.save()
			except:
				
				Bal = Balances(account = Res[0], currency_id=2)
				Bal.balance = sato2Dec(Res[1])
				Bal.save()
