from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection

from main.models import Currency, Accounts, VolatileConsts
from django.contrib.auth.models import User
import urllib2
from xml.dom import minidom

class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
             CheckAuto = VolatileConsts.objects.get(Name = "rate_auto")
	     print "rates_usd_uah"
	     print "================================="
             Url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
	     if CheckAuto.Value == "1":
		print "get  rate from privat"
		D = urllib2.urlopen(Url)	
                xml =  D.read()
		doc = minidom.parseString(xml)
             	UsdRate = VolatileConsts.objects.get(Name = "usd_uah_rate")
  		Rates = doc.getElementsByTagName("exchangerate")
		for item in Rates :
			Rate = item.getAttribute("sale")
			cur = item.getAttribute("ccy")
			base = item.getAttribute("base_ccy")
			if base == "UAH" and cur == "USD":
				UsdRate.Value = Rate
				print " new exchange rate is %s" % (Rate)
				UsdRate.save()
				break
                
	     else:
		print "rate setupin manually"  
