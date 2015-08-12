from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from datetime import datetime
from decimal import getcontext
import sys
from django.core.management import call_command



class Command(BaseCommand):
  def handle(self, *args, **options):

  
        #call_command('add_currency', 'BTC','RUR','0.001','3')
        #call_command('add_currency', 'BTC','UAH','0.001','4')
        #call_command('add_currency', 'LTC','USD','0.001','5')
        #call_command('add_currency', 'LTC','EUR','0.001','6')
        #call_command('add_currency', 'LTC','RUR','0.001','7')
        #call_command('add_currency', 'LTC','UAH','0.001','8')
        #call_command('add_currency', 'EUR','USD','1','9')
        #call_command('add_currency', 'RUR','UAH','20','10')
        #call_command('add_currency', 'USD','UAH','20','11')
        #call_command('add_currency', 'EUR','UAH','20','12')
        #call_command('add_currency', 'DOGE','BTC','20','13')
        #call_command('add_currency', 'NMC','BTC','1','14')
        #call_command('add_currency', 'PPC','BTC','1','15')
        call_command('add_currency', 'NVC','BTC','1','16')

