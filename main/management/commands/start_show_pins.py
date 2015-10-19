from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import PinsImages, start_show_pin
from django.db import connection


class Command(BaseCommand):
    args = ''
    help = 'reset pins for all users'

    def handle(self, *args, **options):
        for obj in PinsImages.objects.all():
            start_show_pin(obj.show_key, 160000)
            print "start show for %s" % (obj.user.username)
        
        
        
           
 
       
