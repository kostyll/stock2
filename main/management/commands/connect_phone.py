from django.core.management.base import BaseCommand, CommandError
from main.models import Orders,P24TransIn
import hashlib
import sys

class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'
    def handle(self, *args, **options):
	F = args[0]

        with open(F, 'r') as f:


             content = f.readlines()
	     #2014-10-12 21:25:31.643,+380503202264,P24A110486415879993,4206,490
             #sending funds of natasha to 1MFV449MQ2YcsXt1mzf3V1ip9CoR3vqTKt amount 340000
             #txid d5b46042ad7cbdadcebae0a6c5306c5157818bcdde7b5b419ae9154615d7650b     
             for line in content:
	         Params = line.split(",")
		 Phone = Params[1]
		 Ref = Params[2]
		 print Params
                 OrderId = int(Params[3])
		 Order = Orders.objects.get(id = OrderId)
		 P24In = None
		 try :
                 	P24In =  P24TransIn.objects.get(order = Order)
		 except: 
			print "doesn't find"
			continue
		 
		 P24In.phone = Phone
                 P24In.ref = Ref
		 P24In.save()
		 User = Order.user
                 User.first_name = User.first_name + "," + Phone
		 User.save()
	          
		
       
           
 
       
