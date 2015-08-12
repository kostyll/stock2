from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import  new_pin4user, PinsImages
from django.db import connection
import time

class Command(BaseCommand):
    args = ''
    help = 'reset pins for all users'
    def handle(self, *args, **options):
        Oper = User.objects.get(id=1)
        for user in User.objects.filter(is_staff = False):
                new_pin = PinsImages(user = user)
                
                print "sent email  to %s  user %s" % (user.email, user.username)
                if len(user.email)>0:
                        new_pin4user(new_pin, Oper)
                time.sleep(1)
        
        
        
           
 
       
