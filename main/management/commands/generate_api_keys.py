from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from main.models import ApiKeys
from main.http_common import generate_key_from, generate_key
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext
import hashlib


class Command(BaseCommand):
    args = '<CurrencyTitle1 CurrencyTitle2 MinTrade...>'
    help = 'first currency is trade Currency, the second currency is base Currency'
    def handle(self, *args, **options):
        for one_user  in User.objects.all():
            if not  one_user.is_staff and one_user.is_active:
                Key1 = generate_key()
                Key2 = generate_key()
                PrivateKey = generate_key_from(Key1, one_user.email)
                new_obj = ApiKeys(public_key = Key2, private_key = PrivateKey, user = one_user)
                new_obj.save()
        
           
 
       
