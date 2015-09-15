from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection

from main.models import Currency, Accounts
from django.contrib.auth.models import User



class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
        F = args[0]      
        List =  list(User.objects.all() )
        bulk_add  = []
        cur_instance = Currency.objects.get(title = F)
               
        for user in List:
                         try:
                                Account  = Accounts.objects.get(user = user,
                                         currency = cur_instance
                                                   )
                         except Accounts.DoesNotExist:       
                                bulk_add.append(
                                        Accounts(  user = user,
                                                   balance = "0.00",
                                                   currency = cur_instance
                                                )
                                )
        
        
        Accounts.objects.bulk_create(bulk_add)           
                                

       
